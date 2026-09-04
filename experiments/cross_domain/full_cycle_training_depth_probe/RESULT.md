# Full-cycle training-depth probe — result

## Question
Does the unchanged self-reflexive P/J operator preserve a taught periodic rotation more accurately when the same full cycle is taught with finer phase sampling and/or repeated for more complete cycles?

## Scope
This is a **structural memory probe**, not yet the final emergent-coordinate teacher test. A synthetic compact 4D P/J object is represented on a periodic 4D lattice only to remove boundary/birth contamination. The teacher acts locally on the object core; the surrounding P/J state is **not reset**, so repeated cycles can leave history in the environment.

No inertia, angular-momentum law, torque, damping, stabilizer, or physical metric is added. The local live-neighbour transfer algebra remains

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

with `alpha` from current positive P differences and `beta` from normalized previous-flow distribution.

## Teacher
One taught rotation is a complete 2pi cycle of a compact threefold-marked ring-like P object with a corresponding local tangential J component and a longitudinal fourth-direction phase component.

Two training-depth axes were varied:

- phase resolution per full cycle: `N_phi = 8, 16, 32, 64`
- repeated full cycles: `N_cycle = 1, 2, 4, 8` (64-phase pilot run used 1,2,4 cycles)

After training, all teacher forcing is removed and the object is evolved freely for one nominal cycle length.

## Primary release diagnostic
The external marker phase is followed only as a representation diagnostic. The important quantity is the fraction of the expected one-cycle orientation progression that survives after release:

`phase_progress_ratio = observed free phase progression / expected progression`

A value near 1 would indicate continuation of the taught rotation; 0 indicates no continuation.

## Results

| N_phi | N_cycle | free phase continuation ratio | marker amplitude start | marker amplitude end |
|---:|---:|---:|---:|---:|
| 8 | 1 | -0.018 | 0.0719 | 0.0185 |
| 8 | 2 | -0.030 | 0.0602 | 0.0173 |
| 8 | 4 | -0.038 | 0.0481 | 0.0169 |
| 8 | 8 | -0.042 | 0.0367 | 0.0159 |
| 16 | 1 | +0.177 | 0.0605 | 0.0060 |
| 16 | 2 | -0.167 | 0.0414 | 0.0089 |
| 16 | 4 | -0.160 | 0.0261 | 0.0106 |
| 16 | 8 | -0.153 | 0.0149 | 0.0115 |
| 32 | 1 | +0.144 | 0.0465 | 0.0152 |
| 32 | 2 | +0.142 | 0.0299 | 0.0149 |
| 32 | 4 | +0.138 | 0.0177 | 0.0147 |
| 32 | 8 | +0.129 | 0.0104 | 0.0144 |
| 64 | 1 | +0.125 | 0.0354 | 0.0157 |
| 64 | 2 | +0.119 | 0.0226 | 0.0155 |
| 64 | 4 | +0.110 | 0.0149 | 0.0153 |

## Interpretation
### 1. Minimum one full cycle matters, but finer phase sampling alone does not produce autonomous rotation
The 8-phase training gives essentially no forward continuation. At 16–64 phase samples, some orientation memory appears, typically about 11–18% of one expected free cycle. Therefore the released dynamics is sensitive to training resolution.

However, the continuation does not converge toward 100% as `N_phi` increases. The 32- and 64-phase cases are not better than 16 in a monotonic way.

### 2. Repeating complete cycles does not improve memory monotonically
For fixed phase resolution, increasing `N_cycle` from 1 to 2,4,8 does not systematically improve the free orbit. In most families the continuation stays similar or becomes worse. Thus there is no evidence here for cumulative multi-cycle learning under the current raw operator.

### 3. The environment really was allowed to retain history
The teacher was applied only to the local object core. The surrounding P/J field evolved continuously and was not reset between cycles. Therefore the absence of monotonic multi-cycle improvement cannot be explained by resetting the environment each cycle.

### 4. The taught marker itself relaxes strongly
The m=3 marker amplitude decreases substantially during the free stage in every case. Hence the released state is not a rigidly rotating invariant object; it relaxes/diffuses while retaining at most a limited phase bias from the taught history.

## Structural consequence
The current operator contains only one-frame explicit J memory through normalized `beta`. Repeated history may be present indirectly in the surrounding P distribution, but this pilot shows that this is not sufficient to reconstruct a complete taught periodic orbit with increasing fidelity.

The supported statement is therefore:

> Under the present raw operator, teaching one or more complete rotation cycles with finer sampling leaves a measurable but limited phase-history bias; it does not produce a self-sustaining rigid periodic rotation, and repeated complete cycles do not yield monotonic fidelity improvement.

## What is not falsified
- the broader hypothesis that a stable object requires at least one complete taught period;
- a different P/J phase-orbit teacher defined directly in emergent coordinates rather than by a lattice marker;
- a deeper state representation in which more than the normalized previous-flow distribution survives locally;
- a stable object whose internal P/J cycle itself regenerates the external rotation rather than merely storing an imposed tangential J.

## Next decisive test
The next test should remove the remaining grid-fixed teacher analogy. Instead of prescribing a rotating image, define the teacher by a sequence of **emergent invariant states** over one closed cycle, then test whether increasing invariant-state sampling density improves release fidelity. If repeated cycles still do not improve fidelity, the limitation is much more likely to lie in the current memory structure of the operator itself.
