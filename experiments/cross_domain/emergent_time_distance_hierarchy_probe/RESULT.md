# Emergent time–distance hierarchy probe — result

## Aim
Search for **candidate** emergent distance/time readouts built only from the unchanged P/J dynamics and its derived alpha/beta characteristics, while respecting the previously defined relational hierarchy:

- first-order relation: local directed transport / velocity-like readout,
- second-order relation: variation of the first-order readout / acceleration-like readout,
- third-order relation: variation of the second-order readout / higher dynamical-curvature readout.

No Euclidean, Minkowski or GR metric was inserted into the operator. These are external structural benchmarks only.

## Operator
Unchanged scanner operator:

`alpha_ij = Delta_ij / sum_k Delta_ik`

`beta_ij = Jprev_ij / sum_k Jprev_ik`

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

No stabilizer, force law, inertia, damping, metric, speed of light or synchronization law was added.

## First-order characteristic
For each local direction `a`, the dimensionless self-reflexive transport characteristic was taken directly from the operator factor

`kappa_a ~ alpha_a / (1 + beta_a)`

and normalized over live directions. Its signed 4D orientation vector is the weighted sum of the local direction representatives.

A pure homogeneous directed reference state determines a coherent local axis `n_t`. This axis is **not declared physical time**; it is only the candidate complementer direction for the 3+1 projection test. The component of the normalized local transport characteristic parallel to `n_t` is `T`, and the magnitude of its orthogonal three-dimensional component is `S`.

Two local bounded candidate shares were then tested:

`D1 = S / (S + T)`

`Theta1 = T / (S + T)`

so that `D1 + Theta1 = 1` wherever there is active directed transport. This identity is a construction property and is therefore **not evidence** for physical spacetime complementarity; the test is whether the same pair remains useful across the E→M→G hierarchy and under object-induced distortion.

The raw reciprocal candidate

`v_raw = S / T`

was tested separately and rejected as a universal readout because it becomes singular on local surfaces where the time-like component tends to zero.

## Test A — homogeneous directed family (Minkowski-like structural benchmark)
A smooth affine P field was oriented at angles from 0° to 85° between the coherent complementer direction and one orthogonal direction. With beta initially zero, the first-order candidate gave:

| angle | D1 | Theta1 | S/T |
|---:|---:|---:|---:|
| 0° | 0.0000 | 1.0000 | 0.0000 |
| 10° | 0.1499 | 0.8501 | 0.1763 |
| 20° | 0.2668 | 0.7332 | 0.3640 |
| 30° | 0.3660 | 0.6340 | 0.5774 |
| 45° | 0.5000 | 0.5000 | 1.0000 |
| 60° | 0.6340 | 0.3660 | 1.7321 |
| 75° | 0.7887 | 0.2113 | 3.7321 |
| 85° | 0.9195 | 0.0805 | 11.4301 |

For the homogeneous affine family, all second- and third-order relational variation descriptors were zero to numerical precision. Thus the same readout produces a pure first-order kinematic regime without artificial higher-order structure.

### Interpretation
This supports using the bounded pair `(D1, Theta1)` as a **first-order candidate family**. It has the desired opposite variation and gives a monotonic velocity-like ratio, but no claim is made that `D1`, `Theta1` or `S/T` are already physical distance, time or velocity.

## Test B — localized object on the same directed background (GR-like structural benchmark)
A smooth localized 4D P bump was added to the 30° homogeneous directed background and the exact raw operator was evolved freely. The object amplitude was swept through

`0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.80, 1.20`.

After two free steps, the bounded first-order shares developed local center-versus-far distortions. Representative results:

| bump amplitude | center−far D1 | center−far Theta1 | center A2 | far A2 | center J3 | far J3 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 0.05 | +0.0284 | -0.0284 | 0.0427 | 0.0197 | 0.0154 | 0.0087 |
| 0.10 | +0.0595 | -0.0595 | 0.1055 | 0.0372 | 0.0405 | 0.0143 |
| 0.20 | +0.0480 | -0.0480 | 0.1216 | 0.0698 | 0.0487 | 0.0257 |
| 0.35 | -0.0221 | +0.0221 | 0.0780 | 0.0812 | 0.0334 | 0.0344 |
| 0.50 | -0.0176 | +0.0176 | 0.0962 | 0.0690 | 0.0181 | 0.0356 |
| 0.80 | +0.0027 | -0.0027 | 0.1170 | 0.0620 | 0.0087 | 0.0313 |
| 1.20 | +0.0151 | -0.0151 | 0.1309 | 0.0648 | 0.0094 | 0.0297 |

Here `A2` is a second relational difference of the bounded first-order readout along the candidate complementer relation, and `J3` is the corresponding third relational difference. They are graph-order diagnostics, not yet physical acceleration and jerk.

### Interpretation
The important structural result is not monotonicity with bump amplitude — that is not observed globally — but hierarchy separation:

- homogeneous directed background: first-order signal only;
- localized object: first-order local distortion plus nonzero second- and third-order relation terms;
- the distance-like and time-like bounded shares distort with opposite sign by construction while the higher-order terms are generated only by inhomogeneous object structure.

