"""Independent R7 finite-volume and energy-ratio verifier; no R7 science import."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import sys
import numpy as np
from scipy.sparse import diags
ROOT=Path(__file__).resolve().parents[2]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bump(x,R):
    result=np.zeros_like(x)
    mask=abs(x)<R
    result[mask]=np.exp(1.-1./(1.-(x[mask]/R)**2))
    return result


def verify(path):
    from antigravity_research.ph16.ph16_04_joint_stationary import CoulombSource,Spec,JointAction,Settings
    path=Path(path).resolve()
    assert path.parent==ROOT/'results/data'
    assert re.fullmatch(r'gamma1_00r7_\d{8}T\d{12}Z\.json',path.name)
    assert path.with_name(path.name+'.sha256').read_text().strip()==sha(path)+'  '+path.name
    result=json.loads(path.read_text())
    assert result['classification']=='PASS_WEIGHTED_FV_SMOOTH_PROBE_TREND_NATIVE_MISMATCH_OPEN'
    assert len(result['parent_hashes'])==6
    for rec in result['parent_hashes'].values():
        assert sha(ROOT/rec['path'])==rec['expected']==rec['actual']
    for rel,digest in result['source_hashes'].items():
        assert sha(ROOT/rel)==digest
    survey=result['science']['mesh_sweep']
    assert [m['nr'] for m in survey]==[8,12,16,20]
    for mdoc in survey:
        nr=mdoc['nr']
        m=CoulombSource(Spec(nr=nr,L=12.),self_order=8)
        j=JointAction(m,Settings(nr=nr,L=12.))
        W=diags(m.w)
        # Independent sparse finite-volume reconstruction from original operators.
        X=(W@m.L).toarray()
        Y=(W@(m.L+diags(1./m.rho**2))).toarray()
        for sector,K,G,L in (('X',j.Kx,m.wkernel,X),('Y',j.Ky,m.wmagkernel,Y)):
            assert np.linalg.norm(K@G-W.toarray())/np.linalg.norm(W.toarray())<1e-10
            mask=np.arange(m.cells).reshape(nr,2*nr)[1:-1,1:-1].ravel()
            for label,kk,ll in (('whole_fit',K,L),('interior_fit',K[np.ix_(mask,mask)],L[np.ix_(mask,mask)])):
                scale=float(np.sum(kk*ll)/np.sum(ll*ll))
                mismatch=float(np.linalg.norm(kk-scale*ll)/np.linalg.norm(kk))
                stored=mdoc['Green_vs_weighted_FV'][sector][label]
                assert np.allclose([scale,mismatch],[stored['scale'],stored['relative_frobenius_mismatch']],rtol=1e-10,atol=1e-12)
            for name,rr,zz,z0 in [('compact_center',7.,7.,0.),('compact_shifted',6.,5.,2.),('compact_wide',9.,8.,-1.)]:
                v=bump(m.rho,rr)*bump(m.z-z0,zz)
                if sector=='Y':v=m.rho*v
                ratio=float((v@K@v)/(v@L@v))
                assert np.isclose(ratio,mdoc['compact_smooth_energy_K_over_FV'][sector][name],rtol=2e-11,atol=1e-12)
        # Reproduce both on-background measurements without another PH16 solve.
        if nr==12:
            p=ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz'
            with np.load(p,allow_pickle=False) as f:
                for sector,K,L,v in [('X',j.Kx,X,f['A_X']),('Y',j.Ky,Y,f['A_Y'])]:
                    Kv=K@v;Lv=L@v
                    scale=float(np.dot(Kv,Lv)/np.dot(Lv,Lv))
                    error=float(np.linalg.norm(Kv-scale*Lv)/np.linalg.norm(Kv))
                    stored=mdoc['native_R3_background'][sector]
                    assert np.isclose(error,stored['on_field_best_scaled_gradient_mismatch'],rtol=1e-10,atol=1e-12)
                    assert error>.7
    for sector in ('X','Y'):
        for probe in ('compact_center','compact_shifted','compact_wide'):
            gaps=[abs(m['compact_smooth_energy_K_over_FV'][sector][probe]-1) for m in survey]
            assert all(gaps[i+1]<gaps[i] for i in range(3))
    assert result['science']['scope']['continuum_exterior']=='NOT_CERTIFIED'
    assert result['science']['scope']['Schur_boundary_DtN']=='NOT_CONSTRUCTED'
    assert result['GAMMA1_01_authorized'] is False
    assert result['006D_replaced'] is False
    assert result['whole_craft_up']=='NOT_DERIVED'
    print('GAMMA1_00R7_INDEPENDENT_VERIFICATION=PASS')
    print('12_L12_X_WEIGHTED_FV_INTERIOR_MISMATCH='+str(survey[1]['Green_vs_weighted_FV']['X']['interior_fit']['relative_frobenius_mismatch']))
    print('12_L12_Y_WEIGHTED_FV_INTERIOR_MISMATCH='+str(survey[1]['Green_vs_weighted_FV']['Y']['interior_fit']['relative_frobenius_mismatch']))
    print('20_L12_X_COMPACT_CENTER_ENERGY_RATIO='+str(survey[-1]['compact_smooth_energy_K_over_FV']['X']['compact_center']))
    print('20_L12_Y_COMPACT_CENTER_ENERGY_RATIO='+str(survey[-1]['compact_smooth_energy_K_over_FV']['Y']['compact_center']))
    print('RESULT_SHA256='+sha(path))

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: verify_gamma1_00r7.py exact-result.json')
    verify(sys.argv[1])
