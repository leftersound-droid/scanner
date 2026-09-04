# Emergent rigid-rotation necessary-condition probe — pilot result

## Question
Can a compact P/J object initialized with both internal longitudinal phase structure and a rigid-rotation-like circulating J component preserve autonomous periodic/inertial rotation under the unchanged self-reflexive transfer algebra, without a continued teacher?

## Scope
This is a necessary-condition pilot, not yet a full emergent-metric rigid-body test. The 4D toroidal lattice is used only as a boundary-free numerical representation. Primary readouts are graph/direction-pair invariants. The m=3 orientation phase is retained only as a representation diagnostic and is not interpreted as physical angle.

No stabilizer, damping, torque law, angular-momentum law, inertia law, force law, or physical metric is added after initialization.

## Initial state
A compact anisotropic ring-like P object carries an m=3 internal marker. The initial previous-flow state contains:

- a tangential circulation component in one local graph plane;
- a longitudinal +/- fourth-direction phase component.

After frame 0 the P/J state is released completely.

Rotation-amplitude sweep: `0, 0.01, 0.04, 0.10, 0.25`.

## Key numerical findings
The initial circulation magnitude changes strongly across the sweep, but the operator output rapidly forgets that amplitude. Representative values:

| initial rotation amplitude | initial circulation RMS | circulation RMS after first operator step |
|---:|---:|---:|
| 0.00 | 0.000235 | 0.001476 |
| 0.01 | 0.000283 | 0.001438 |
| 0.04 | 0.000671 | 0.001434 |
| 0.10 | 0.001587 | 0.001439 |
| 0.25 | 0.003930 | 0.001444 |

Thus a >16x change in initial circulation is compressed to an output band of only about 3% width after one step.

For the `rotation_amp=0.10` case, circulation RMS then evolves:

`0.001439 -> 0.000604 -> 0.000485 -> 0.000373 -> 0.000351 -> 0.000342 -> 0.000350 -> 0.000374`

in the first eight released frames. There is no sustained circulation plateau at the initialized value and no sign of a closed circulation orbit.

The representation-only m=3 orientation diagnostic does not continue rotating. Across 50 frames, depending on the initialization amplitude, the total orientation excursion remains below about `0.20 deg`. The m=3 shape marker decays to about `18-19%` of its first-step amplitude.

The P excess is conserved by the live-neighbour transfer algebra, while local structure spreads/relaxes. Graph-native Dirichlet/participation readouts change monotonically toward a more diffuse state rather than revisiting an earlier invariant state.

## Structural interpretation
The result is consistent with the current operator form:

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

where `alpha` is rebuilt from current downhill P differences and `beta` is only a normalized distribution of previous J over currently live downhill edges.

Consequences visible in this pilot:

1. absolute previous-flow magnitude is largely discarded by beta normalization;
2. previous J does not independently transport a tangential/inertial current;
3. every new J is rebuilt from current positive P differences;
4. a circulating initial J therefore does not behave as a conserved angular/inertial state variable.

This is a structural negative result for the *current operator*, not for the broader hypothesis that stable objects require periodic inertial rotation.

## What is and is not falsified
Supported negative statement:

> A compact P structure plus one initialized longitudinal/circulating J phase is not sufficient, under the current raw operator, to generate autonomous rigid-body-like periodic rotation.

Not falsified:

- a more complex self-consistent P/J phase orbit learned over a full cycle;
- a genuinely emergent rigid rotation defined after reconstructing emergent distance/orientation;
- a deeper operator in which P and J are complementary dynamical state variables rather than J being regenerated almost entirely from instantaneous downhill P.

## Important methodological conclusion
A full test of the user's rigid-body stability hypothesis cannot use grid angle as its criterion. It requires at least:

1. an emergent shape invariant / distance readout;
2. an emergent orientation relation;
3. a cyclic orientation trajectory while shape invariants remain constant;
4. an internal P/J phase orbit coexisting with that external cyclic motion;
5. representation and refinement invariance.

The present probe therefore serves as a falsification gate: the current raw operator does not preserve even the weaker graph-circulation necessary condition from a one-shot inertial seed.
