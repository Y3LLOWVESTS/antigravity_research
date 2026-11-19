# GAMMA1-00R1 — Local universal-metric reciprocity and sign preflight

Scope: fixed finite-dimensional local Lorentzian background; four independent
*trial* canonical scalar representatives (source, neutral, Earth, supports)
sharing a single field-dependent metric. Not a sourced PH16/Einstein solution.

## One representative same-action local density

Use signature (-+++), g_cov=diag(-t,a,b,c), all parameters positive.
F_X01=ex, F_X23=bx, F_Y01=ey, F_Y23=by. Let v=sqrt(tabc).

    P=(ex by+bx ey)/v
    sigma=alpha P-beta P^2
    Q=sum_{participants} g^{mu nu} k_{s,mu} k_{s,nu}
    U=sum_{participants} U_s
    L_matter_density=-v[0.5 exp(2sigma) Q+exp(4sigma) U]
    L_Maxwell_density=0.5v[(ex^2+ey^2)/(ta)-(bx^2+by^2)/(bc)]

The scalar k_s represent local trial covariant gradients. They are *not*
certified solutions of charged-scalar equations or realistic Earth/support EOS.

Metric/Hodge variation at fixed F:

    dP=0.5 P g_mn d g^{mn}
    lambda=-(exp(2sigma) Q+4 exp(4sigma) U) sigma'(P)
    T_mn^E=exp(2sigma)sum_s k_{s,m}k_{s,n}
           -g_mn[0.5 exp(2sigma)Q+exp(4sigma)U+lambda P]

Carrier source terms are the same density derivatives:

    dL/de_x=v ex/(ta)+lambda by
    dL/db_x=-v bx/(bc)+lambda ey
    dL/de_y=v ey/(ta)+lambda bx
    dL/db_y=-v by/(bc)+lambda ex

These are independently checked by finite differences of the full local
action density in all four diagonal metric directions and all four F slots.
They are not the field Euler-Lagrange solutions on the PH16 mesh.

At P=0, alpha!=0 and X electric field nonzero, dL/db_y may be nonzero
through lambda ex. Therefore a zero existing Y field does not automatically
mean Y satisfies its linearized action equation. A constant lambda gives a
bulk boundary/topological null after Bianchi; spatial gradients matter.

## Local electric kinetic necessary preflight

Holding metric, scalar gradients and magnetic F fixed, the electric
Hessian along ex, ey is

    H_E= [v/(ta)] I_2 + [chi/v] (by,bx)^T(by,bx)
    chi=d lambda/dP (with fixed local canonical scalar data)

This is only a local 2x2 sub-block of the full constrained Lorentzian
principal symbol. It is NOT a physical-mode positivity certificate.

With beta=40 and alpha=0.05 a deliberately off-shell timelike scalar
trial (k0=2, U=.2, bx=.2, P=0) has H_E minimum -9.23952.
This is a counterexample to *uniform positivity for all backgrounds*,
NOT a proven ghost on the stationary PH16-04R2 solution.

## Prescribed dipole exterior sign theorem

Assume, only in a region outside physical material, two far field dipoles
produce collinear fields on their common axis:

    E_X=2 p_X/r^3, B_Y=2 m_Y/r^3, E_Y=B_X=0
    P=4 d/r^6, d=p_X m_Y
    sigma=4 alpha d/r^6-16 beta d^2/r^12
    a_sigma/c^2= -d(sigma)/dr
                 =24 alpha d/r^7-192 beta d^2/r^13

A sign flip of the prescribed dipole orientation changes the leading r^-7
term, not the quadratic r^-13 term. Hence no source-independent outward
sign is established. These exact algebraic far-field expressions are not
on-shell two-carrier field solutions and do NOT include the sourced
Einstein potential, stress, recoil, support forces, or Earth loading.

## Conservation and stopping criterion

To derive Earth-down and whole-craft-up forces requires an actually varied
Earth term and actual supported source/geometry. Full off-shell Noether,
Ward and Bianchi equations on the same dynamically coupled fields, healthy
constrained kinetic modes, true exterior convergence, SI source/support
costs, empirical and UV consistency and worldtube boundary flux remain OPEN.

Do not invoke GAMMA1-01 or PH17 just because finite-difference identities
pass. Do not modify any GAMMA1-00, PH16, ALPHA, BETA or 006D artifacts.
No numerical continuation, optimization or field-capacity polishing here.
