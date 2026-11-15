"""Execute PH13-MEGA same-action / source / recoil audit.

Produces a unique immutable JSON result. Passes do not certify an engine.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys

from antigravity_research.agminer import (
    hook17_ph13_integrated_go_no_go as ph13
)


def main():
    root = Path.cwd()
    result = ph13.run(root)
    stamp = datetime.now(timezone.utc)

    result['execution'] = {
        'timestamp_utc': stamp.isoformat(),
        'python': sys.version,
        'platform': platform.platform(),
        'module_sha256': sha256(
            Path(ph13.__file__).read_bytes()
        ).hexdigest(),
        'runner_sha256': sha256(
            Path(__file__).read_bytes()
        ).hexdigest()
    }

    dest = root/'results/data'/(
        '032h17_ph13_integrated_go_no_go_'
        +stamp.strftime('%Y%m%dT%H%M%S%fZ')
        +'.json'
    )

    dest.parent.mkdir(
        parents=True,exist_ok=True
    )

    with dest.open(
        'x',encoding='utf-8'
    ) as stream:
        json.dump(
            result,stream,
            sort_keys=True,
            indent=2,
            allow_nan=False
        )
        stream.write('\n')

    print('RUN='+result['branch'])
    print('PROVENANCE='+result['gates']['P0_PROVENANCE'])

    radial = result[
        'independent_radial_static_fixed_charge'
    ]

    print(
        'PH12_INDEPENDENT_OMEGA='
        +str(radial['bvp_omega'])
    )

    print(
        'SOURCE_GAUSS_RELOADED_REL='
        +str(
            radial['finite_volume'][
                'Gauss_flux_relative_error'
            ]
        )
    )

    print(
        'FIXED_CHARGE_FINITE_BASIS_HESSIAN_MIN='
        +str(radial['hessian_min'])
    )

    print(
        'FIXED_CHARGE_GRADIENT='
        +str(radial['gradient'])
    )

    print(
        'FIXED_CHARGE_SUBSPACE_NEGATIVE_DIRECTIONS='
        +str(radial['negative_eigenvalues'])
    )

    joint = result[
        'joint_scalar_carrier_principal_gate'
    ]

    print(
        'JOINT_SCALAR_CARRIER='
        +str(
            joint[
                'source_center_conditional_joint_hessian'
            ]
        )
    )

    print(
        'JOINT_FROZEN_PASS_BUT_FULL_FAIL_CONTROL='
        +str(
            joint[
                'constructed_frozen_positive_joint_negative'
            ]
        )
    )

    print(
        'TRACE_INDUCED_SECOND_CARRIER='
        'LEADING_ORDER_OFFSHELL_COMPOSITE'
    )

    induced = result[
        'PH12_pair_linear_trace_induced_Y'
    ]

    for n,case in induced['resolution_cases'].items():
        print(
            'INDUCED_Y_N'+n
            +'_B2='+str(case['Y_B2_integral'])
            +' ABS_LOCAL_P='+str(case['L1_local_P'])
            +' SIGNED_VOLUME_P='
            +str(case['signed_integral_P'])
        )

    print(
        'PH7_MOMENTUM_LEDGER='
        +str(
            result['whole_spacecraft_momentum_theorem']
        )
    )

    for name,status in result['gates'].items():
        print('GATE_'+name+'='+status)

    print('VERDICT='+result['verdict'])
    print('JSON='+str(dest))

    return (
        0 if result['gates']['P0_PROVENANCE']=='PASS'
        else 2
    )


if __name__=='__main__':
    raise SystemExit(main())
