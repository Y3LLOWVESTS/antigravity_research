"""Run the G01-R provider using the active checkout's native GRAVITY2 watchdog."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time


def copy_once(src,dest):
    if dest.exists():
        if src.read_bytes()!=dest.read_bytes():
            raise ValueError("existing evidence differs: "+str(dest))
        return
    with tempfile.NamedTemporaryFile(dir=dest.parent) as tmp:
        tmp.write(src.read_bytes()); tmp.flush()
        os.link(tmp.name,dest)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase",choices=("apply","verify"))
    parser.add_argument("repo",type=Path)
    parser.add_argument("output",type=Path,nargs="?")
    args=parser.parse_args()
    phase=args.phase
    root=args.repo.resolve()
    package=Path(__file__).resolve().parent
    out=(args.output or root/"results/gravity2/g01r_finite_range_miner_v1").resolve()
    stage_mode=args.output is not None
    sys.path.insert(0,str(root/"src"))
    from antigravity_research.gravity2 import engine,policy
    if engine.ROOT!=root:
        raise ValueError("miner checkout drift")
    for mod,pin in ((engine,"17f83c04ec069a56e5a678240051cbe18589398bde06de6dafb7c64d81f6fae6"),
                    (policy,"e35aeb28d11fa5621d7767c53698ca614b1fa99b4efd717a415cb2d32cb6c25c")):
        if engine.digest(Path(mod.__file__))!=pin:
            raise ValueError("native miner code drift")
    out.mkdir(exist_ok=True,parents=True)
    if out==package: raise ValueError("choose an evidence directory separate from source")
    pins={"produce.py":"5d09c4c9ed7bf494f1a5554d22191645e9e54d774a34fb0c7a93abb5b952c380",
          "verify.py":"0cf68d263f7aa5dcec7774fa79c582a77ce4819249fc3cf68608d5cf3e5c1357",
          "constraints.py":"e8bd5c1ae8602cc8bec0330fbbbd65e6ce963696880ad31dda7ad8c848ea6b2d"}
    for n,pin in pins.items():
        if engine.digest(package/n)!=pin: raise ValueError("provider drift: "+n)
    env=dict(os.environ,OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1",VECLIB_MAXIMUM_THREADS="1",MKL_NUM_THREADS="1")
    source="produce.py" if phase=="apply" else "verify.py"
    copy_once(package/source,out/source)
    if not stage_mode:
        label="source" if phase=="apply" else "check"
        copy_once(package/source,root/"scripts"/f"g01r_finite_range_{label}_v1.py")
    result="science.json" if phase=="apply" else "verification.json"
    if phase=="apply" and not (out/"parents.json").exists():
        parents=engine.parent_audit()
        if any(v["mandatory"] and v["status"]!="MATCH" for v in parents.values()):
            raise ValueError("native mandatory parents drift")
        audit=subprocess.check_output([sys.executable,"-IB","-m","antigravity_research.gravity2.registry_v6","audit"],
                                      cwd=root,env=env,text=True,timeout=30)
        engine.atomic_json(out/"parents.json",dict(parents=parents,registry=audit,engine_sha256=engine.digest(Path(engine.__file__))))
    if not (out/result).exists():
        used=0 if phase=="apply" else json.loads((out/"apply_runtime.json").read_text())["seconds"]
        seconds=450 if phase=="apply" else 600-used
        if seconds<=0: raise ValueError("compute budget exhausted")
        with tempfile.TemporaryDirectory(dir=out,prefix="work_") as folder:
            work=Path(folder)
            copy_once(out/source,work/source)
            if phase=="verify":
                for n in ("science.json","produce.py"): copy_once(out/n,work/n)
            start=time.monotonic()
            cmd=[sys.executable,"-IB",str(work/source),str(root),str(work)]
            local_meter=False
            try:
                local_meter=engine.rss_tree_mib(os.getpid()) is None
            except PermissionError:
                local_meter=True
            original_meter=engine.rss_tree_mib
            if local_meter:
                # These two providers are single-process. On restricted macOS
                # hosts the worker can report its own kernel high-water mark.
                (work/"rss").write_bytes(bytes(8))
                meter_code="""import mmap,resource,runpy,sys,threading,time
