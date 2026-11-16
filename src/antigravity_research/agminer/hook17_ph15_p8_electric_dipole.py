"""PH15-P8: neutral electric-dipole X source from a distinct scalar action.

Model (fixed Minkowski, -+++, all quantities canonical):
 L = -1/4 F_X**2 + sum_i[-|D_X psi_i|**2-U_i(|psi_i|**2)]
     - g |psi_+|**2 |psi_-|**2,  q=(+e,-e),
 U(s)=s-2s**2+2s**3.

The positive cross-coupling g is NEW source physics relative to PH14-P7;
no winding or imposed source-current is used. The stationary X-source fields
and individual omega_i are solved together at N_i=N using a fixed-charge
energy variational formulation, in a finite cylindrical Dirichlet box.
The Y field is only the linear induced field at F_Y=0 via lambda=-2 alpha
(K+2U_total). It is NOT a reciprocal 2-U(1) solution, a physical metric,
GR, a spacecraft force, or an SI energy model. Full nonaxisymmetric mode
health, nonlinear field reciprocity and free-space exterior remain open.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh
from scipy.sparse import lil_matrix, diags, eye, kron
from scipy.sparse.linalg import spsolve
from scipy.ndimage import shift as ndi_shift


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@dataclass(frozen=True)
class Spec:
    nr: int=18
    L: float=12.
    N: float=400.
    e: float=.12
    g: float=.20
    seed_separation: float=3.


class Dipole:
    """Stationary two-complex-scalar/electrostatic X finite-volume solver."""
    def __init__(self,s):
        self.s=s
        if s.nr<8 or s.L<=0 or s.N<=0 or s.e<=0 or s.g<0:
            raise ValueError('Invalid source specification')
        self.nr=s.nr
        self.nz=2*s.nr
        self.h=s.L/s.nr
        rr=(np.arange(self.nr)+.5)*self.h
        zz=(np.arange(self.nz)+.5)*self.h-s.L
        r,z=np.meshgrid(rr,zz,indexing='ij')
        self.rho=r.ravel()
        self.z=z.ravel()
        self.w=2*np.pi*self.rho*self.h**2
        self.cells=self.nr*self.nz
        self.q=np.array([s.e,-s.e])
        R=lil_matrix((self.nr,self.nr));Z=lil_matrix((self.nz,self.nz))
        for i in range(self.nr):
            d=0.
            if i>0:
                a=(rr[i]-.5*self.h)/(rr[i]*self.h**2)
                R[i,i-1]=-a;d+=a
            if i<self.nr-1:
                a=(rr[i]+.5*self.h)/(rr[i]*self.h**2)
                R[i,i+1]=-a;d+=a
            else:
                d+=2*(rr[i]+.5*self.h)/(rr[i]*self.h**2)
            R[i,i]=d
        for j in range(self.nz):
            d=0.
            if j>0:Z[j,j-1]=-1/self.h**2;d+=1/self.h**2
            else:d+=2/self.h**2
            if j<self.nz-1:Z[j,j+1]=-1/self.h**2;d+=1/self.h**2
            else:d+=2/self.h**2
            Z[j,j]=d
        self.L=(kron(R.tocsr(),eye(self.nz))+kron(eye(self.nr),Z.tocsr())).tocsr()

    def seed(self,sep=None):
        if sep is None:sep=self.s.seed_separation
        r2=self.rho**2
        Fs=[]
        for sign in (1,-1):
            f=np.exp(-(r2+(self.z-sign*sep/2)**2)/(2*2.6**2))
            f*=np.sqrt(self.s.N/(1.6*np.dot(self.w,f*f)))
            Fs.append(f)
        return np.array(Fs)

    def fields(self,F):
        f2=F*F
        I=f2@self.w
        if min(I)<1e-12:raise ArithmeticError('Vanishing scalar norm')
        D=(self.L+diags(2*(self.q**2@f2))).tocsc()
        omega=self.s.N/(2*I)
        for _ in range(80):
            A=spsolve(D,2*((self.q*omega)@f2))
            nxt=(self.s.N/2+self.q*(f2@(self.w*A)))/I
            if np.max(abs(nxt-omega))<2e-12:
                omega=nxt
                break
            omega=nxt
        else:raise ArithmeticError('Gauss/Noether fixed point did not converge')
        A=spsolve(D,2*((self.q*omega)@f2))
        W=omega[:,None]-self.q[:,None]*A
        return A,W,omega

    def energy(self,y,details=False):
        F=np.asarray(y).reshape(2,self.cells)/np.sqrt(self.w)
        A,W,omega=self.fields(F)
        f2=F*F
        Ee=.5*np.dot(self.w*A,self.L@A)
        E=Ee+self.s.g*np.dot(self.w,f2[0]*f2[1])
        gradient=[];equations=[]
        for i in (0,1):
            f=F[i];s=f2[i]
            U=s-2*s*s+2*s**3
            E+=np.dot(self.w,W[i]*W[i]*s+f*(self.L@f)+U)
            residual=self.L@f+(1-W[i]**2-4*s+6*s*s+self.s.g*f2[1-i])*f
            gradient.append(2*np.sqrt(self.w)*residual)
            equations.append(float(np.sqrt(np.dot(self.w,residual**2))))
        grad=np.concatenate(gradient)
        if not details:return float(E),grad
        nums=2*(W*f2)@self.w
        charge=2*((self.q[:,None]*W*f2).sum(axis=0))
        gauss=self.L@A-charge
        centers=[float(np.dot(self.w*self.z,f2[i])/np.dot(self.w,f2[i])) for i in (0,1)]
        R=np.sqrt(self.rho**2+self.z**2)
        outer=R>(.8*self.s.L)
        total_density=f2.sum(axis=0)
        tail=float(np.dot(self.w*outer,total_density)/np.dot(self.w,total_density))
        dipole=float(np.dot(self.w*self.z,charge))
        return {
            'energy_CANONICAL_NOT_J':float(E),'electrostatic_energy':float(Ee),
            'individual_Noether':nums.tolist(),'net_X_charge':float(self.q@nums),
            'charge_density_L2':float(np.sqrt(np.dot(self.w,charge**2))),
            'gauss_L2':float(np.linalg.norm(gauss)),
            'scalar_EOM_weighted_L2':equations,
            'omega':omega.tolist(),'centers':centers,
            'source_separation':float(centers[0]-centers[1]),
            'electric_dipole_X':dipole,
            'outer_80percent_spherical_tail_fraction':tail,
            'domain':'FINITE_CYLINDRICAL_DIRICHLET',
        },{'F':F,'A':A,'W':W,'omega':omega,'charge':charge}

    def solve(self,steps=400):
        rootw=np.sqrt(self.w)
        seed=(self.seed()*rootw).ravel()
        opt=minimize(self.energy,seed,jac=True,method='L-BFGS-B',
            bounds=[(0,None)]*seed.size,
            options={'maxiter':steps,'gtol':3e-7,'ftol':0.,'maxls':35,'maxcor':15})
        info,fields=self.energy(opt.x,True)
        info['optimizer']={'success':bool(opt.success),'iterations':int(opt.nit),
            'gradient_inf':float(max(abs(opt.jac))),'message':str(opt.message)}
        info['symmetric_parity_max']=float(np.max(abs(
            fields['F'][0].reshape(self.nr,self.nz)-
            fields['F'][1].reshape(self.nr,self.nz)[:,::-1])))
        return info,fields

    def y_response(self,fields,alpha=1.):
        """First-order, frozen-X induced magnetic Y. Y electric is zero here."""
        shape=(self.nr,self.nz)
        F=fields['F'].reshape(2,*shape)
        W=fields['W'].reshape(2,*shape)
        A=fields['A'].reshape(shape)
        rr=self.rho.reshape(shape)
        zz=self.z.reshape(shape)
        h=self.h
        def dr(f):return np.gradient(f,h,axis=0,edge_order=2)
        def dz(f):return np.gradient(f,h,axis=1,edge_order=2)
        ff=F*F
        K=np.sum(np.gradient(F,h,axis=1,edge_order=2)**2
            +np.gradient(F,h,axis=2,edge_order=2)**2-W*W*ff,axis=0)
        U=np.sum(ff-2*ff**2+2*ff**3,axis=0)+self.s.g*ff[0]*ff[1]
        lam=-2*alpha*(K+2*U)
        # PH15-P1: jphi=lambda_r * A0_z - lambda_z * A0_r.
        Er,Ez=-dr(A),-dz(A)
        current=dr(lam)*dz(A)-dz(lam)*dr(A)
        Lphi=(self.L+diags(1/self.rho**2)).tocsc()
        v=spsolve(Lphi,current.ravel()).reshape(shape)
        Br=-dz(v)
        Bz=dr(v)+v/rr
        P=Er*Br+Ez*Bz
        w=self.w.reshape(shape)
        radius=np.sqrt(rr**2+zz**2)
        shell=radius>.65*self.s.L
        ymag=.5*np.dot(self.w*current.ravel(),v.ravel())
        # This axisym magnetic dipole is a leading finite-box diagnostic.
        y_mu=float(.5*np.sum(w*rr*current))
        return {
            'alpha':alpha,'Y_current_L2':float(np.sqrt(np.sum(w*current**2))),
            'Y_magnetic_energy_CANONICAL':float(ymag),
            'Y_electric_field_first_order':'EXACT_ZERO_BX_ZERO_STATIONARY',
            'Y_magnetic_dipole':y_mu,
            'P_absolute_integral':float(np.sum(w*abs(P))),
            'P_signed_integral':float(np.sum(w*P)),
            'P_max_abs':float(np.max(abs(P))),
            'portal_sigma_max_abs_beta0':float(np.max(abs(alpha*P))),
            'P_outer_shell_max_abs':float(np.max(abs(P[shell]))),
            'Y_B_outer_shell_max_abs':float(max(np.max(abs(Br[shell])),np.max(abs(Bz[shell])))),
            'leading_axis_dipole_product_XY':float(fields['charge']@(self.w*self.z)*y_mu),
            'Y_boundary':'FINITE_DIRICHLET_NOT_FREESPACE_CERTIFIED',
            'Y_reciprocal_loading':'NOT_SOLVED',
        }

    def axial_trial(self,fields,step=.18):
        """Restricted fixed-Noether energy probes; NOT full stability."""
        baseF=fields['F'].reshape(2,self.nr,self.nz)
        base=self.energy((baseF.reshape(2,-1)*np.sqrt(self.w)).ravel())[0]
        out={}
        for family in ('relative','common'):
            ds=[]
            for sign in (-1,1):
                trial=baseF.copy()
                for i in (0,1):
                    multiplier=sign*(1 if family=='common' or i==0 else -1)
                    trial[i]=ndi_shift(baseF[i],(0,multiplier*step/self.h),
                        order=3,mode='constant',cval=0.)
                e=self.energy((trial.reshape(2,-1)*np.sqrt(self.w)).ravel())[0]
                ds.append(float(e-base))
            out[family]={'delta_energy_minus':ds[0],'delta_energy_plus':ds[1],
                'symmetric_curvature_proxy':float((ds[0]+ds[1])/step**2)}
        return out

    def matched_angular_trial(self,fields,k,h,t,angles=24):
        """Independent 3D-azimuth density trial with local Gauss source fixed.

        f_i**2 -> f_i**2 (1+t*a_i*cos(k*phi)), where
        W_+ f_+**2 a_+ == W_- f_-**2 a_- pointwise.
        Each N_i is exactly fixed after angle averaging, while rho_X is
        unchanged locally. This is a narrow subset of physical perturbations;
        X and Y backreaction and general phase modes are untested.
        """
        F=fields['F'];W=fields['W'];s=F*F
        weighted=W*s;totalw=weighted.sum(axis=0)
        a=np.stack((weighted[1]/totalw*h,weighted[0]/totalw*h))
        value=0.
        for phi in 2*np.pi*np.arange(angles)/angles:
            c=np.cos(k*phi);st=np.sin(k*phi)
            factor=1+t*a*c
            if np.min(factor)<=0:raise ValueError('Negative density in trial')
            ff=s*factor
            f=F*np.sqrt(factor)
            grad=sum(np.dot(self.w,f[i]*(self.L@f[i])) for i in (0,1))
            angular=sum(np.dot(self.w,s[i]*(t*k*a[i]*st)**2/
                (4*factor[i]*self.rho**2)) for i in (0,1))
            scalar=sum(np.dot(self.w,W[i]**2*ff[i]+ff[i]-2*ff[i]**2+
                2*ff[i]**3) for i in (0,1))
            contact=self.s.g*np.dot(self.w,ff[0]*ff[1])
            value+=(grad+angular+scalar+contact)/angles
        return float(value)

    def angular_gauss_matched_screen(self,fields,levels=(1,2)):
        """Six-mode Rayleigh screen; positive is NOT full mode health."""
        F=fields['F'];W=fields['W'];
        weighted=W*(F*F);den=weighted.sum(axis=0)
        c=np.stack((weighted[1]/den,weighted[0]/den))
        ans={}
        for k in levels:
            B=np.array([
                (self.rho/3)**k*np.exp(-(
                    (self.rho-r0)**2+(self.z-z0)**2)/(2*3.5**2))
                for r0 in (1.5,4.) for z0 in (-3.,0.,3.)
            ])
            eps=.04
            base=self.matched_angular_trial(fields,k,B[0],0)
            def quadratic(h):
                return (self.matched_angular_trial(fields,k,h,eps)
                    +self.matched_angular_trial(fields,k,h,-eps)-2*base)/(2*eps**2)
            count=len(B)
            H=np.array([[.25*(quadratic(B[i]+B[j])-quadratic(B[i]-B[j]))
                for j in range(count)] for i in range(count)])
            H=(H+H.T)/2
            G=np.array([[sum(np.dot(self.w*F[m]**2*c[m]**2*B[i],B[j])
                for m in (0,1)) for j in range(count)] for i in range(count)])
            eigen=eigh(H,G,eigvals_only=True)
            ans['k'+str(k)]={
                'minimum_generalized_energy_eigen':float(eigen[0]),
                'maximum_generalized_energy_eigen':float(eigen[-1]),
                'basis_dimension':count,'quadrature_angles':24,
                'gram_condition':float(np.linalg.cond(G)),
                'scope':'GAUSS_MATCHED_DENSITY_ONLY_FROZEN_GAUGE',
                'full_stability':'NOT_CERTIFIED',
            }
        return ans


def one_charged_soliton_reference(spec):
    """Separately solve one matched-N charged X soliton in same finite box.

    2*E_one is a baseline; finite-box charged monopoles do not give an
    exact unbounded-space separated-pair energy.
    """
    model=Dipole(spec)
    w=model.w
    q=spec.e
    f0=np.exp(-(model.rho**2+model.z**2)/(2*2.6**2))
    f0*=np.sqrt(spec.N/(1.6*np.dot(w,f0*f0)))
    def E(y):
        f=y/np.sqrt(w)
        f2=f*f
        I=np.dot(w,f2)
        D=(model.L+diags(2*q*q*f2)).tocsc()
        omega=spec.N/(2*I)
        for _ in range(80):
            A=spsolve(D,2*q*omega*f2)
            nxt=(spec.N/2+q*np.dot(w,f2*A))/I
            if abs(nxt-omega)<2e-12:
                omega=nxt
                break
            omega=nxt
        A=spsolve(D,2*q*omega*f2)
        W=omega-q*A
        val=.5*np.dot(w*A,model.L@A)+np.dot(w,
            W*W*f2+f*(model.L@f)+f2-2*f2*f2+2*f2**3)
        resid=model.L@f+(1-W*W-4*f2+6*f2*f2)*f
        return float(val),2*np.sqrt(w)*resid
    opt=minimize(E,f0*np.sqrt(w),jac=True,method='L-BFGS-B',
        bounds=[(0,None)]*len(w),options={'maxiter':350,'gtol':4e-7,
                                          'ftol':0.,'maxls':35})
    v,grad=E(opt.x)
    if max(abs(grad))>5e-5:raise ArithmeticError('One-soliton comparison unconverged')
    return {
        'single_energy_CANONICAL_NOT_J':v,
        'two_separate_reference_energy_CANONICAL_NOT_J':2*v,
        'gradient_inf':float(max(abs(grad))),
        'scope':'MATCHED_N_CHARGED_MONOPOLE_IN_SAME_FINITE_DIRICHLET_BOX',
        'not_global_binding_proof':True,
    }


def theorem_checks():
    """Independent symbolic variations of new contact term and portal trace."""
    import sympy as sp
    f1,f2,g,K,a,b,P=sp.symbols('f1 f2 g K alpha beta P',real=True)
    u=lambda f:f*f-2*f**4+2*f**6
    U=u(f1)+u(f2)+g*f1*f1*f2*f2
    assert sp.simplify(sp.diff(U,f1)-2*f1*(1-4*f1*f1+6*f1**4+g*f2*f2))==0
    assert sp.simplify(sp.diff(U,f2)-2*f2*(1-4*f2*f2+6*f2**4+g*f1*f1))==0
    sigma=a*P-b*P**2
    lag=-sp.exp(2*sigma)*K-sp.exp(4*sigma)*U
    lam=sp.diff(lag,P)
    lam0=sp.simplify(lam.subs(P,0))
    assert sp.simplify(lam0+2*a*(K+2*U))==0
    assert sp.simplify(sp.diff(lam0,g)+4*a*f1*f1*f2*f2)==0
    lamprime=sp.simplify(sp.diff(lam,P).subs(P,0))
    assert sp.simplify(lamprime-(4*b*(K+2*U)-4*a*a*(K+4*U)))==0
    return {
        'source_contact_variation':'PASS_EXACT_BOTH_SPECIES',
        'portal_lambda_0':'-2*alpha*(K+2*U_total)',
        'contact_portal_derivative':'d(lambda0)/dg=-4*alpha*fplus^2*fminus^2',
        'lambda_prime_0':'4*beta*(K+2*U_total)-4*alpha^2*(K+4*U_total)',
        'gauge_Ward':'STATIONARY_X_SOURCE_CURRENT_CONTINUITY_ONLY',
        'full_metric_stress':'NOT_DERIVED',
    }


def evaluate_case(spec):
    s=Dipole(spec)
    info,fd=s.solve()
    if (max(info['scalar_EOM_weighted_L2'])>2e-4
        or info['gauss_L2']>1e-8
        or max(abs(np.array(info['individual_Noether'])-spec.N))>1e-7
        or abs(info['net_X_charge'])>1e-8
        or info['optimizer']['gradient_inf']>1e-4):
        raise RuntimeError('X-source numerical EOM/conservation gate failed')
    info['spec']=asdict(spec)
    info['Y_first_order']=s.y_response(fd)
    info['restricted_axial_trial']=s.axial_trial(fd)
    if spec.g>.0 and spec.seed_separation==3. and spec.nr in (18,24):
        info['gauss_matched_angular_screen']=s.angular_gauss_matched_screen(fd)
        info['separated_reference']=one_charged_soliton_reference(spec)
        info['conditional_two_monomer_energy_advantage']=float(
            info['separated_reference']['two_separate_reference_energy_CANONICAL_NOT_J']
            -info['energy_CANONICAL_NOT_J'])
    else:
        info['gauss_matched_angular_screen']='NOT_RUN_FOR_THIS_CASE'
    return info


def run(root,quick=False):
    cases=[
        ('base18_seed0p5',Spec(seed_separation=.5)),
        ('base18_seed3',Spec(seed_separation=3.)),
        ('base18_seed6',Spec(seed_separation=6.)),
        ('refine27_L12',Spec(nr=27,L=12.)),
        ('large24_L16',Spec(nr=24,L=16.)),
        ('large30_L20',Spec(nr=30,L=20.)),
        ('control_g0',Spec(g=0.)),
        ('control_e0p14',Spec(e=.14)),
    ]
    if quick:cases=[cases[1],cases[6]]
    out={}
    for name,spec in cases:
        r=evaluate_case(spec)
        out[name]=r
        print('CASE',name,
            'E',round(r['energy_CANONICAL_NOT_J'],6),
            'separation',round(r['source_separation'],6),
            'Y_jphi',round(r['Y_first_order']['Y_current_L2'],6),
            'P_outer',round(r['Y_first_order']['P_outer_shell_max_abs'],9),
            'tail',round(r['outer_80percent_spherical_tail_fraction'],6),
            'mode_relative',round(r['restricted_axial_trial']['relative']['symmetric_curvature_proxy'],6),flush=True)
    artifact={
        'branch':'032H17-PH15-P8-DISTINCT_NONWINDING_TWO_CENTER_X_SOURCE',
        'source_sha256':sha256(__file__),
        'utc':datetime.now(timezone.utc).isoformat(),
        'new_physics':'POSITIVE_INTERSPECIES_CONTACT_QUARTIC_g|psi+|^2|psi-|^2',
        'action_scope':'FIXED_MINKOWSKI_TWO_CHARGED_SCALARS_X_MAXWELL',
        'physical_metric':'PROPOSED_CONFORMAL_NOT_ONSHELL_GRAVITY',
        'cases':out,
        'exact_action_theorems':theorem_checks(),
        'P8_source_on_shell':'FINITE_BOX_DISCRETE_X_ONLY',
        'first_order_Y':'LINEAR_RESPONSE_FIXED_X_NOT_RECIPROCAL',
        'full_stability':'NOT_CERTIFIED',
        'full_2U1_reciprocal':'NOT_SOLVED',
        'free_space_exterior':'NOT_CERTIFIED',
        'complete_SI_energy':'NOT_AVAILABLE',
        'Earth_down_craft_up':'NOT_DERIVED',
        '50_percent_theory_gate':'NOT_MET',
        'stable_source':'NOT_CERTIFIED',
        '006D_replaced':False,'M5V_status':'FROZEN',
    }
    path=Path(root)/'results/data'/('032h17_ph15_p8_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:json.dump(artifact,f,indent=2,sort_keys=True,allow_nan=False)
    print('RESULT_PATH='+str(path))
    print('RESULT_SHA256='+sha256(path))
    print('PH15_P8_EXECUTION=PASS_SCOPED')
    return artifact


if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1] not in ('quick','full'):
        raise SystemExit('Usage: python module.py [quick|full]')
    run(Path.cwd(),quick=(len(sys.argv)>1 and sys.argv[1]=='quick'))
