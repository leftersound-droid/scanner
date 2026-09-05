# Euclidean–Minkowski–GR teacher-depth / grid-calibration series

Date: 2026-09-05

Status: exploratory structural test. The self-reflexive operator is unchanged. No Euclidean metric, Minkowski metric, GR equation, inertial law, force law, damping, stabilizer, or synchronization law is inserted into the dynamics.

## Question

Test the hypothesis that the same fixed P/J operator can support increasingly rich physical analogues when the **teacher/input information depth** and **readout relational order** are increased:

- E-level: homogeneous/weakly perturbed state, grid coordinates and iteration used only as external calibration references;
- M-level: homogeneous dynamical 4D state, testing coordinate/direction invariance and a state-derived 3+1 readout;
- G-level: richer teacher carrying internal shape dynamics plus external motion, testing whether object dynamics produces local deformation in the same readout family.

A second goal is to locate where the input-to-grid mapping itself becomes the dominant source of error.

## Operator

Unchanged live-neighbour rule:

```text
Delta_ij = (P_i - P_j)_+
alpha_ij = Delta_ij / sum_k Delta_ik
beta_ij  = Jprev_ij / sum_k Jprev_ik
C_i      = mean positive Delta_ij
J_ij     = C_i * alpha_ij / (1 + beta_ij)
```

The numerical domain is periodic in this probe to remove boundary/birth contamination.

---

## E-level: grid as calibration reference, not ontology

### Input

A weak smooth 4D periodic reference field was sampled at resolutions n = 8,10,12,14,16,18,20,22.

The first-order flux density `J/h` was used as a representation-calibrated local readout. Four dimension activities were compared.

### Raw point-sampling result

For a single fixed grid alignment, the mean dimension activity oscillated with resolution, approximately

```text
0.04094, 0.04712, 0.04087, 0.04527,
0.04074, 0.04426, 0.04064, 0.04342
```

Across the full series the coefficient of variation was about 5.4% (about 3.8% over the last four resolutions).

The four coordinate directions remained mutually equal to numerical precision within each run, so the error is not directional symmetry breaking; it is grid/input phase aliasing.

### Sub-cell translation / representation averaging

The same continuous field was then sampled at eight sub-cell translations for every resolution and the readout averaged over these equivalent embeddings.

The mean `J/h` values became

```text
n=8   0.0412751
n=10  0.0413078
n=12  0.0412476
n=14  0.0410951
n=16  0.0410814
n=18  0.0409437
n=20  0.0409340
n=22  0.0408717
```

This is a much tighter convergence trend (~1% change from the coarse phase-averaged value to n=22).

### Interpretation

This supports the user's proposed role for the Euclidean level:

- the numerical grid can be used as an **axiomatic calibration ruler/clock** in the lowest-complexity regime;
- it must not be identified with physical space/time;
- an emergent candidate should approach a simple linear mapping to the grid reference in a homogeneous limit;
- the continuous input must be mapped to the grid in a representation-neutral way.

The first clear E-level grid problem is therefore **sub-cell phase / sampling aliasing**. A single point-sampled embedding can shift the measured first-order readout by several percent even though the underlying continuous state is unchanged.

---

## M-level: 4D invariance and 3+1 projection

### Input

A smooth homogeneous-dynamical 4D field with distinct amplitudes along all four coordinate directions was used. No coordinate was designated as physical time by the operator.

### Exact coordinate-permutation control

At n=14 the initial field was transformed by swapping the first and fourth coordinate axes, including the corresponding direction-channel labels. After one unchanged operator frame, the permuted result was mapped back.

Result:

```text
max |Delta P| = 2.220446049250313e-16
max |Delta J| = 0
```

Thus the numerical dynamics is equivariant under the tested 4D axis permutation to machine precision.

### Refinement of first-order 4D activities

For n = 8..20 the representation-scaled per-dimension current activities `q_a = J_a/h` approached stable values corresponding to the imposed continuous directional content. The 4D activity norm stayed near 0.055, while a selected 3+1 projected spatial/time-like activity ratio stayed of order 0.88–0.91 after the coarsest grid.

The projection-dependent ratio is not itself a Lorentz invariant; the important result is that the full four-direction P/J state transforms exactly under coordinate relabeling, while a 3+1 split can be applied afterward as a readout.

### Interpretation

This is the strongest current structural analogy:

```text
4D state/dynamics is coordinate-direction invariant
        ->
3+1 distinction must be selected by state/readout, not hard-coded geometry
```

This is compatible with a Minkowski-like research path, but no Minkowski metric or Lorentz transformation law has yet been derived.

---

## G-level: teacher information depth and object-generated deformation

### Rich teacher

A closed teacher cycle was built from a smooth localized 4D object whose state contained simultaneously:

- external periodic motion of the center in the projected R3 plane;
- internal rotation of an anisotropic profile;
- pulsation of the fourth-direction width;
- a nontrivial background first-order P/J state.

This is teacher information only. No inertial equation or force law is inserted.

### Failed teacher representation: full-frame overwrite

First, every teacher phase replaced the entire P field.

Result: the dynamic-cycle teacher and a repeated static teacher produced nearly identical free behavior.

Reason: full-frame replacement erased the environment's P memory every phase. Only the most recent normalized J-direction distribution could survive through `beta`. This made the supposedly deeper teacher effectively shallow.

This is an input-representation failure, not evidence against object-dynamics/geometry coupling.

