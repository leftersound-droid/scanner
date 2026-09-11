# Work memory — effective particle state and object/background formalization v0.1

Date: 2026-09-11
Status: mathematical formalization / working readout framework. No operator change.

## 1. Constraints

The self-reflexive P/J operator remains unchanged. P and J are complementary local informational variables. Known physics is used only as external analogy/validation and not as input dynamics.

The numerical lattice coordinate is not assumed to be physical distance and the update index is not assumed to be physical time.

Because the 2026-09-10 reparameterization control showed strong clock sensitivity of dG/dtau and d2G/dtau2, time derivatives are excluded from the intrinsic particle-state vector until an independent emergent clock is identified.

## 2. Fundamental state

Let the instantaneous graph state be

G = (V,E;P,J)

with node scalar P_i and directed local edge-flow components J_{i,a}.

The operator generates

G_(n+1) = O[G_n]

with no additional physical variables.

## 3. Background as a relational reference, not a second ontology

For a given experiment define a matched background reference B using, in order of preference:

1. the same background preparation evolved by the same operator without the localized object, or
2. the asymptotic/far-field state when a matched control is unavailable.

B is a readout reference only. It does not modify the dynamics.

For each node i define dimensionless relational channels

r_i^P = P_i / B_i^P

r_i^J = (sum_a J_{i,a}) / (sum_a B^J_{i,a})

and directional flow fractions

pi_{i,a} = J_{i,a} / sum_b J_{i,b}.

When a denominator is numerically zero, any epsilon regularization is strictly a numerical readout device and its sensitivity must be reported; it is not an axiom or dynamics parameter.

A local joint relational signature can therefore be written schematically as

z_i = (r_i^P, r_i^J, pi_i - pi_i^B, harmonic content, relative phase content, ...).

No single weighted norm of z_i is declared fundamental.

## 4. Object without a hard boundary

The object is defined as a localized, connected departure of the joint P/J relational state from the background reference, not as a region selected by a fixed P threshold.

Channel-specific soft localization measures may be used, e.g.

w_i^P = (P_i-B_i^P)^2 / sum_j (P_j-B_j^P)^2

w_i^J = ||J_i-J_i^B||^2 / sum_j ||J_j-J_j^B||^2.

These are readout measures only. They do not affect evolution.

The previous empirical core/coupling/far decomposition is reinterpreted as three relational regimes:

- core: strongest persistent joint departure from background and strongest object-specific internal pattern;
- coupling zone: smaller raw contrast but strong relational dependence on the core and strong transfer of the object's characteristic pattern/phase;
- far field: weak departure from background and weak object-specific detail, possibly retaining interaction-relevant low-order characteristics.

Thus the object need not possess one unique geometric radius.

## 5. First effective particle-state vector

The first effective particle description is deliberately dimensionless and unnamed physically.

Define

C_P = P_core / P_far
C_J = J_core / J_far
T_P = P_coupling / P_core
T_J = J_coupling / J_core
H_Pq = A_m^P(coupling) / A_m^P(core)
H_Jq = A_m^J(coupling) / A_m^J(core)
H_Pf = A_m^P(far) / A_m^P(core)
H_Jf = A_m^J(far) / A_m^J(core)
K_P = coherence_P(coupling,core) / coherence_P(core-shell,core)
K_J = coherence_J(coupling,core) / coherence_J(core-shell,core)
R_34 = J_R3 / J_w.

The minimal current coordinate in effective-state space is

Q^(0) = (C_P,C_J,T_P,T_J,H_Pq,H_Jq,H_Pf,H_Jf,K_P,K_J,R_34,...).

This is not yet a list of physical observables. It is a coordinate system for identifying stable P/J dynamical classes.

## 6. Numerical value from the existing 24^4 object/environment experiment

Using the previously measured region averages:

C_P = 15.8121
C_J = 11.3463
T_P = 0.52468
T_J = 0.66365
H_Pq = 0.39144
H_Jq = 0.30808
H_Pf = 0.32891
H_Jf = 0.13561
K_P = 2.05797
K_J = 1.13439.

From the independent multiresolution measurements, R_34 = J_R3/J_w was approximately 3.0 with mean cross-resolution CV about 0.76%, making it the strongest present invariant candidate.

The other values above are only one measured state's coordinates and must not yet be called particle invariants.

## 7. Orbit/class definition of a particle

A particle candidate is not a fixed Q vector. It is a bounded dynamical class/orbit in Q-space:

C_particle = { Q[G] : G belongs to the same recurrent relational class }.

A microscopic trajectory may change continuously while the class remains stable.

Two states are candidates for the same effective particle when their Q-trajectories are equivalent under allowed phase/orientation changes and remain in the same bounded relational class under weak perturbations.

## 8. Separating intrinsic state from environmental response

Intrinsic candidate coordinates are those that remain stable across changes of scanner resolution, small background variations, phase choice and weak perturbations.

Physical properties should later be sought in the response of Q to controlled P-only probes rather than assigned directly to raw P or J.

For a small probe family epsilon_b define the response matrix

chi_ab = [ Q_a(G_epsilon_b) - Q_a(G_0) ] / epsilon_b

in the weak-probe limit where this limit exists.

J is never externally forced.

At first chi_ab remains unnamed. A row/column is called charge-like, spin-like, mass/inertia-like, etc. only after it reproduces the corresponding functional behavior across multiple independent experiments.

## 9. Time-parametrization rule

Until emergent time is independently calibrated, the intrinsic particle state must use quantities invariant under monotonic time reparameterization where possible:

- raw dimensionless ratios;
- harmonic amplitudes and relative phases;
- parametric orbit relations Q_b(Q_a);
- loop/hysteresis geometry in state space;
- recurrence/topological class without assigning a physical period.

Quantities dQ/dtau and d2Q/dtau2 are retained only as clock-dependent diagnostics.

## 10. Immediate consequence

The earlier three-region experiment already supplies a nontrivial first map

G_P/J -> Q^(0)

without inserting mass, charge, spin, force, wave equations or other physical axioms.

The next experimental cycle should test which components of Q^(0) survive changes in:

- resolution;
- object preparation phase;
- weak P-only isotropic probe;
- weak P-only R3 gradient;
- weak P-only w/radial gradient;
- weak P-only tangential orientation probe;
- small background phase/amplitude changes.

The result should be a sensitivity/response matrix separating candidate intrinsic invariants from environment-dependent coordinates.

Only after this separation should individual channels be compared with known particle properties.
