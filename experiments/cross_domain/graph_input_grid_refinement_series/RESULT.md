# Graph hierarchy + input/grid refinement series

Date: 2026-09-05

Status: partial structural result / falsification series. The raw self-reflexive operator was not modified.

## Aim

Test two things together:

1. whether the previously defined relational hierarchy remains distinguishable under a single P/J, alpha/beta readout family;
2. where the mapping from emergent/continuous input state to a finite 4D scanner grid becomes the limiting factor.

The comparison deliberately separates a **naive grid input** from a **continuum/emergent-matched input**.

## Operator

Unchanged live-neighbour operator:

`Delta_ij = (P_i - P_j)_+`

`alpha_ij = Delta_ij / sum_k Delta_ik`

`beta_ij = Jprev_ij / sum_k Jprev_ik`

`C_i = mean(positive Delta_ij)`

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

No metric, force, damping, GR term, synchronization law, stabilizer, or physical constant was inserted.

## Test states

- **E**: homogeneous static P state.
- **M**: homogeneous first-order mixed 3+1 gradient with a fixed relative directional teacher characteristic.
- **G**: the same M background plus a localized 4D P/J object-like structure with a local tangential/longitudinal teacher characteristic.

The numerical domain is used only as a representation. Diagnostics are taken from the central region so that the periodic numerical boundary does not define the measured object.

## Two input mappings

### Naive grid mapping

The localized object width is kept fixed in **cell count** (`sigma ≈ 2 cells`). Therefore its continuum/emergent width shrinks as the grid is refined.

This is intentionally a wrong representation control.

### Continuum/emergent-matched mapping

The same smooth P profile is sampled at every resolution with a fixed width in the underlying continuous coordinate ratio (`sigma = 0.22` in the reference domain), while the directional teacher is sampled from the same continuous directional characteristic.

Finite differences are interpreted with the appropriate grid spacing `h`; first flux readout uses `J/h` because smooth P differences and the operator's live-neighbour J scale as `h` under refinement.

## Readouts

### Complementary 3+1 first-order readout

From the actual local J after one operator step, opposite channels are paired per dimension.

`S3` = mean current contribution per R3 dimension.

`T4` = fourth-direction current contribution.

`D = S3 / (S3 + T4)`

`T = T4 / (S3 + T4)`

`D + T = 1`.

The robust velocity-like candidate is the **ratio of integrated/mean components**:

`v_global = mean(S3) / mean(T4)`.

A separate diagnostic also used the pointwise ratio `D/T` before averaging. That local ratio is intentionally tested as a possible failure mode.

### Relational-order readouts

- order 1: finite first flux `q = signed(J)/h`;
- order 2 candidate: graph/continuum variation of q;
- order 3 candidate: second graph/continuum variation of q.

Both RMS derivative norms and L1/integrated variation norms were tested.

## Results

### 1. E state: exact low-order null state

Across all tested resolutions (`n = 8,10,12,14,16`), the homogeneous E state produced no active directional current and no higher-order signal.

This is exactly representation stable for the tested operator sector.

Interpretation: the numerical grid does not spontaneously create an effective direction or geometry in the homogeneous control.

### 2. M state: exceptionally tight first-order convergence

For every tested resolution from `n=8` through `n=20`:

`D = 0.5090909...`

`T = 0.4909091...`

`v_global = 1.037037...`

and the first flux magnitude was

`|q| = 0.073527...`

independent of resolution to floating-point precision.

Higher-order q variation remained at numerical roundoff.

Interpretation: the homogeneous first-order relational regime is not merely qualitative; for this controlled state its dimensionless first-order P/J -> alpha/beta -> J readout is effectively exact under grid refinement.

This is the tightest current E/M structural analogy.

### 3. G state: first-order readout remains reasonably tight if read correctly

For the continuum/emergent-matched G input over `n=12..22`:

- mean `D = 0.58310`, coefficient of variation ≈ **1.21%**;
- mean `T = 0.41690`, coefficient of variation ≈ **1.70%**;
- mean `v_global = 1.26105`, coefficient of variation ≈ **0.83%**.

Thus the integrated first-order kinematic candidate is already quite tight despite the localized object and despite the grid still being relatively coarse.

The median pointwise `D/T` had a larger ≈ **2.36%** coefficient of variation.

The raw mean of pointwise `D/T` was substantially less stable because local cells with very small `T` amplify representation errors.

**Readout conclusion:** `mean(D/T)` is a poor candidate; `mean(S3)/mean(T4)` is much more representation robust.

This is a readout problem, not evidence that the underlying first-order relation fails.

### 4. The clearest input/grid failure: fixed-cell object width

With the naive mapping, the object is always about two cells wide. Therefore its emergent/continuous width tends to zero as `h -> 0`.

This produces a misleading refinement behaviour. The mean first flux magnitude in G changed approximately

`0.0873 (n=8) -> 0.0495 (n=22)`

although no intended emergent object parameter was changed.

The representation itself was changing the object.

