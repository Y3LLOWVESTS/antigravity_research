"""Common finite-dimensional quadratic action: toy-only reciprocity test."""
import numpy as np

SCHEMA = 'gravity2.toy_response.v7'
VERDICT = 'PASS_SCOPED_RECIPROCAL_TOY_NO_GRAVITY'


def example():
    return {'schema': SCHEMA, 'source_kind': 'PRESCRIBED_TOY',
            'units': 'ABSTRACT_CANONICAL',
            'A': [[3., 0.], [0., 4.]], 'B': [[.4], [.25]], 'C': [[2.]],
            'j_source': [1., .4], 'j_field': [.3],
            'translation_source': [.2, -.1], 'translation_field': [.5],
            'relative_displacement': .125}


def matrices(spec):
    if not isinstance(spec, dict) or set(spec) != set(example()):
        raise ValueError('TOY_ACTION_SCHEMA_HOLD')
    if (spec['schema'], spec['source_kind'], spec['units']) != (
            SCHEMA, 'PRESCRIBED_TOY', 'ABSTRACT_CANONICAL'):
        raise ValueError('PHYSICAL_SOURCE_OR_SI_NOT_DERIVED')
    a, b, c = (np.asarray(spec[k], dtype=float) for k in ('A', 'B', 'C'))
    if (a.ndim != 2 or b.ndim != 2 or c.ndim != 2
            or a.shape[0] not in range(1, 7)
            or c.shape[0] not in range(1, 7)
            or a.shape[1] != a.shape[0] or c.shape[1] != c.shape[0]
            or b.shape != (len(a), len(c))):
        raise ValueError('BOUNDED_TOY_DIMENSIONS_HOLD')
    j = np.r_[np.asarray(spec['j_source'], dtype=float),
              np.asarray(spec['j_field'], dtype=float)]
    t = np.r_[np.asarray(spec['translation_source'], dtype=float),
              np.asarray(spec['translation_field'], dtype=float)]
    if j.shape != (len(a) + len(c),) or t.shape != j.shape:
        raise ValueError('TOY_VECTOR_SHAPE_HOLD')
    if not np.allclose(a, a.T, atol=1e-12, rtol=0) or not np.allclose(c, c.T, atol=1e-12, rtol=0):
        raise ValueError('NO_COMMON_QUADRATIC_ACTION')
    k = np.block([[a, b], [b.T, c]])
    d = spec['relative_displacement']
    if (type(d) not in (float, int) or not np.isfinite(d) or abs(d) > 100
            or not all(np.isfinite(x).all() and np.max(np.abs(x)) <= 1e5 for x in (k, j, t))):
        raise ValueError('NONFINITE_OR_UNBOUNDED_TOY')
    eigen = np.linalg.eigvalsh(k)
    if eigen[0] <= 1e-8 or eigen[-1]/eigen[0] > 1e8:
        raise ValueError('UNHEALTHY_TOY_MODE')
    return a, b, c, k, j, t, d, eigen


def compute(spec):
    a, b, c, k, j, t, d, eig = matrices(spec)
    f = j + d*t
    z = np.linalg.solve(k, f)
    s = c - b.T @ np.linalg.solve(a, b)
    zg = np.linalg.solve(s, f[len(a):] - b.T @ np.linalg.solve(a, f[:len(a)]))
    zs = np.linalg.solve(a, f[:len(a)] - b @ zg)
    residual = float(np.max(np.abs(k @ z-f)))
    schur_error = float(np.max(np.abs(z-np.r_[zs, zg])))

    def on_shell(x):
        v = j+x*t
        return -0.5*float(v @ np.linalg.solve(k,v))

    h = 1e-5*max(1,abs(d))
    force = float(t @ z)
    fd = -(on_shell(d+h)-on_shell(d-h))/(2*h)
    if max(residual,schur_error) > 1e-9 or abs(fd-force) > 1e-7*max(1,abs(force)):
        raise ValueError('TOY_SCHUR_OR_ENERGY_IDENTITY_HOLD')
    frozen = np.linalg.solve(c, f[len(a):]-b.T @ np.linalg.solve(a,f[:len(a)]))
    return {
        'status': VERDICT, 'model': 'FINITE_QUADRATIC_TOY',
        'assumption': 'PRESCRIBED_SOURCE_RELATIVE_COORDINATE',
        'min_hessian_eigenvalue':float(eig[0]),
        'min_schur_eigenvalue':float(np.linalg.eigvalsh(s)[0]),
        'loaded_field_response_toy':zg.tolist(),
        'frozen_field_response_toy':frozen.tolist(),
        'stationary_energy_toy':on_shell(d),
        'craft_coordinate_force_toy':force,
        'earth_coordinate_force_toy':-force,
        'schur_error':schur_error, 'stationary_residual':residual,
        'derivative_fd_error':abs(fd-force),
        'Einstein_metric_variation':'NOT_DERIVED',
        'finite_source_realization':'NOT_DERIVED',
        'Earth_down_craft_up':'NOT_DERIVED',
        'whole_craft_lift':'NOT_DERIVED',
        'complete_SI_energy':'NOT_CERTIFIED',
        'gravitational_survivors':0,
    }
