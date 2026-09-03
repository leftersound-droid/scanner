# P/J metric-regime probe

Purpose: test whether the unchanged self-reflexive operator contains graph-native structure sufficient to distinguish (i) homogeneous Euclidean/Newton-like background, (ii) homogeneous oriented/causal Minkowski candidate, and (iii) inhomogeneous second-order GR-like candidate, without inserting Newton, Minkowski, or Einstein dynamics.

## Operator
Uses `src/scanner/self_reflexive_operator.py` unchanged.

## Controls
- E: constant P background, J initially zero.
- N: weak affine P gradient along one lattice direction.
- M: the same affine gradient along a different lattice direction.
- G: localized smooth 4D P bump.

The N/M pair is a falsification control. If the readout is representation-independent, a coordinate permutation must not make them physically distinct.

## Graph-native measurements
All are readouts only and do not feed back into the operator:
- first-order normalized P edge variation;
- antipodal second P difference;
- normalized outgoing-J orientation vector magnitude;
- global orientation coherence;
- neighbor-to-neighbor orientation-field roughness;
- local J-activity roughness.

## Result (interior of 9^4 lattice, four operator steps)

E remains exactly flat: all listed complexity readouts are 0.

M step 1:
- P first-order variation = 0.00250225395
- P second-order variation ~ 1.45e-18
- J orientation magnitude = 1.0
- global orientation coherence ~ 1.0
- orientation roughness = 0
- mean J activity = 0.0200

G step 1:
- P first-order variation = 0.0118740151
- P second-order variation = 0.00326272006
- J orientation magnitude = 0.473289573
- global orientation coherence ~ 2.9e-17
- orientation roughness = 0.151526493
- J activity roughness = 0.147918424
- mean J activity = 0.0313585743

After four steps the G state still has clear second-order structure (P second-order = 0.00168752; orientation roughness = 0.146572), while M remains globally coherent with zero orientation roughness.

Potential is conserved to machine precision in all runs; no births occurred in these interior-safe pilots.

## Strong falsification result
N (affine gradient in coordinate 0) and M (identical gradient in coordinate 3) are exactly related by the coordinate permutation x <-> w. For all four steps, after mapping states and direction labels through this permutation:

- max |Delta P| = 0.0
- max |Delta J| = 0.0

Therefore no representation-independent P/J readout may call one of these states 'Newton' and the other 'Minkowski' merely because the active channel is named x versus w. A Minkowski/time-like sector requires an additional graph-native invariant (for example a persistent causal/orbit property), not a selected lattice coordinate.

## Interpretation
The pilot supports a three-level structural distinction:
1. homogeneous static state: zero relational complexity;
2. homogeneous oriented state: first-order directed relation with high global coherence and negligible second-order roughness;
3. inhomogeneous state: nonzero second-order P/J variation and spatially changing orientation field.

This is evidence that the current P/J dynamics contains enough native information to distinguish first-order homogeneous from second-order inhomogeneous regimes. It does **not** yet derive Newtonian, Minkowski, or GR metrics. In particular, the L(P,J) and T(P,J) metric/causal readouts remain undefined.

Next decisive test: define a coordinate-free causal invariant from P/J history/closed state recurrence, then test whether a single L/T readout family maps the homogeneous static, homogeneous causal, and inhomogeneous second-order regimes to Euclidean/Newton, Minkowski, and GR-like effective forms without regime-specific tuning.
