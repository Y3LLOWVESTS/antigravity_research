"""Independent GRAVITY2-02 action-atlas evidence verifier."""
from __future__ import annotations

import json
import sympy as sp

from . import action02_core as core
from .action02 import code_hashes
from .engine import ROOT, atomic_json, atomic_text, digest


def verify_run(directory):
    checks={}

    def check(name,ok):
        checks[name]=bool(ok)
        if not ok:
            raise AssertionError(name)

    try:
        manifest=json.loads(
            (directory/"manifest.json").read_text()
        )
        science=json.loads(
            (directory/"science.json").read_text()
        )
        recorded={
            name:hash_value
            for hash_value,name in (
                row.split("  ",1)
                for row in (
                    directory/"hashes.sha256"
                ).read_text().splitlines()
            )
        }

        check(
            "manifest SHA",
            recorded["manifest.json"]==
                digest(directory/"manifest.json")
        )
        check(
            "science SHA",
            recorded["science.json"]==
                digest(directory/"science.json")
        )
        check(
            "run ID",
            manifest["run_id"]==
                science["run_id"]==directory.name
        )
        check(
            "producing sources",
            manifest["producer_sha256"]==code_hashes()
        )
        check(
            "read-only old miner",
            manifest["legacy_AGMINER"]==
                "READ_ONLY_HASH_NO_EXECUTION"
        )
        check(
            "previous GRAVITY2 untouched declaration",
            manifest["GRAVITY2_00_01"]=="NOT_MODIFIED"
        )
        check(
            "L0 only",
            manifest["level"]=="L0"
            and manifest["workers"]==1
        )
        check(
            "no physical promotion",
            science["complete_covariant_action"]
                =="NOT_DERIVED"
            and science["qualified_physical_survivors"]==0
            and science["whole_craft_lift"]=="NOT_DERIVED"
            and science["complete_energy"]=="NOT_CERTIFIED"
            and science["006D_replaced"] is False
        )
        check(
            "full regression not claimed",
            science["full_regression"]=="NOT_RUN"
        )
        check(
            "resource scope",
            science["resource"]["limit_kind"]==
                "APPLICATION_SOFT_WATCHDOG"
        )

        if science["execution_status"]=="COMPLETED":
            e=science["evidence"]
            check(
                "parent decision",
                e["decision"]==
                    "SCOPED_ACTION_TEMPLATE_ATLAS_NO_PROMOTION"
            )

            for name,pin in e["parents"].items():
                path=ROOT/pin["path"]
                check(
                    "G01 live SHA "+name,
                    digest(path)==pin["expected_sha256"]
                    and pin["actual_sha256"]==pin["expected_sha256"]
                )

            pins,_=core.read_pinned(ROOT)
            for name,pin in pins.items():
                check(
                    "historical source "+name,
                    pin["status"]=="MATCH"
                    and e["historical_files"][name]
                        ["actual_sha256"]==pin["actual_sha256"]
                )

            check(
                "three distinct candidate templates",
                [c["id"] for c in e["candidates"]]==[
                    "C0_SOURCE_FREE_CONTROL",
                    "C1_TWO_CHARGED_SCALARS",
                    "C2_POINT_CHARGE_CONTROL",
                ]
            )
            check(
                "no invented source existence",
                e["candidates"][1]["sourceability"]==
                    "FINITE_STABLE_EQUILIBRIUM_NOT_DERIVED"
            )
            check(
                "point-charge reject scoped",
                e["candidates"][2]["classification"]==
                    "REJECT_INFINITE_SELF_ENERGY_UNDER_ASSUMPTIONS"
            )
            check(
                "support and Earth actions open",
                "UNEXPANDED" in e["source_action_template"]["supports"]
                and "UNEXPANDED" in e["source_action_template"]["Earth_matter"]
            )
            check(
                "G02 partial only",
                e["gates"]["G02_VARIATION"]==
                    "PARTIAL_EXACT_PORTAL_AND_SOURCE_VARIATION"
            )
            check(
                "no full action",
                e["qualified_survivors"]==0
                and e["complete_action"]=="NOT_DERIVED"
            )
            check(
                "loaded failure retained",
                e["historical_loaded_min_m_s2"]==
                    -129.67185782242464
            )
            check(
                "field capacity not operating energy",
                e["historical_R3B_capacity_J"]==
                    1.5429162116460216
                and e["historical_values"]==
                    "PROVENANCE_ANCHORS_NOT_RECOMPUTED"
            )

            # Independently derive conformal metric trace factor.
            p,a,b,t=sp.symbols("p a b t")
            sig=lambda z:a*z-b*z*z
            s=(1+t)*sp.exp(
                2*sig(p/(1+t)**2)-2*sig(p)
            )
            independently_derived=sp.simplify(
                sp.diff(s,t).subs(t,0)
            )
            expected=1-4*p*(a-2*b*p)
            check(
                "independent conformal metric derivative",
                sp.simplify(independently_derived-expected)==0
            )
            check(
                "reported metric trace structure",
                sp.simplify(
                    sp.sympify(
                        e["symbolic_identities"]["metric_trace_factor"],
                        locals={"alpha":a,"beta":b}
                    )-expected
                )==0
            )

            # Independent 1D gauge-current Noether check.
            ar,bi,da,db,Ax,q=sp.symbols(
                "ar bi da db Ax q"
            )
            d2a,d2b,dAx=sp.symbols("d2a d2b dAx")
            u=da+q*Ax*bi
            v=db-q*Ax*ar
            j=q*(bi*u-ar*v)
            Dj=(
                sp.diff(j,ar)*da
                +sp.diff(j,bi)*db
                +sp.diff(j,da)*d2a
                +sp.diff(j,db)*d2b
                +sp.diff(j,Ax)*dAx
            )
            Du=d2a+q*(dAx*bi+Ax*db)
            Dv=d2b-q*(dAx*ar+Ax*da)
            Ea=q*Ax*v+Du
            Eb=-q*Ax*u+Dv
            check(
                "independent U1 current identity",
                sp.simplify(
                    Dj-q*(bi*Ea-ar*Eb)
                )==0
            )
            check(
                "reported local Ward identity",
                e["symbolic_identities"][
                    "charged_scalar_one_coordinate_Ward_residual"
                ]=="0"
            )

            eps,R=sp.symbols("eps R",positive=True)
            check(
                "independent positive point-charge divergence",
                sp.limit(1/eps-1/R,eps,0,dir="+")==sp.oo
                and e["symbolic_identities"][
                    "point_charge_self_energy_limit"
                ]=="POSITIVE_INFINITY"
            )
            check(
                "topological direct stress distinction",
                e["symbolic_identities"][
                    "bare_fixed_theta_direct_Hilbert_residual"
                ]=="0"
                and e["symbolic_identities"]["scope"].startswith(
                    "EXACT_SYMBOLIC_LOCAL"
                )
            )
            state="PASS_SCOPED_ACTION_ATLAS_NOT_PHYSICAL_MODEL"
        else:
            check(
                "interrupted run not promoted",
                science["qualified_physical_survivors"]==0
                and science["complete_covariant_action"]=="NOT_DERIVED"
            )
            state="PASS_INTEGRITY_INCOMPLETE_RUN"

        result={
            "program":"GRAVITY2-02_INDEPENDENT_VERIFIER",
            "run_id":directory.name,
            "status":state,
            "checks":checks,
            "science_sha256":digest(
                directory/"science.json"
            ),
            "complete_gravitational_action":"NOT_DERIVED",
            "qualified_survivors":0,
        }

    except Exception as exc:
        result={
            "program":"GRAVITY2-02_INDEPENDENT_VERIFIER",
            "run_id":directory.name,
            "status":"HOLD",
            "checks":checks,
            "error":repr(exc),
            "qualified_survivors":0,
        }

    path=directory/"verification.json"
    if path.exists():
        if json.loads(path.read_text())!=result:
            print("VERIFICATION_RECHECK_DIFFERS_NO_OVERWRITE")
            return 3
    else:
        atomic_json(path,result)
        atomic_text(
            directory/"verification.sha256",
            digest(path)+"  verification.json\n"
        )

    print("GRAVITY2_02_VERIFY="+result["status"])
    print(
        "CHECKS="
        +str(sum(checks.values()))
        +"/"+str(len(checks))
    )
    print("VERIFICATION_SHA256="+digest(path))
    return 0 if result.get("status") == "PASS_SCOPED_ACTION_ATLAS_NOT_PHYSICAL_MODEL" else 3
