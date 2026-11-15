"""PH11 execution: exact universal matter chain rule plus support debt."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys

from antigravity_research.agminer import (
    hook17_ph11_universal_metric_support_gate as ph11
)


def main():
    root = Path.cwd()
    result = ph11.run(root)
    now = datetime.now(timezone.utc)

    result['execution'] = {
        'utc': now.isoformat(),
        'python': sys.version,
        'platform': platform.platform(),
        'module_sha256':
            sha256(Path(ph11.__file__).read_bytes()).hexdigest(),
        'simulation_sha256':
            sha256(Path(__file__).read_bytes()).hexdigest(),
    }

    dest = root/'results/data'/(
        '032h17_ph11_universal_metric_support_'
        + now.strftime('%Y%m%dT%H%M%S%fZ')
        + '.json'
    )

    dest.parent.mkdir(parents=True, exist_ok=True)

    with dest.open('x', encoding='utf-8') as f:
        json.dump(
            result, f, sort_keys=True,
            indent=2, allow_nan=False
        )
        f.write('\n')

    print('RUN=' + result['branch'])
    print('PROVENANCE=' + result['gates']['P0_PROVENANCE'])

    for item in result['well_support_debt']['modes']:
        print(
            'WELL_L=' + str(item['l'])
            + ' PAIR_RADIAL_TRACTION='
            + str(item['integrated_radial_traction_pair'])
            + ' FD_ERROR='
            + str(item['relative_derivative_disagreement'])
        )

    print(
        'TOTAL_RADIAL_TRACTION='
        + str(
            result['well_support_debt'][
                'total_integrated_radial_traction_magnitude'
            ]
        )
    )

    a = result['ph10_matter_and_reaction_audit']

    print(
        'PH10_FLAT_SOURCE_TRACE_INTEGRAL='
        + str(a['loaded_stress_trace_integral_at_Omega_1'])
    )
    print(
        'PH10_DISCRETE_CURRENT_DIVERGENCE_REL='
        + str(a['source_current_relative_divergence'])
    )
    print('PH10_SOURCE_KG_X=' + str(a['loaded_scalar_EOM_X']))
    print('PH10_SOURCE_KG_Y=' + str(a['loaded_scalar_EOM_Y']))

    for name, state in result['gates'].items():
        print('GATE_' + name + '=' + state)

    print('VERDICT=' + result['verdict'])
    print('JSON=' + str(dest))

    return (
        0 if result['gates']['P0_PROVENANCE'] == 'PASS'
        else 2
    )


if __name__ == '__main__':
    raise SystemExit(main())
