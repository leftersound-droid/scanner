# Continuum-to-grid calibration probe — result

## Scope

This is a representation-calibration test, not a physical calibration and not a definition of emergent distance, volume, mass, energy, or time.

The live-neighbour algebra of the current self-reflexive operator is kept unchanged.  A smooth periodic 4D reference state is sampled at several resolutions.  The periodic domain is a control device that removes boundary/birth contamination from this calibration test.

The same continuous reference field is sampled at `n = 8, 12, 16, 20, 24`.  Numerical evolution is compared at constant `steps*h = pi/2`, i.e. the number of updates is increased as the spatial sampling is refined.  This is only a numerical-evolution scaling control, not physical time.

## Main measured values (base representation)

| n | h | steps | raw sum(P) | h^4 sum(P) | J/h | RMS(J)/h | direction entropy | antipodal orientation |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8  | 0.785398 | 2 | 6,144 | 2337.818185 | 0.055514 | 0.011396 | 0.589111 | 0.217716 |
| 12 | 0.523599 | 3 | 31,104 | 2337.818185 | 0.058931 | 0.012359 | 0.580442 | 0.235481 |
| 16 | 0.392699 | 4 | 98,304 | 2337.818185 | 0.061199 | 0.012745 | 0.585316 | 0.241023 |
| 20 | 0.314159 | 5 | 240,000 | 2337.818185 | 0.062844 | 0.013065 | 0.586885 | 0.243245 |
| 24 | 0.261799 | 6 | 497,664 | 2337.818185 | 0.064161 | 0.013311 | 0.588107 | 0.243979 |

`mean(P)` remained exactly 1.5 at every resolution.  Total potential was conserved by the transfer update to numerical precision.

## Relative error versus n=24 reference

| n | raw sum(P) | integrated P | std(P) | raw mean J | J/h | RMS(J)/h | direction entropy | direction concentration | antipodal orientation |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8  | 98.77% | ~0% | 20.56% | 159.57% | 13.48% | 14.39% | 0.17% | 2.87% | 10.76% |
| 12 | 93.75% | 0%  | 10.44% | 83.70%  | 8.15%  | 7.15%  | 1.30% | 3.46% | 3.48% |
| 16 | 80.25% | ~0% | 5.23%  | 43.08%  | 4.62%  | 4.25%  | 0.47% | 1.34% | 1.21% |
| 20 | 51.77% | ~0% | 2.10%  | 17.54%  | 2.05%  | 1.85%  | 0.21% | 0.50% | 0.30% |

## Representation permutation control

A second representation swaps the first and fourth computational axes.  After mapping the result back through the same permutation and remapping the associated direction channels, at n=16:

- max |Delta P| = 2.44e-15
- max |Delta J| = 1.02e-15

Thus the local live-transfer dynamics is equivariant under this representation symmetry to machine precision.

## Interpretation

1. **Raw grid totals are not continuum observables.**  `sum(P)` grows approximately with the number of grid samples and changes by almost two orders of magnitude across the tested range.

2. **A correctly weighted integral can remove pure sampling distortion.**  On this deliberately known reference measure, `h^4 sum(P)` is invariant to machine precision.  This does *not* establish the model's emergent volume measure; `h^4` is only the known control measure of the synthetic calibration manifold.

3. **The raw current has a resolution scale.**  For a smooth state, nearest-neighbour potential differences shrink with `h`, so the operator current also shrinks.  Dividing the current by `h` produces a quantity that approaches a stable continuum value.  At n=20 it is about 2% from the n=24 result, whereas raw mean J is still about 18% away.

4. **Normalized local directional observables converge much faster.**  Direction entropy, concentration and antipodal orientation are already much less resolution-sensitive than raw current magnitude.  This is consistent with the ratio-based alpha/beta structure being closer to a continuum-native description.

5. **Update count must be treated as a numerical discretization parameter.**  Keeping the same number of updates at every resolution compares different amounts of local propagation.  The control `steps*h = const` substantially improves the meaning of a refinement comparison.  It is not a physical-time definition.

6. **Grid orientation is not physics in this control.**  Computational-axis permutation gives the same P/J trajectory after the isomorphism is mapped back.

## Consequence for the emergent-calibration program

The experiment supports the three-stage calibration architecture:

`grid representation -> continuum/state invariant -> physical observable`

rather than direct `grid quantity -> physical quantity` calibration.

For the actual model the next step is to replace the known control weight `h^4` with a candidate state-dependent quadrature weight `w_i(P,J)` and demand the same refinement invariance.  The same principle applies to direction-space weights.  No such weight is chosen here because its definition is still an open part of the theory.

Likewise this run does not yet define `d_em`, `V_em`, `E_em`, `M_em`, or `tau_em`.  It establishes a practical falsification criterion for any future candidate: equivalent refinements and representations must converge to the same value.
