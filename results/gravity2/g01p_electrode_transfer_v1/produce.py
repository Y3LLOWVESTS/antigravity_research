"""G01-P static bright-X electrode-transfer check, distances in micrometres.

Ideal equipotential electrodes in vacuum. Visible E vanishes inside their
metal, hence tangential E vanishes on each face. With no hidden source the
bare electrostatic solution and H_Y=0 obey the full static jumps. Uniqueness
follows by positivity of the constrained incremental bulk energy. For s=1
the hidden magnetic scalar crosses this metal with unit permeability and no
reflection. The bead still perturbs the visible surface charges. This solver
keeps that feedback. It does not model a coating breach or the measured
permanent dipoles and calibration electronics.

The moving 500 x 2000 x 10 tip is approximated by a fixed 1 V cuboid;
the 4 mm grounded cage has an assumed rear feed opening. Bead locations are
sampled relative to that assembly. Electrode patches use singularity-integrated
constant elements. A neutral sphere has no l=0 response. Symmetries in x,y
retain real cosine harmonics with even azimuthal index. Force is integrated
against the field of the solved electrode charges using the bead's effective
exterior electric multipoles. Decaying hidden self-fields have zero net force.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.special import sph_harm_y
from numpy.polynomial.legendre import leggauss

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def panels(level):
    rows=[]
    def face(axis,pos,first,second,voltage,aperture=False):
        for a,b in zip(first[:-1],first[1:]):
            for c,d in zip(second[:-1],second[1:]):
                if aperture and a>=-400 and b<=400 and c>=-400 and d<=400:
                    continue
                rows.append([axis,pos,a,b,c,d,voltage])
    # Cyclic tangential axes: x-face (y,z), y-face (z,x), z-face (x,y).
    x=np.linspace(-250,250,8*level+1)
    y=np.linspace(-5,5,level+1)
    z=-2000*np.linspace(1,0,9*level+1)**2.35
    for v in (-250,250): face(0,v,y,z,1)
    for v in (-5,5): face(1,v,z,x,1)
    for v in (-2000,0): face(2,v,x,y,1)
    cage=np.unique(np.r_[np.linspace(-2000,2000,4*level+1),-400,400])
    for axis in range(3):
        for v in (-2000,2000): face(axis,v,cage,cage,0,axis==2 and v<0)
    return np.array(rows)

def centres(p):
    pts=np.empty((len(p),3))
    for j in range(3):
        mask=p[:,0]==j
        pts[mask,j]=p[mask,1]
        pts[mask,(j+1)%3]=(p[mask,2]+p[mask,3])/2
        pts[mask,(j+2)%3]=(p[mask,4]+p[mask,5])/2
    return pts

def panel_green(pts,p):
    out=np.empty((len(pts),len(p)))
    for j in range(3):
        mask=p[:,0]==j
        _,pos,x0,x1,y0,y1,_=p[mask].T
        x=pts[:,(j+1)%3,None]
        y=pts[:,(j+2)%3,None]
        h=np.abs(pts[:,j,None]-pos)
        def primitive(u,v):
            tiny=1.e-150
            return (u*np.arcsinh(v/np.maximum(np.hypot(u,h),tiny))
                   +v*np.arcsinh(u/np.maximum(np.hypot(v,h),tiny))
                   -h*np.arctan2(u*v,h*np.sqrt(u*u+v*v+h*h)))
        out[:,mask]=(primitive(x-x0,y-y0)-primitive(x-x1,y-y0)
                    -primitive(x-x0,y-y1)+primitive(x-x1,y-y1))/((x1-x0)*(y1-y0))
    return out

def harmonics(v,orders):
    rad=np.linalg.norm(v,axis=1)
    polar=np.arccos(np.clip(v[:,2]/rad,-1,1))
    az=np.arctan2(v[:,1],v[:,0])
    return np.column_stack([sph_harm_y(l,m,polar,az).real*(math.sqrt(2) if m else 1)
                            for l,m in orders])

def sphere_rule():
    x,w=leggauss(9)
    phi=np.arange(20)*2*np.pi/20
    xx,pp=np.meshgrid(x,phi,indexing="ij")
    sint=np.sqrt(1-xx**2)
    return np.c_[(sint*np.cos(pp)).ravel(),(sint*np.sin(pp)).ravel(),xx.ravel()],np.repeat(w,20)*2*np.pi/20

def one_distance(p,pts,lu,q0,d,a,theta,eps):
    order=[(l,m) for l in range(1,5) for m in range(0,l+1,2)]
    l=np.array([v[0] for v in order])
    dirs,weights=sphere_rule()
    Y=harmonics(dirs,order)
    proj=Y.T*weights
    origin=np.array([0.,0.,float(d)])
    surface=origin+a*dirs
    delta=np.array([0.,0.,.02])
    gs=panel_green(surface,p)
    dg=(panel_green(surface+delta,p)-panel_green(surface-delta,p))/.04
    # Leading dipole comparator uses independent axial derivatives of the
    # unperturbed collocation potential, in the same finite geometry.
    offsets=np.arange(-2,3)*.12
    v=panel_green(origin[None,:]+np.outer(offsets,[0,0,1]),p)@q0
    vp=(v[0]-8*v[1]+8*v[3]-v[4])/(12*.12)
    vpp=(-v[0]+16*v[1]-30*v[2]+16*v[3]-v[4])/(12*.12**2)
    reg=proj@gs
    radius=np.linalg.norm(pts-origin,axis=1)
    outgoing=harmonics(pts-origin,order)*(a/radius[:,None])**(l+1)
    response=lu_solve(lu,outgoing)
    eps_eff=eps+(l+1)*theta**2/(2*l+1)
    K=l*(eps_eff-1)/(l*eps_eff+l+1)
    ratios=[]
    for limit in (1,2,4):
        keep=l<=limit
        W=response[:,keep]*K[keep]
        inc=np.linalg.solve(np.eye(np.sum(keep))-reg[keep]@W,reg[keep]@q0)
        charge=q0+W@inc
        dz=proj[keep]@(dg@charge)
        force=a/(4*np.pi)*np.dot((2*l[keep]+1)*K[keep]*inc,dz)
        ratios.append(float(force/(a**3*K[0]*vp*vpp)))
    return {"distance_um":d,"radius_um":a,"bare_E_per_V":-vp,
            "bare_dE_dz_per_V":-vpp,"force_ratios_L1_L2_L4":ratios}

def main(root,out):
    parent=root/"results/gravity2/g01o_static_source_overlap_v1"
    archive=parent.with_name(parent.name+"_UPLOAD.tar.gz")
    pins={archive:"620202385ecebc57ef7e8fb5c5f64ec2c4017764114cdc569cb8464666671233",
          parent/"science.json":"9852e3c1a7cf1b6fbe66dad3d73e270b25d1dd984a72bcfbb8cea9fba4c2c948",
          parent/"verification.json":"e1386cb63175cddaf75b7b72a3459c78fadf0e0f8070bfa10dbb2b29aaa06021"}
    for path,pin in pins.items():
        if sha(path)!=pin: raise ValueError("parent drift "+str(path))
    data=json.loads((parent/"science.json").read_bytes())
    report=[]
    for level in (1,2,3):
        p=panels(level)
        pts=centres(p)
        G=panel_green(pts,p)
        lu=lu_factor(G)
        q0=lu_solve(lu,p[:,-1])
        err=float(np.max(np.abs(G@q0-p[:,-1])))
        if err>1e-9: raise ValueError("electrode residual")
        for target in data["rows"]:
            ratios=[one_distance(p,pts,lu,q0,d,a,target["theta"],3.8)
                    for d in (20,30,60,100,150) for a in (1.78,3.22)]
            report.append(dict(level=level,elements=len(p),residual=err,
                scale_eV=target["portal_scale_eV"],samples=ratios))
    doc=dict(run="G01-P",parents={str(k.relative_to(root)):v for k,v in pins.items()},
        producer_sha256=sha(Path(__file__)),samples=report,
        paper="10.1103/PhysRevLett.117.101101",unit_voltage=1,bright_fraction_s=1,
        transfer="induced quadratic force / isolated point-dipole prediction, same bare electrode geometry",
        ruled_scope="ideal conductor apparatus, centered neutral linear bead, sampled separations and two endpoint radii",
        measured_fit_reconstructed=False,raw_time_series_used=False,
        hidden_mixed_source_s_lt_1_finite_bead_response="OPEN",
        source_charge_retention="OPEN",physical_survivors=0,full_regression="NOT_RUN")
    with (out/"science.json").open("x") as o: json.dump(doc,o,indent=2,sort_keys=True,allow_nan=False)
    for row in report:
        vals=[t["force_ratios_L1_L2_L4"][-1] for t in row["samples"]]
        print(row["level"],row["elements"],row["scale_eV"],min(vals),max(vals))
    print("SCIENCE_SHA256",sha(out/"science.json"))

if __name__=="__main__": main(*map(Path,sys.argv[1:3]))
