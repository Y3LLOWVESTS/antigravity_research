"""Independent GRAVITY2-08 theorem and saved-field verification.

Reconstructs Gauss current and all three Euler derivatives without calling
bridge08_core; independent finite difference of an explicit augmented action.
PASS only establishes a periodic single-sign-charge obstruction, never an
exterior gravitational no-go or a physically sourced vehicle.
"""
from __future__ import annotations

import json
import numpy as np
import sympy as sp

from .engine import ROOT, atomic_json, atomic_text, digest
from . import bridge08 as run
from . import bridge07_core as old


def D(a,h,axis):
    return (np.roll(a,-1,axis=axis)-np.roll(a,1,axis=axis))/(2*h)


def independent(a,f,b,h):
    ax,az=D(a,h,0),D(a,h,1)
    bx,bz=D(b,h,0),D(b,h,1)
    fx,fz=D(f,h,0),D(f,h,1)
    P=ax*bz-az*bx
    sig=.08*P-.005*P*P
    w=np.exp(2*sig)
    z=np.exp(4*sig)
    Om=1.25-.4*a
    K=Om**2*f*f-fx**2-fz**2
    V=.8*f*f/2+.4*f**4/4
    Pi=(w*K-4*z*V)*(.08-.01*P)
    rho=.4*w*Om*f*f

    Ea=-rho-D(ax+Pi*bz,h,0)-D(az-Pi*bx,h,1)
    Ef=w*Om**2*f-z*(.8*f+.4*f**3)+D(w*fx,h,0)+D(w*fz,h,1)
    Eb=D(bx,h,0)+D(bz,h,1)+D(Pi*az,h,0)-D(Pi*ax,h,1)
    parent=float(h*h*np.sum(-.5*(bx**2+bz**2)+.5*w*K-z*V))
    augmented=float(parent+.5*h*h*np.sum(ax**2+az**2))
    return {'rho':rho,'Ea':Ea,'Ef':Ef,'Eb':Eb,
            'parent_action':parent,'augmented_action':augmented,
            'maxwell_term':augmented-parent,'Omega':Om,'w':w,
            'div':D(ax+Pi*bz,h,0)+D(az-Pi*bx,h,1)}


def independent_symbolic():
    a,ax,az,bx,bz,f,fx,fz,om,q,alpha,beta,m2,lam = sp.symbols(
        'a ax az bx bz f fx fz om q alpha beta m2 lam',real=True)
    P=ax*bz-az*bx
    sig=alpha*P-beta*P*P
    w=sp.exp(2*sig)
    z=sp.exp(4*sig)
    Om=om-q*a
    K=Om**2*f*f-fx*fx-fz*fz
    V=m2*f*f/2+lam*f**4/4
    L=(ax*ax+az*az-bx*bx-bz*bz)/2+w*K/2-z*V
    Pi=(w*K-4*z*V)*(alpha-2*beta*P)

    assert sp.simplify(sp.diff(L,a)+q*w*Om*f*f)==0
    assert sp.simplify(sp.diff(L,ax)-(ax+Pi*bz))==0
    assert sp.simplify(sp.diff(L,az)-(az-Pi*bx))==0
    assert sp.simplify(sp.diff(L,bx)-(-bx-Pi*az))==0
    assert sp.simplify(sp.diff(L,bz)-(-bz+Pi*ax))==0
    assert sp.simplify(sp.diff(L,fx)+w*fx)==0

    c=sp.symbols('c',real=True)
    assert sp.simplify(
        L.subs({a:a+c,om:om+q*c},simultaneous=True)-L
    )==0
    return True