By contrast, with the continuum-matched fixed emergent width, the same quantity moved

`0.0461 (n=8) -> 0.0599 (n=22)`

and approached the scale of the surrounding first-order state instead of disappearing merely because the grid was refined.

This identifies a concrete input rule:

**Object width, phase structure, characteristic gradients and teacher detail must be defined in emergent/continuous ratios first and only then sampled onto the grid. Keeping them fixed in cells is not a refinement of the same model state.**

### 5. Higher relational orders expose a different grid/readout problem

For G, the RMS norms of `grad q` and `grad^2 q` increased with resolution instead of converging.

This occurs even while the first-order `q = J/h` remains finite.

The origin is structurally identifiable: the operator contains

`(P_i - P_j)_+`.

The set of live downhill directions can switch across codimension-one surfaces. Under refinement these become sharper switching surfaces. A volume RMS derivative penalizes an increasingly thin layer with increasingly large derivative, so an RMS derivative can diverge even when an integrated surface contribution has a finite continuum meaning.

This is therefore not yet evidence of a fatal model divergence.

It shows that the higher relational hierarchy cannot automatically be read with ordinary bulk RMS derivatives.

### 6. Surface/integrated variation improves the interpretation but is not yet fully converged

Replacing RMS by an L1/integrated variation measure makes the order-2 signal much more bounded.

For the continuum-matched G state, the order-2 L1 variation stayed roughly in the `0.09-0.19` range over `n=8..22` rather than showing the strong RMS blow-up.

The order-3 L1-like quantity still increased substantially (roughly `0.46 -> 1.62` over the same range).

So:

- order 1: quantitatively well controlled;
- order 2: qualitative structure robust, quantitative continuum functional not yet uniquely identified;
- order 3: robust presence of higher-order structure, but current local derivative readouts are not converged.

This matches the project's expectation that higher relational orders may require surface/integral functionals in fundamental R4 rather than a naive pointwise derivative norm.

## Where the grid/input problem appears

The series separates three distinct failure modes.

### A. Input representation error

Appears when an intended emergent quantity is specified in cells rather than in a continuum/emergent ratio.

Example: fixed 2-cell object width shrinks the represented object as resolution increases.

This is a **teacher/input-to-grid problem**.

### B. Singular local readout error

Appears when a ratio such as local `D/T` is evaluated where its denominator becomes small.

The underlying D and T fields can remain stable while the local quotient is noisy.

This is a **readout problem**.

### C. Wrong norm for higher-order switching surfaces

Appears when a codimension-one live-direction boundary is treated as a smooth bulk field and differentiated in an RMS norm.

This is a **continuum/readout-functional problem**, not necessarily an operator problem.

## How tight is the current model analogy?

### Euclidean-like / zero-order homogeneous sector

**Very tight structurally.**

Homogeneity is preserved as a no-direction/no-higher-order control; no grid direction is generated.

No claim of an actual Euclidean metric is made.

### Minkowski-like / first-order oriented sector

**Very tight at the current structural level.**

The dimensionless complementary D/T and first flux readouts are effectively resolution invariant in the homogeneous mixed 3+1 state.

This supports a robust first-order kinematic analogy, but it is not yet a derivation of Minkowski spacetime or c.

### GR-like / higher-order object-environment sector

**Moderately strong qualitatively, not quantitatively tight yet.**

A localized object-like P/J structure robustly creates nonzero local deformation and higher relational order while the same first-order readout remains well behaved.

However the numerical value of order-2/order-3 geometric deformation is not yet continuum calibrated. The current GR analogy is therefore a necessary-structure analogy only:

`localized object dynamics -> local deformation/higher relational structure`.

It is not yet a metric, curvature tensor, Einstein equation, or quantitatively converged geometry.

## Main conclusion

No fatal contradiction was found in the E -> M -> G hierarchy in this series.

The strongest result is that the lower-order relation graph is substantially more representation robust than the higher-order graph:

`order 0/1: tight`

`order 2: robust but readout-functional dependent`

`order 3+: present but not continuum-calibrated`.

The most important practical correction is on the **input side**: refinement must preserve emergent/continuous state quantities, not cell counts. The next refinement should therefore represent teacher/object features by fixed dimensionless continuum ratios and, for higher graph orders, search for convergent surface/integral functionals rather than assuming ordinary pointwise RMS derivatives.

## Falsification status

Not observed:

- spontaneous grid-induced direction in E;
- breakdown of the first-order M readout under refinement;
- disappearance of the G deformation when the object is correctly continuum-matched;
- need to modify the operator to obtain the E/M/G hierarchy.

Still open / potentially fatal if unresolved:

- failure to find any convergent order-2/order-3 R4 surface/integral functional;
- loss of the same hierarchy under directional refinement, non-Cartesian equivalent graph embeddings, or continuum teacher sampling;
- necessity of different ad hoc readout laws for each regime;
- inability to maintain an object at fixed emergent size/phase structure under true free evolution.