### Refined teacher representation: delta teacher on evolving environment

The test was repeated with

```text
P_current <- P_current + [P_teacher(s+ds) - P_teacher(s)]
```

before each operator frame.

This makes the teacher specify only the intended state change while leaving the operator-evolved background P/J memory present. The closed teacher cycle has zero net teacher-state difference over one complete cycle apart from numerical sampling.

Resolutions tested: n=10,12,14,16. After the teacher cycle, the teacher was removed and six free operator frames were measured.

### First free frame: dynamic vs static teacher

The integrated 3+1 activity ratio changed only modestly but systematically:

```text
relative dynamic/static excess:
 n=10  +2.63%
 n=12  +3.20%
 n=14  +1.51%
 n=16  +1.79%
```

The absolute dynamic ratio had about 3.35% coefficient of variation across these resolutions; the static control about 2.89%.

Higher-order/local deformation was much more sensitive to teacher history. The local first-variation readout around the object was larger in the dynamic teacher case by factors:

```text
n=10  10.45 x
n=12   6.15 x
n=14   4.24 x
n=16   3.27 x
```

The local D/T-field standard deviation was also larger (roughly +52% to +186%, depending on resolution), and object-region P contrast was about twice the static control.

### Six free frames later

The dynamic-history excess persisted but relaxed:

```text
integrated 3+1 ratio excess:
 n=10  +0.52%
 n=12  +1.84%
 n=14  +1.89%
 n=16  +0.86%
```

The local first-variation readout remained about

```text
2.27 x to 2.80 x
```

larger than the static-teacher control.

Thus the richer teacher can write a distinguishable, decaying local environmental/object state when the input mapping preserves P memory.

### Important limitation

The numerical magnitude of the higher-order local derivative readouts does **not** yet converge. Their absolute value grows with resolution because the `(Delta P)_+` directional activation introduces increasingly sharp active/inactive flow surfaces. Therefore local RMS/pointwise derivatives are not yet valid continuum observables for the GR-like layer.

This reproduces the earlier conclusion that higher relational order probably needs surface/integrated functionals rather than naive pointwise derivative norms.

---

## Hierarchy assessment

### E — low relational depth

**Analogy quality: strong as a calibration structure, not yet as an emergent metric.**

- homogeneous directional equality is excellent;
- `J/h` has a sensible continuum scaling;
- single-grid alignment creates several-percent aliasing;
- representation-averaged sampling tightens the result to approximately the 1% level.

The Euclidean benchmark is therefore useful precisely because it exposes whether an emergent quantity is sufficiently well defined before object complexity is added.

### M — medium relational depth

**Analogy quality: currently strongest.**

- exact tested 4D coordinate permutation equivariance;
- stable first-order continuum-scaled activities;
- 3+1 split can be treated as a readout of the state rather than an operator axiom.

No actual Lorentz/Minkowski invariant has yet been derived, so this remains structural rather than a reproduction of SR.

### G — high relational depth

**Analogy quality: positive qualitative structure, weak quantitative closure.**

- richer object dynamics affects the same local P/J-derived kinematic/geometric readout after teacher removal;
- the effect is much stronger locally than globally;
- the effect survives multiple free frames but relaxes;
- correct teacher/environment memory handling is essential;
- current second/third-order pointwise norms are grid-sensitive and not yet continuum-calibrated.

This satisfies a necessary GR-like structural condition:

```text
internal/external object dynamics
        ->
local deformation/history in the same underlying P/J state
```

but it is not a GR derivation and does not yet demonstrate a scale-propagating metric field.

---

## Where the grid/input problem appears

The experiment separates four distinct problems:

1. **Sub-cell embedding aliasing (E level).** A fixed continuous field gives measurably different readouts depending on its phase relative to the grid. Translation/embedding averaging largely removes it.
2. **Object-size misrepresentation.** Keeping an object at a fixed number of cells while refining the grid changes the represented object; teacher quantities must be defined in continuous/emergent ratios first, then sampled.
3. **Teacher overwrite / memory erasure (G level).** Replacing the whole P frame destroys environment memory and collapses a deep teacher to almost one-frame beta information.
4. **Higher-order norm mismatch.** Naive pointwise/RMS derivatives can diverge on increasingly sharp active-flow surfaces even if an integrated/surface measure remains finite.

None of these currently requires changing the operator.

---

## Main conclusion

The results support the proposed information-depth hierarchy:

```text
E: axiomatic reference geometry / minimal state information
       -> emergent readout should approach a simple grid calibration

M: full 4D directional state with state-selected 3+1 projection
       -> exact tested 4D permutation invariance and stable first-order readout

G: teacher with internal dynamics + external motion + environment memory
       -> local higher-order deformation/history appears, but its continuum readout is unresolved
```

The present evidence is therefore **not** that one fixed formula already reproduces Euclidean, Minkowski and GR geometry. The stronger supported statement is that the same unchanged operator displays a hierarchy of increasingly complex state/readout behavior when the teacher information content is increased, and the main failures encountered so far are traceable to representation/readout choices rather than a fatal contradiction in the operator.

## Next falsification target

For the G layer, replace pointwise derivative norms with representation-invariant surface/integral functionals and test whether the dynamic/static teacher deformation ratio converges under spatial refinement and directional refinement. A failure of every such graph-native/integrated higher-order functional to converge would be a serious structural problem for the GR-like branch.