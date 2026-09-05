# Newton–Minkowski–GR object-optimized series

Date: 2026-09-05

## Methodological constraint
The self-reflexive operator was left unchanged. No force law, inertia term, Lorentz law, curvature law, damping, stabilization, synchronization term, or physical constant was added. The experiment varied only teacher information content and readout depth.

For refinement controls a periodic dense 4D reference domain was used to isolate the live-neighbour algebra from boundary/birth effects. This is a numerical control representation, not physical geometry.

## Object classes

### N object — compact centroid-readable teacher
A compact approximately isotropic P/J object was translated during training with fixed internal geometry. It was optimized only for a low-order point-object readout: excess-P centroid and post-release displacement.

### M object — 4D phase/orientation teacher
A richer anisotropic object with internal phase, fourth-direction width modulation, and external translation was used. The same continuous teacher was also axis-permuted (x <-> w). Raw P/J outputs were mapped back and compared, while the selected 3+1 readout was intentionally kept fixed.

### G object — dynamic high-information teacher
A teacher with translation, internal rotation/shape phase, fourth-direction pulsation, and preserved environmental memory was compared with lower-information objects and with a mock teacher that repeatedly overwrote the full P field.

Teacher hierarchy:
- O0: static localized object
- O1: internal pulsation
- O2: translation + pulsation
- O3: translation + pulsation + internal rotation/4D phase structure

The dynamic teacher was applied incrementally (`current P += target(s)-target(s-1)`) so operator-generated environmental P/J memory survived. The mock control repeatedly replaced the complete P frame.

## 1. Newtonian-limit test

Across n = 12, 14, 16 the trained centroid velocity was stable:

| n | trained centroid slope | first free displacement | velocity retention |
|---:|---:|---:|---:|
| 12 | 0.024016 | 0.004008 | 0.1669 |
| 14 | 0.024299 | 0.003169 | 0.1304 |
| 16 | 0.024472 | 0.001824 | 0.0745 |

After release the object retained only about 7–17% of the trained translational rate in the first free frame, and the centroid subsequently relaxed and eventually reversed rather than continuing inertially.

### Interpretation
The object is readable as a low-order mass-point-like centroid, but the present operator/teacher representation does **not** produce a genuine Newtonian inertial object. The failure becomes stronger under refinement, so this is not explained by coarse-grid error alone.

Status: **negative for emergent Newtonian inertia in this object class**.

## 2. Minkowski-level 4D invariance test

The same M teacher was permuted by exchanging x and w, evolved with the unchanged operator, and mapped back.

Resolution controls:

| n | max raw equivariance error | raw q-norm difference |
|---:|---:|---:|
| 12 | 5.81e-10 | 2.57e-13 |
| 14 | 1.49e-11 | 1.38e-15 |
| 16 | 9.54e-11 | 7.91e-14 |

At n=14 the raw q norm was identical after permutation to displayed precision, while the fixed 3+1 readout changed, e.g. at release:

- base 3+1 ratio: ~1.078
- x<->w-permuted 3+1 ratio: ~0.829

The raw 4D state therefore remains essentially invariant while the selected projection/readout changes.

### Interpretation
This is the strongest result of the series. It supports the hierarchy:

`raw R4 P/J dynamics -> state/readout-selected 3+1 decomposition`

rather than a fundamental time axis built into the operator.

Status: **strong structural positive for Minkowski-like 4D invariance**, but no Lorentz metric or physical invariant has yet been derived.

## 3. GR-level teacher-information-depth test

At n=14 after release and free evolution, the higher-order local variation readout clearly separated low-information and high-information teachers.

Representative free-frame-8 global gradient-like readout:

- O0 static: 0.00454
- O1 pulse: 0.00432
- O2 move+pulse: 0.01002
- O3 full dynamic: 0.01182

Representative core-local readout at free frame 8:

- O0 static: 0.01381
- O1 pulse: 0.01291
- O2 move+pulse: 0.12994
- O3 full dynamic: 0.16488

Thus adding mere pulsation did not automatically increase the higher-order signal, while adding coherent external motion and richer internal phase structure did.

This is important: readout complexity did not simply track 'more parameters'; it tracked specific relational/dynamical information.

## 4. Real-vs-mock control

The O3 teacher was run in two modes:

1. **dynamic/incremental:** only the next teacher-state difference was added, preserving environmental memory;
2. **mock/overwrite:** every teacher frame replaced the full P field, destroying most accumulated environmental P memory.

At release the difference was modest, but during free evolution the high-order local distinction increased strongly. At n=14 the core-gradient ratio `real/mock` evolved approximately:

1.34, 1.60, 1.98, 2.42, 2.83, 3.45, 3.67, 3.89, 3.52

across free frames 0..8.

The corresponding low-order/global 3+1 ratios differed much less.

### Interpretation
Geometrically similar teacher frames are not dynamically equivalent. Preserved relational history creates information that becomes visible mainly in higher-order readouts.

This supports the proposed distinction:

`particle-looking mock != dynamically admissible object orbit`

and the methodological rule:

`readout complexity <= teacher relational information content`.

## 5. Resolution dependence of the G signal

The dynamic-vs-mock distinction survives n = 12, 14, 16, but its absolute amplitude and ratio are not monotonic. Example core `real/mock` ratio after six free frames:

- n=12: 3.68
- n=14: 1.48
- n=16: 2.06

Therefore the G-level result is currently structural, not quantitatively converged.

Likely cause remains the same as in prior refinement tests: higher-order pointwise/RMS derivatives are sensitive to active/inactive flow surfaces created by `(Delta P)_+`. A surface/integral functional is likely a better continuum readout candidate.

## 6. Coarse-graining result: G -> M -> N

The same high-information O3 teacher can be read at three depths:

- N readout: object centroid / coarse point-object motion;
- M readout: global 3+1 directional ratio and raw 4D orientation invariants;
- G readout: local higher-order object-environment deformation.

The real-vs-mock difference is weakest in low-order global descriptors and strongest in local high-order descriptors. This is qualitatively the expected information hierarchy.

However, because the N-level free inertial continuation fails, the current O3 object is **not yet a single self-consistent object that simultaneously reproduces valid N, M, and G limits**.

## Overall assessment

### Newtonian
- centroid/object readout: yes
- inertial continuation: no
- refinement trend: negative

### Minkowski
- raw 4D directional equivariance: extremely strong
- 3+1 projection dependence: yes
- physical Lorentz invariant: not yet derived

### GR-like
- object dynamics -> persistent local higher-order environmental deformation: yes
- dynamic teacher > geometric mock after release: yes
- quantitative continuum convergence: not yet

## Main conclusion
The experiment supports the proposed information-depth hierarchy more strongly than it supports any specific physical theory:

`simple object -> low-order point readout`

`4D oriented dynamic object -> strong R4 invariant / 3+1 projected readout`

`history-rich dynamic object -> higher-order object-environment deformation`

The main failure is equally important: a compact moving teacher still does not become an autonomous Newtonian inertial object after release. Therefore the next decisive step is not to add an inertia law, but to search for an operator-admissible self-maintaining P/J orbit whose low-order coarse-graining has inertial persistence.

No operator modification is justified by this experiment.