def finite_differences(a,f,b,h):
    n=a.shape[0]
    x=np.arange(n)*h
    X,Z=np.meshgrid(x,x,indexing='ij')
    b_off=b+.035*np.sin(X+2*Z)+.017*np.cos(2*X-Z)
    data=independent(a,f,b_off,h)
    eps=2e-5
    errors={}
    signals={}

    for key,field in [('a',a),('f',f),('b',b_off)]:
        d=np.zeros_like(field)
        d[3,4]=1

        def calc(shift):
            A=a+shift*d if key=='a' else a
            F=f+shift*d if key=='f' else f
            B=b_off+shift*d if key=='b' else b_off
            return independent(A,F,B,h)['augmented_action']

        numeric=(calc(eps)-calc(-eps))/(2*eps)
        predicted=float(h*h*data['E'+key if key!='a' else 'Ea'][3,4])
        errors[key]=float(abs(numeric-predicted))
        signals[key]=float(abs(predicted))
    return errors,signals


def verify(folder):
    checks={}

    def gate(k,ok):
        checks[k]=bool(ok)
        if not ok:
            raise AssertionError(k)

    try:
        man=json.loads((folder/'manifest.json').read_text())
        sci=json.loads((folder/'science.json').read_text())
        ledger=dict(
            line.split('  ',1)[::-1]
            for line in (folder/'hashes.sha256').read_text().splitlines()
        )

        for name in ('manifest.json','science.json'):
            gate('sha '+name,ledger[name]==digest(folder/name))

        gate('run linkage',man['run_id']==sci['run_id']==folder.name)
        gate('producer sha',man['source_hashes']==run.source_hashes())
        gate('parent hashes',sci['parents']==run.parents() and sci['parents']['all_match'])
        gate('L0 bounded',man['level']=='L0' and man['workers']==1 and 0<man['seconds_ceiling']<=30)
        gate('watchdog',sci['resource']['watchdog']=='SOFT_PSUTIL_PROCESS')
        gate('old sources preserved',man['no_prior_source_modification'] is True and man['AGMINER']=='HASHED_NO_EXECUTION')
        gate('execution',sci['execution_status']=='COMPLETED')
        gate('no fake source',sci['physical_finite_source']=='NOT_ESTABLISHED' and sci['external_neutralizer']=='NOT_INTRODUCED')
        gate('no Einstein lift',sci['Einstein_gravity']=='NOT_SOLVED' and sci['whole_craft_lift']=='NOT_DERIVED')
        gate('energy unresolved',sci['complete_energy_SI']=='NOT_CERTIFIED' and not sci['006D_replaced'])
        gate('no level promotion',sci['L2_authorized'] is False and sci['qualified_physical_survivors']==0)
        gate('regression scope',sci['full_repository_regression']=='NOT_RUN')

        ev=sci['evidence']
        gate('scoped verdict',ev['decision']=='PARENT_07_X_GAUSS_ZERO_MODE_OBSTRUCTED_NO_COMPENSATOR')
        gate('separate action erratum',ev['parent_action_erratum']=='ACTUAL_07_ACTION_OMITS_X_MAXWELL_DESPITE_SCIENCE_L_SUMMARY')
        gate('no offshell promotion',ev['physical_survivors']==0 and ev['L2_source_solve_authorized'] is False)
        gate('exact symbolic independent',independent_symbolic())
        gate('four grids',tuple(x['n'] for x in ev['rows'])==(9,15,23,31))

        prior=json.loads((ROOT/run.PARENT_DIR/'science.json').read_text())
        gate('prior action *description* mismatch acknowledged','1/2|grad a|^2' in prior['evidence']['L'])

        with np.load(ROOT/run.PARENT_DIR/'fields.npz',allow_pickle=False) as ar:
            gate('archive field names',set(ar.files)=={
                f'{key}_{n}' for key in 'afb' for n in (9,15,23,31)
            })
            qvalues=[]

            for row in ev['rows']:
                n=row['n']
                h=2*np.pi/n
                a,f,b=[np.asarray(ar[f'{key}_{n}'],float) for key in 'afb']
                gate(f'finite fields {n}',all(
                    z.shape==(n,n) and np.isfinite(z).all()
                    for z in (a,f,b)
                ))

                z=independent(a,f,b,h)
                charge=float(h*h*np.sum(z['rho']))
                qvalues.append(charge)

                gate(f'positive charge {n}',
                    z['rho'].min()>.17 and z['Omega'].min()>1.1
                    and z['w'].min()>0 and charge>16
                )

                gate(f'Gauss integral {n}',
                    abs(charge-row['charge_integral_canonical'])<1e-10
                    and abs(h*h*np.sum(z['Ea'])+charge)<1e-10
                )

                gate(f'periodic divergence {n}',
                    abs(h*h*np.sum(z['div']))<1e-10
                )

                for field,key in [
                    ('Ea','X_euler_rms'),
                    ('Ef','scalar_euler_rms'),
                    ('Eb','Y_euler_rms'),
                ]:
                    rms=float(np.sqrt(np.mean(z[field]**2)))
                    gate(f'{field} rms {n}',abs(rms-row[key])<1e-10)

                gate(f'Y only stationary {n}',
                    np.sqrt(np.mean(z['Eb']**2))<1e-9
                    and np.sqrt(np.mean(z['Ea']**2))>.4
                    and np.sqrt(np.mean(z['Ef']**2))>.4
                )

                gate(f'action parent numeric {n}',
                    abs(z['parent_action']-row['parent_action_value'])<1e-9
                )

                gate(f'action Maxwell correction {n}',
                    z['maxwell_term']>.5
                    and abs(
                        z['maxwell_term']
                        -row['X_maxwell_term_missing_in_parent_action']
                    )<1e-9
                )

                gate(f'parent actual source action {n}',
                    abs(old.action(b,a,f,h)-z['parent_action'])<1e-9
                )

                gate(f'unphysical uniform neutralizer not enough {n}',
                    np.sqrt(np.mean(
                        (z['Ea']+np.mean(z['rho']))**2
                    ))>.1
                )

                if n==15:
                    errors,signals=finite_differences(a,f,b,h)
                    for key in ('a','f','b'):
                        gate(
                            f'finite-difference action gradient {key}',
                            errors[key]<5e-7 and signals[key]>1e-6
                        )

                    wrong=np.mean(-z['div'])
                    gate('omitted charge false Gauss null control',
                        abs(wrong)<1e-12 and np.mean(z['rho'])>.35
                    )

            gate('grid sensitivity no continuum claim',
                abs(qvalues[-1]-qvalues[-2])/qvalues[-1]<1e-5
            )

        report={
            'program':'GRAVITY2-08_INDEPENDENT_SOURCE_GAUSS',
            'run_id':folder.name,
            'status':'PASS_SCOPED_PERIODIC_X_GAUSS_OBSTRUCTION_NO_LIFT',
            'science_sha256':digest(folder/'science.json'),
            'checks':checks,
            'physical_source':'NOT_ESTABLISHED',
            'whole_craft_lift':'NOT_DERIVED',
        }

    except Exception as exc:
        report={
            'program':'GRAVITY2-08_INDEPENDENT_SOURCE_GAUSS',
            'run_id':folder.name,
            'status':'HOLD',
            'checks':checks,
            'error':repr(exc),
            'whole_craft_lift':'NOT_DERIVED',
        }

    dest=folder/'verification.json'

    if dest.exists():
        if json.loads(dest.read_text())!=report:
            print('GRAVITY2_08_REVERIFY_DIFFERENCE_NO_OVERWRITE')
            return 3
    else:
        atomic_json(dest,report)
        atomic_text(
            folder/'verification.sha256',
            digest(dest)+'  verification.json\n'
        )

    print('GRAVITY2_08_VERIFY='+report['status'])
    print('CHECKS='+str(sum(checks.values()))+'/'+str(len(checks)))
    if 'error' in report:
        print('ERROR='+report['error'])
    print('VERIFICATION_SHA256='+digest(dest))

    return (
        0 if report['status']
        =='PASS_SCOPED_PERIODIC_X_GAUSS_OBSTRUCTION_NO_LIFT'
        else 3
    )
