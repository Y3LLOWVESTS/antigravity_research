"""Execute PH12's isolated trap-free gauged source feasibility audit.

No magnetic carrier, gravitational lift or SI energy is certified.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys

from antigravity_research.agminer import (
    hook17_ph12_gauged_qball_source as ph12
)


def main():
    root=Path.cwd()
    data=ph12.run(root)
    now=datetime.now(timezone.utc)

    data["execution"]={
        "utc":now.isoformat(),
        "python":sys.version,
        "platform":platform.platform(),
        "module_sha256":
            sha256(Path(ph12.__file__).read_bytes()).hexdigest(),
        "simulation_sha256":
            sha256(Path(__file__).read_bytes()).hexdigest(),
    }

    out=root/"results/data"/(
        "032h17_ph12_gauged_qball_"
        +now.strftime("%Y%m%dT%H%M%S%fZ")
        +".json"
    )
    out.parent.mkdir(parents=True,exist_ok=True)

    with out.open("x",encoding="utf-8") as stream:
        json.dump(
            data,stream,sort_keys=True,indent=2,allow_nan=False
        )
        stream.write("\n")

    p=data["primary_gauged_equilibrium"]

    print("RUN="+data["branch"])
    print("PROVENANCE="+data["gates"]["P0_PROVENANCE"])

    for key in (
        "omega",
        "center_f",
        "tail_f_relative",
        "BVP_max_collocation_rms",
        "relative_gauss_flux_error",
        "Noether_number",
        "gauge_charge_integrated",
        "relative_integrated_stress_defect",
        "exact_radial_stress_balance_max_residual",
    ):
        print(key.upper()+"="+str(p[key]))

    print("CANONICAL_ENERGY="+str(p["canonical_energy"]))
    print("LARGER_DOMAIN="+str(data["larger_domain_control"]))
    print("MESH="+str(data["high_precision_mesh_control"]))
    print("BRANCH_SLOPE="+str(
        data["local_branch_stability_slope_control"]
    ))
    print("CHARGE_CONJUGATE="+str(data["charge_conjugation"]))
    print("UNBOUND_NEGATIVE_CONTROL="+str(
        data["unbound_branch_negative_control"]
    ))
    print("STRONGER_GAUGE_NEGATIVE_CONTROL="+str(
        data["stronger_gauge_negative_control"]
    ))

    for name,status in data["gates"].items():
        print("GATE_"+name+"="+status)

    print("VERDICT="+data["verdict"])
    print("JSON="+str(out))

    return (
        0 if data["gates"]["P0_PROVENANCE"]=="PASS"
        else 2
    )


if __name__=="__main__":
    raise SystemExit(main())
