# Global R4 growth probe — emergent volume/time readout

## Purpose
Revisit the original one-singularity/global-growth branch using the current reconstructed self-reflexive P/J operator, while treating the lattice only as numerical bookkeeping rather than physical geometry.

## Operator
Exact `src/scanner/self_reflexive_operator.py` on branch `agent/scanner-v2-beta`, including the current live-neighbour alpha/beta coupling and missing-neighbour birth rule. No damping, threshold, force law, stabilizer, or post-teacher drive was added.

## Initial condition
A reproducible small random complex seed was used (random seed 1000): one central state plus 12 nearby active numerical labels, total P normalized to 1, with random P amplitudes and random initial directional J-memory. After initialization there was no external P or J write.

## Provisional emergent readouts
The numerical frame index and lattice coordinates were not treated as physical time or distance.

Effective state-volume candidate:

`V_em = exp(-sum_i p_i log p_i)`, with `p_i=P_i/sum P`.

Cross-check volume candidate:

`V_PR = (sum P)^2 / sum P_i^2`.

Emergent-time candidate:

`d tau_em = sum_edges J_ij / sum_i P_i`, accumulated along the free evolution.

These are provisional readouts, not final definitions.

## Run limit
The free sparse R4 evolution was run until the available execution window was exhausted (~50 s). This reached 32,744 active numerical states in 280 update frames. These counts are implementation diagnostics only, not physical volume/time.

Total P was conserved to numerical precision; maximum per-step conservation error was 0.

## Main emergent-readout result
Final:

- `tau_em = 26.2998`
- entropy effective volume `V_em = 12417.5`
- participation volume `V_PR = 9310.35`
- total flow `J_total = 0.042309`

The last 20% of **emergent tau**, rather than the last 20% of update frames, was analysed separately.

Within that late emergent-time window:

- `d V_em / d tau ≈ 1070.19`
- `d V_PR / d tau ≈ 777.11`
- `d J_total / d tau ≈ -0.002633`
- mean P fraction on numerical graph boundary ≈ `0.98538`
- mean state fraction on graph boundary ≈ `0.99389`
- mean effective number of used R4 axis pairs ≈ `3.9208 / 4`
- mean birth transfer per sampled frame ≈ `3e-6`, decreasing late in the run.

Thus the state-volume readouts continue to grow while total current slowly declines and birth transfer becomes very small.

## Topological connectivity check
A final-state active-neighbour-degree analysis was added as a purely graph-topological diagnostic.

- mean active degree (unweighted) = `3.94985`
- P-weighted mean active degree = `4.07616`
- ~94.08% of numerical states have degree 4
- ~97.42% of total P is carried by degree-4 states
- only ~0.49% of states are degree-8 bulk-like
- only ~1.28% of P is on degree-8 bulk-like states

The naive degree/2 local-dimension proxy is therefore about 2.0, **not** 3.0.

At the same time the directional current uses all four R4 axis pairs almost symmetrically (`axis_eff ≈ 3.92`).

## Interpretation
This first updated global-growth probe does **not** reproduce the desired R3 hyperslab strongly enough to call it a hyperslab.

It does, however, produce a strongly non-bulk, extremely boundary-dominated growing structure. The surprising feature is the combination:

1. almost all P lies on a numerical graph boundary;
2. local connectivity is sharply concentrated around degree 4 rather than degree 8;
3. current still uses all four R4 axis pairs nearly symmetrically.

The safest current description is therefore a thin, sparse, all-R4-oriented relational sheet/network with approximately degree-4 local connectivity, not an R3 hypersurface.

This is a useful negative/diagnostic result: with the present random seed class and current operator, the global free growth branch does not yet yield the originally expected R3 hyperslab.

## Next relevant tests
- repeat across independent random complex seed realizations to see whether the degree-4 state is generic or seed-specific;
- classify seed information as radial / tangential / mixed P/J and compare the emergent graph state;
- test convergence of `V_em(tau)` and the degree distribution under numerical refinement / alternate sparse embeddings without treating coordinate spacing as physical;
- search for a seed class that yields a stable degree≈6 P-weighted local connectivity before making any R3-hyperslab claim.
