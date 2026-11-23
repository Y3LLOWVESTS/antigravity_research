"""Independent full-inverse audit of toy response; not Einstein gravity."""
import math
import numpy as np
from .response_v7 import matrices, VERDICT


def review(spec, r):
    a,b,c,k,j,t,d,eig = matrices(spec)
    inv = np.linalg.inv(k)
    z = inv @ (j+d*t)
    f = j+d*t
    s = c-b.T @ np.linalg.inv(a) @ b
    checks = {
        'status_scoped':r['status']==VERDICT,
        'inverse_identity':np.max(abs(k@inv-np.eye(len(k)))) < 1e-9,
        'hessian_healthy':eig[0] > 1e-8,
        'schur_healthy':np.linalg.eigvalsh(s)[0] > 1e-8,
        'loaded_source_response':np.max(abs(z[len(a):]-r['loaded_field_response_toy'])) < 1e-9,
        'energy':math.isclose(r['stationary_energy_toy'],-.5*float(f@z),abs_tol=1e-9),
        'source_load_force':math.isclose(r['craft_coordinate_force_toy'],float(t@z),abs_tol=1e-9),
        'equal_opposite_coordinate_force':math.isclose(r['earth_coordinate_force_toy'],-float(t@z),abs_tol=1e-9),
        'stationarity':r['stationary_residual'] < 1e-9,
        'schur_reconstruction':r['schur_error'] < 1e-9,
        'translation_derivative':r['derivative_fd_error'] < 1e-7,
        'not_Einstein':r['Einstein_metric_variation']=='NOT_DERIVED',
        'not_a_real_source':r['finite_source_realization']=='NOT_DERIVED',
        'no_Earth_craft_promotion':r['Earth_down_craft_up']=='NOT_DERIVED' and r['whole_craft_lift']=='NOT_DERIVED',
        'no_energy_promotion':r['complete_SI_energy']=='NOT_CERTIFIED' and r['gravitational_survivors']==0,
    }
    if not all(isinstance(v,(bool,np.bool_)) and v for v in checks.values()):
        raise ValueError('INDEPENDENT_TOY_REVIEW_HOLD')
    return {name:bool(value) for name,value in checks.items()}