This is consistent with the intended idea that lower-order projected physics can look kinematic, while higher-order relational resolution is required to see object-induced geometry/dynamics.

## Test C — relation-shell extent / scale dependence
The same localized object was tested with different smooth widths. Using relation-shell number only as a **representation diagnostic**, not as physical distance, broader objects produced distortions over more graph shells. For example after two free steps with amplitude 0.2:

- narrow width 0.8: third-order signal decreased from about 0.158 at the core to about 0.0047 by shell 6;
- width 1.5: first/second-order distortion remained substantial through shells 4–6;
- width 2.0: the distortion remained broad across the full measured region.

Thus local object-induced P/J characteristic changes can become effectively global on a finite observed subsystem as the object/background scale ratio grows. This is a structural analogue only; relation-shell count is not emergent physical radius.

## Test D — continuum/refinement behavior of naive higher derivatives
The same smooth continuum reference field was sampled at increasing numerical resolution. The bounded first-order `D1` changed smoothly with refinement, but naive pointwise second/third derivatives of the normalized alpha/beta direction field did **not** show clean convergence. In a representative refinement series (`n=9,13,17`), the local derivative means increased instead of stabilizing.

This occurs near surfaces where the active downhill direction set changes and the normalized alpha characteristic is only piecewise smooth.

### Consequence
The naive rule

`higher physical order = repeated pointwise derivative of normalized alpha/beta direction`

is **rejected** as a universal continuum construction.

This is not a fatal contradiction for the model because the relational hierarchy already allows partial derivatives **and** integrals/surface terms. Integrated variation measures behave much better.

A numerical total-variation density of `D1`, scaled as a continuum integral, showed a progressively flattening sequence:

| n | h | mean D1 | integrated first variation density | integrated second variation density |
|---:|---:|---:|---:|---:|
| 9 | 0.5000 | 0.6472 | 0.2632 | 0.8089 |
| 13 | 0.3333 | 0.6590 | 0.3279 | 1.2219 |
| 17 | 0.2500 | 0.6536 | 0.3762 | 1.4487 |
| 21 | 0.2000 | 0.6461 | 0.4027 | 1.5792 |
| 25 | 0.1667 | 0.6393 | 0.4190 | 1.6676 |
| 29 | 0.1429 | 0.6336 | 0.4295 | 1.7277 |
| 33 | 0.1250 | 0.6290 | 0.4370 | 1.7731 |

This is not yet a demonstrated continuum limit, but it is much more compatible with a surface/integral higher-order construction than with repeated local derivatives.

## Test E — global vs local time
The earlier growing-domain birth tests remain relevant:

- total P was conserved;
- active 4D support could grow monotonically;
- Shannon-type entropy was **not** universally monotonic.

Therefore the current hierarchy is most consistent with keeping two separate time notions:

1. a global clock candidate tied to growth of the active 4D measure / global dilution;
2. a local clock-rate candidate tied to the bounded complementer share and possibly local entropy/distribution change.

Entropy alone is rejected as universal global time.

## Current candidate hierarchy
The strongest surviving architecture is therefore:

### Order 1 — local kinematic readout
From the operator characteristic `alpha/(1+beta)` construct a dimensionless local 4D transport orientation. Relative to an emergently selected coherent complementer direction, split it into bounded spatial-like and time-like shares `(D1, Theta1)`.

Projected 3+1 interpretation: velocity-like / local clock-rate-like quantities may be monotonic functions of these shares.

### Order 2 — object/inhomogeneity response
Do **not** use a raw repeated pointwise derivative everywhere. Use graph partial derivatives where smooth, supplemented by integrated or surface variation across direction-switch / characteristic boundaries.

Projected 3+1 interpretation: acceleration-like and local geometry-distortion-like quantities.

### Order 3 — higher feedback / curvature-dynamics response
Use variation of the second-order integrated/surface characteristic, again representation-invariant and refinement-tested.

Projected 3+1 interpretation: higher dynamical response / curvature-evolution-like behavior, not yet a specific GR tensor.

## Falsification status
### Rejected candidates
- `v_raw = S/T` as a universal velocity/distance readout because of local singularities;
- entropy alone as global emergent time;
- repeated naive pointwise derivatives of normalized alpha/beta as universal second/third-order continuum observables.

### Not falsified
- a bounded complementary first-order distance/time share derived from the local self-reflexive transport characteristic;
- global time from active 4D measure growth/dilution with local clock-rate modulation;
- a relational hierarchy in which higher orders require integral/surface terms at alpha/beta characteristic boundaries;
- object-induced local distortion that becomes larger-scale as the object/background relation scale increases.

## Strongest justified conclusion
The unchanged operator supports a nontrivial **hierarchical readout architecture**: a smooth homogeneous directed state is first-order/kinematic; localized object structure creates higher relational orders and local distortion; but the continuum mathematics cannot be a simple repeated derivative of normalized alpha/beta. Surface/integral terms appear structurally necessary.

This is compatible with the project goal of constructing a possible P/J physics, but it does not yet identify unique mathematical formulas for emergent distance or time.
