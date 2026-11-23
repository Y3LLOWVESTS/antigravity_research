"""Run the G01-S provider using the active checkout's native GRAVITY2 watchdog."""
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


def execute(root, package, out, phase, source, result, budget, stage_mode, engine, policy):
    env=dict(os.environ,OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1",VECLIB_MAXIMUM_THREADS="1",MKL_NUM_THREADS="1")
    copy_once(package/source,out/source)
    if not stage_mode:
        label={"apply":"source","verify":"check","loaded":"loaded","comparison":"comparison","independent":"independent"}[phase]
        copy_once(package/source,root/"scripts"/f"g01s_capacitor_{label}_v1.py")
    if (out/result).exists():
        if not (out/(phase+"_runtime.json")).exists(): raise ValueError("incomplete prior publication")
        return
    seconds=budget
    if seconds<=0: raise ValueError("research time budget exhausted")
    with tempfile.TemporaryDirectory(dir=out,prefix="work_") as folder:
        work=Path(folder)
        copy_once(out/source,work/source)
        if phase!="apply":
            for n in ("produce.py","science.json"): copy_once(out/n,work/n)
        if phase in ("loaded","comparison"): copy_once(out/"verification.json",work/"verification.json")
        if phase=="comparison":
            for n in ("loaded.py","loaded.json"): copy_once(out/n,work/n)
        if phase=="independent":
            for n in ("loaded.json","comparison.json"): copy_once(out/n,work/n)
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

PROVIDERS={'produce.py': 'a0ee8bc0e2e67490befab3c57d38ff2ec74e0371ca9a0a1d7711dc25ab364bba', 'verify.py': 'b12faf27f8a369f8def05a9dbdf66e146779f472da3d022c16bbac9874a9c5ca', 'loaded.py': '7c6cfe7eaa739054cf0b06f561c2f5b7112d8875c28abae1550ccf2123f03270'}

PROVIDERS["compare.py"]="d01a7c5b44adb70ef9661ce030c3b5b3028b5ef95406f11bcb272c2d8f448f62"

PROVIDERS["audit.py"]="25a688947d6bc7297882d63e2d30ee613538416afd3cfd343328115784bcbd91"

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase",choices=("apply","verify"))
    parser.add_argument("repo",type=Path)
    parser.add_argument("output",type=Path,nargs="?")
    args=parser.parse_args()
    package=Path(__file__).resolve().parent
    root=args.repo.resolve()
    out=(args.output or root/"results/gravity2/g01s_capacitor_miner_v1").resolve()
    stage=args.output is not None
    sys.path.insert(0,str(root/"src"))
    from antigravity_research.gravity2 import engine,policy
    if root!=engine.ROOT or out==package: raise ValueError("repo or evidence path")
    for mod,pin in ((engine,"17f83c04ec069a56e5a678240051cbe18589398bde06de6dafb7c64d81f6fae6"),
                    (policy,"e35aeb28d11fa5621d7767c53698ca614b1fa99b4efd717a415cb2d32cb6c25c")):
        if engine.digest(Path(mod.__file__))!=pin: raise ValueError("miner code drift")
    for n,pin in PROVIDERS.items():
        if engine.digest(package/n)!=pin: raise ValueError("provider drift: "+n)
    out.mkdir(exist_ok=True,parents=True)
    if args.phase=="apply":
        if not (out/"parents.json").is_file():
            parents=engine.parent_audit()
            if any(v["status"]!="MATCH" and v["mandatory"] for v in parents.values()): raise ValueError("parent drift")
            audit=subprocess.check_output([sys.executable,"-IB","-m","antigravity_research.gravity2.registry_v6","audit"],
                                          cwd=root,text=True,timeout=20)
            engine.atomic_json(out/"parents.json",dict(parents=parents,registry=audit))
        execute(root,package,out,"apply","produce.py","science.json",240,stage,engine,policy)
        print("SCIENCE_SHA256",engine.digest(out/"science.json"))
        return
    if not (out/"science.json").is_file(): raise ValueError("apply required")
    used=lambda: sum(json.loads(f.read_text())["seconds"] for f in out.glob("*_runtime.json"))
    execute(root,package,out,"verify","verify.py","verification.json",min(100,600-used()),stage,engine,policy)
    execute(root,package,out,"loaded","loaded.py","loaded.json",600-used(),stage,engine,policy)
    execute(root,package,out,"comparison","compare.py","comparison.json",600-used(),stage,engine,policy)
    execute(root,package,out,"independent","audit.py","independent.json",600-used(),stage,engine,policy)
    independent=json.loads((out/"independent.json").read_text())
    if independent["comparison_sha256"]!=engine.digest(out/"comparison.json") or independent["auditor_sha256"]!=engine.digest(out/"audit.py"):
        raise ValueError("independent audit chain drift")
    comparison=json.loads((out/"comparison.json").read_text())
    if comparison["exp_loaded_sha256"]!=engine.digest(out/"loaded.json") or comparison["source_sha256"]!=engine.digest(out/"compare.py"):
        raise ValueError("constitutive comparison chain drift")
    v=json.loads((out/"verification.json").read_text())
    loaded=json.loads((out/"loaded.json").read_text())
    if v["science_sha256"]!=engine.digest(out/"science.json") or v["checker_sha256"]!=engine.digest(out/"verify.py") or loaded["source_sha256"]!=engine.digest(out/"loaded.py") or loaded["science_sha256"]!=v["science_sha256"]:
        raise ValueError("verification chain drift")
    copy_once(Path(__file__).resolve(),out/"run.py")
    members=["run.py",*PROVIDERS,"science.json","verification.json","loaded.json","comparison.json","independent.json","parents.json"]
    for phase in ("apply","verify","loaded","comparison","independent"):
        members.extend([phase+".log",phase+"_runtime.json"])
    with tempfile.TemporaryDirectory(dir=out.parent,prefix="g01s_publish_") as temp:
        work=Path(temp)
        ledger=work/"SHA256SUMS.txt"
        ledger.write_text("".join(f"{engine.digest(out/n)}  {n}\n" for n in members))
        copy_once(ledger,out/ledger.name)
        archive=out.with_name(out.name+"_UPLOAD.tar.gz")
        if not archive.exists():
            fresh=work/"archive"
            with tarfile.open(fresh,"w:gz") as tar:
                for n in [*members,ledger.name]: tar.add(out/n,arcname=out.name+"/"+n)
            os.link(fresh,archive)
        with tarfile.open(archive,"r:gz") as tar:
            for n in [*members,ledger.name]:
                if tar.extractfile(out.name+"/"+n).read()!=(out/n).read_bytes(): raise ValueError("archive drift")
    print("ARCHIVE_SHA256",engine.digest(archive),"FULL_REGRESSION=NOT_RUN")
if __name__=="__main__": main()
