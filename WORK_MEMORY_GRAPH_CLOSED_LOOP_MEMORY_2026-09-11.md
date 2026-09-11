# Work memory — graph-level closed-loop perturbation / memory test

Date: 2026-09-11
Status: pilot result, drift-corrected; no operator change.

## Goal

The model is fundamentally graph-based, so the next step after the nonlinear Q-manifold test was reframed from a generic Q-space hysteresis test into a graph-level closed-loop perturbation experiment.

Question:

Does a closed external P-only perturbation loop leave a residual relational graph state after the perturbation returns to zero, beyond the graph's ordinary free drift?

## Constraints

- Fixed self-reflexive operator.
- P-only external probe.
- J never externally forced.
- No damping, force, threshold, physical law, or stabilizer added.
- Numerical lattice and update index remain scanner variables, not physical space/time.
- Memory means characteristic persistence through state transformation, not exact state replay.

## Setup

16^4 scanner pilot using the same asymmetric m=3 object/background family as the previous effective-state experiments.

Two probe channels were selected because the previous nonlinear response-manifold scan showed strong separation:

1. tangential m=1 P-only probe,
2. radial/w-gradient P-only probe.

Closed control sequence:

0 -> +A -> 0 -> -A -> 0

with A = 0.005, using intermediate amplitudes and four unchanged operator updates at each plateau.

The state was continuous through the full loop; it was not reset between amplitudes.

## Readouts

Alongside the previously defined Q-state, graph-level readouts were measured:

- object-weighted P mean,
- object-weighted P variance,
- local J directional entropy,
- global J_R3/J_w,
- opposite-direction edge imbalances for x,y,z,w,
- J-edge participation ratio.

These are readouts only.

## Critical control

The raw loop showed large apparent non-return, but this cannot be interpreted as hysteresis because the object also evolves freely during the loop.

Therefore a matched no-probe trajectory was run for exactly the same number of operator updates and sampled at the same points.

All memory claims below refer only to residual differences relative to this matched free-evolution control.

## Drift-corrected results

Tangential m=1 probe:

- residual Q norm at mid zero: 1.923749
- residual Q norm at final zero: 0.519730
- residual graph norm at mid zero: 16.056248
- residual graph norm at final zero: 2.147734
- residual joint final norm: 2.209724
- residual PC1-PC2 loop area: 70.481191
- residual path length in first three PCs: 166.851199

w-gradient probe:

- residual Q norm at mid zero: 6.278223
- residual Q norm at final zero: 0.215976
- residual graph norm at mid zero: 12.748922
- residual graph norm at final zero: 5.437845
- residual joint final norm: 5.442133
- residual PC1-PC2 loop area: 31.846585
- residual path length in first three PCs: 203.526572

The residual response remains strongly low-dimensional:

- tangential m1: PC1 ~59.8%, PC1+2 ~88.4%
- w-gradient: PC1 ~68.7%, PC1+2 ~96.1%

## Component-level final graph residuals

Relative to the matched free control at the same final update:

Tangential m1:

- Pmean_obj: -0.0096%
- Pvar_obj: -1.09%
- J directional entropy: +1.49%
- global J_R3/J_w: -0.77%
- edge participation ratio: -0.087%

w-gradient:

- Pmean_obj: -0.0015%
- Pvar_obj: +0.62%
- J directional entropy: -0.11%
- global J_R3/J_w: -0.28%
- edge participation ratio: -0.197%

Directional imbalance channels show much larger relative residuals, but their baseline values are near zero, so relative percentages there are numerically misleading. They must be analyzed using absolute residuals or a scale independent of a near-zero denominator.

## Interpretation

1. The raw non-return was mostly free evolution and could not be called memory.

2. After matched drift subtraction, a residual state remains. Therefore the closed P-only loop leaves a measurable relational graph history signal beyond ordinary free drift.

3. The residual is not mainly stored in bulk scalar quantities. P mean, edge participation and global R3/w flow return very close to the matched control.

4. The stronger residual appears in organizational/directional graph structure. This is consistent with the project's working memory hypothesis:

   memory != state copy

   memory = partial preservation of relational characteristics through changing microstates.

5. The radial w-gradient leaves a larger final graph residual than the tangential m1 loop in this pilot (5.44 vs 2.15 normalized graph norm), while tangential m1 produces a larger residual loop area in the reduced joint state geometry.

6. This is not yet proof of physical hysteresis or a stable particle memory law. It is a scanner-level graph-memory candidate.

## Methodological consequence

The graph ontology should be treated as primary. Q is a coarse coordinate chart on graph-state space, not the fundamental state itself.

A better hierarchy is:

G_(P/J) -> graph-relational invariants -> low-dimensional Q/manifold -> later physical observables.

The next experiment should test whether the drift-corrected graph residual is robust under:

- loop amplitude,
- loop rate / plateau length,
- scanner resolution,
- phase of object preparation,
- reversing loop order,
- repeating multiple loops.

A genuine memory characteristic should scale reproducibly and survive these controls without requiring a new axiom.

## Generated data files

- graph_closed_loop16_timeseries.csv
- graph_closed_loop16_summary.csv
- graph_closed_loop16_zero_returns.csv
- graph_closed_loop16_relative_return.csv
- graph_closed_loop16_free_control.csv
- graph_closed_loop16_drift_corrected_timeseries.csv
- graph_closed_loop16_drift_corrected_summary.csv
- graph_closed_loop16_final_graph_residual.csv