from pathlib import Path
meter=Path(sys.argv[3])/'rss'
def measure():
    with meter.open('r+b') as stream, mmap.mmap(stream.fileno(),8) as buf:
        while True:
            usage=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            buf[:]=int(usage*(1 if sys.platform=='darwin' else 1024)).to_bytes(8,'little')
            time.sleep(.05)
threading.Thread(target=measure,daemon=True).start()
sys.argv=sys.argv[1:]
runpy.run_path(sys.argv[0],run_name='__main__')"""
                cmd=[sys.executable,"-IB","-c",meter_code,*cmd[2:]]
                engine.rss_tree_mib=lambda pid: int.from_bytes((work/"rss").read_bytes(),"little")/1048576
            worker=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,start_new_session=True)
            try:
                status,peak,monitor,code,_,_=engine.supervise(worker,work,seconds,policy.PRESETS["extended"][1],24,start)
            finally:
                engine.rss_tree_mib=original_meter
                engine.terminate_group(worker)
            if local_meter: monitor="SINGLE_WORKER_KERNEL_PEAK_RSS"
            elapsed=time.monotonic()-start
            print((work/"worker.log").read_text(),end="")
            if status!="COMPLETED" or code!=0: raise ValueError(f"{phase} {status} exit={code}")
            engine.atomic_json(work/"runtime.json",dict(seconds=elapsed,peak_RSS_MiB=peak,
                        monitor=monitor,engine_status=status,budget_seconds=seconds))
            for src,dest in (("worker.log",phase+".log"),("runtime.json",phase+"_runtime.json"),(result,result)):
                copy_once(work/src,out/dest)
    if phase=="verify":
        record=json.loads((out/"verification.json").read_text())
        if record["science_sha256"]!=engine.digest(out/"science.json") or record["checker_sha256"]!=engine.digest(out/"verify.py"):
            raise ValueError("verification binding drift")
        copy_once(package/"constraints.py",out/"constraints.py")
        copy_once(Path(__file__).resolve(),out/"run.py")
        if not stage_mode:
            copy_once(package/"constraints.py",root/"scripts/g01r_finite_range_constraints_v1.py")
        spent=sum(json.loads((out/(s+"_runtime.json")).read_text())["seconds"] for s in ("apply","verify"))
        subprocess.run([sys.executable,"-IB",str(out/"constraints.py"),str(out)],check=True,
                       env=env,timeout=min(30,max(.1,600-spent)))
        copy_once(out.with_name(out.name+"_constraints.json"),out/"constraints.json")
        names=("produce.py","verify.py","constraints.py","run.py","science.json","verification.json",
               "constraints.json","parents.json","apply.log","verify.log","apply_runtime.json","verify_runtime.json")
        with tempfile.TemporaryDirectory(dir=out.parent,prefix="g01r_publish_") as folder:
            work=Path(folder)
            ledger=work/"SHA256SUMS.txt"
            ledger.write_text("".join(f"{engine.digest(out/n)}  {n}\n" for n in names))
            copy_once(ledger,out/"SHA256SUMS.txt")
            archive=out.with_name(out.name+"_UPLOAD.tar.gz")
            if not archive.exists():
                tmp=work/"archive"
                with tarfile.open(tmp,"w:gz") as bundle:
                    for n in (*names,"SHA256SUMS.txt"): bundle.add(out/n,arcname=out.name+"/"+n)
                os.link(tmp,archive)
            with tarfile.open(archive,"r:gz") as bundle:
                for n in (*names,"SHA256SUMS.txt"):
                    if bundle.extractfile(out.name+"/"+n).read()!=(out/n).read_bytes(): raise ValueError("archive drift")
            print("ARCHIVE_SHA256",engine.digest(archive))
    print(phase.upper(),result,engine.digest(out/result),"FULL_REGRESSION=NOT_RUN")


if __name__=="__main__":
    main()
