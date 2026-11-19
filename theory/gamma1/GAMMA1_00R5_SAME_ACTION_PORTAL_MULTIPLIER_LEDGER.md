# GAMMA1-00R5 — Original-action portal multiplier and covariant metric preflight

## Scope and provenance

This run uses the SHA-locked R3 12/L12 native stationary F+/F-/X/Y profile, and reconstructs the exact historical PH16-04R2 finite-lattice Routhian with the UNMODIFIED producing source. It performs NO source solve and does not alter PH16, R3, R4 or R4R1 data or negative controls. The 18/L12 weak-seed failure remains unresolved.

This is a stationary finite-dimensional necessary-condition test together with separately derived restricted Lorentzian identities. The two action levels are NOT assumed identical. There is NO new Einstein metric, complete fluid or support action, physical device force, or SI energy calculation.

## Exact lattice multiplier

The original PH16-04R2 defines, cellwise,

    lambda_R(a) = -(1/w_a) dR/dP_a
    dR/dP_a = (dR/dsigma_a) (alpha - 2 beta P_a)

where the derivative is evaluated at fixed native F/A/Y, and with stationarily eliminated source frequencies and conserved neutral labels (envelope property). The original edge-gradient, potential, fixed-Noether kinetic and neutral-fluid contributions ALL enter dR/dsigma. The R3 native source is evaluated by the original PH16 `JointAction.evaluate` function, and must reproduce its full archived joint gradient.

Original source-cell Routhian gradients obey

    grad_X(R) = -K_X A_X + J_X + C_A^T (-w lambda_R)
    grad_Y(R) =  K_Y A_Y       + C_Y^T (-w lambda_R)

with C_A=dP/dA_X, C_Y=dP/dA_Y from the SAME original lattice action. R5 archives the separate bare and portal terms. Its independent verifier computes dR/dsigma by all-cell finite differences of the frozen-envelope action. This is a genuine additional check, not a projection from toy fields.

## Separate covariant hypothesis

For one candidate universal physical metric,

    gtilde_mn = exp(2 sigma(P)) g_mn
    sigma(P) = alpha P - beta P^2
    P = 1/2 F_Xmn (*F_Y)^mn

with the Lorentzian Hodge star and *covariant* gauge field strengths held fixed in a metric variation,

    delta P = (P/2) g_mn delta g^mn

For any diffeomorphism-invariant physical-metric matter action with physical stress tensor Ttilde_mn and trace Ttilde,

    lambda_cov = exp(4sigma) Ttilde sigma_prime(P)
    T_E_mn = exp(2sigma) Ttilde_mn - lambda_cov P g_mn

The field constitutive tensors include

    H_X^mn = F_X^mn - lambda_cov (*F_Y)^mn
    H_Y^mn = F_Y^mn - lambda_cov (*F_X)^mn

and therefore bulk portal exchange terms proportional to grad(lambda_cov) contracted with the dual carrier strength; constant lambda_cov contributes no bulk source if the other U(1) Bianchi identity holds. The full off-shell source, fluid and solid Ward identities still require their unconstrained dynamical actions. This run checks only the restricted exact algebra and four off-shell Y Bianchi identities; an independent numerical metric trace check is included.

Important: **lambda_R is not lambda_cov** without a demonstrated Lorentzian reduction and stress normalization. Its sign is NOT the sign of Einstein active mass, or proof of gravitational repulsion. The PH16 bare X/Y terms are discrete Green operators, NOT a sourced continuum Einstein field or certified source-free exterior.

## Physical no-promotion conditions

A positive outward sign in R4 and nonzero lambda_R in R5 are necessary model data only. The full Lorentzian constrained modes, Earth/support constitutive laws, universal material response, SI normalization, Einstein geometry, source-free exterior, Earth-down and whole-craft-up momentum, all-phase operation, losses, and UV/quantum consistency remain open.

The target remains at least 1 g throughout a finite 1 kg neutral torus at at least 1 m true source stand-off, with complete operating energy strictly under 10 MJ. Exactly 10 MJ fails. 006D with C=23.591586299249 remains unreplaced. GAMMA1-01, PH16-05, PH17 are not automatically authorized.
