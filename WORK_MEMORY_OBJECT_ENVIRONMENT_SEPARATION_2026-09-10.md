# Work memory — object / coupling-zone / far-field separation experiment

Date: 2026-09-10
Status: **experimental partial result / working interpretation**, not an established physical law.

## Methodological constraints

- Fixed self-reflexive operator.
- Teacher writes **P only**.
- J is never externally forced.
- Numerical lattice coordinates and iteration index are readout/sampling variables, not automatically physical space/time.
- R4 scanner radius used below is only a numerical readout coordinate.
- No stabilizing rule, threshold, external force, or physical law was added.

## Experiment

24^4 scanner.

A structured asymmetric m=3 P object was taught only until emergent time approximately

`tau_teach = 1.0`

with object period

`T_obj = 2.0`

and then released to free evolution until approximately

`tau_end = 2.73`.

The goal was to identify, without a pre-imposed P threshold, whether the object/environment state separates into:

1. a high-contrast object core,
2. a lower-amplitude but dynamically coupled local environment,
3. a far field carrying only weaker residual P/J characteristics.

The free-evolution state was sampled in concentric R4 scanner shells.

Measured shell readouts:

- P density,
- J density,
- m=3 harmonic amplitude in P and J,
- phase coherence of shell P and J relative to the core m=3 phase,
- RMS(dJ/dtau),
- RMS(d2J/dtau2).

A contiguous three-region segmentation was then applied to the combined standardized readout vector. The segmentation itself was a readout analysis only and did not feed back into the dynamics.

## Detected scanner-coordinate transitions

The data-driven three-region segmentation returned approximate boundaries:

`core -> coupling: r_scanner ~ 0.208`

`coupling -> far: r_scanner ~ 0.519`

These are **not physical radii**.

## Region averages

| readout | core | coupling | far |
|---|---:|---:|---:|
| normalized P density | 0.9156 | 0.4804 | 0.0579 |
| normalized J density | 0.9899 | 0.6570 | 0.0872 |
| A3(P) | 0.0539 | 0.0211 | 0.0177 |
| A3(J) | 0.1708 | 0.0526 | 0.0232 |
| P/core phase coherence | 0.2300 | 0.4734 | 0.2512 |
| J/core phase coherence | 0.3359 | 0.3810 | 0.2484 |
| normalized RMS(dJ/dtau) | 0.1335 | 0.7772 | 0.3062 |
| normalized RMS(d2J/dtau2) | 0.2821 | 0.8001 | 0.4436 |

## Main partial result

The observed structure is consistent with a three-scale interpretation:

`high-contrast periodic core -> dynamically coupled local environment -> weak far-field characteristic`

The core contains the strongest object-specific m=3 pattern.

The coupling zone is not simply a lower-amplitude continuation of the core. Its strongest distinguishing feature is the enhanced dynamic J response:

`RMS(dJ/dtau)` and `RMS(d2J/dtau2)` both peak in the intermediate region.

The coupling zone also shows stronger average phase coherence to the core than the core-region shell average itself, especially in P.

The far field retains much smaller P/J amplitudes and weaker object-specific harmonic structure, while nonzero J dynamics and residual phase information remain measurable.

## Interpretation

The current working interpretation is:

- **core**: high-contrast, object-specific P/J dynamic pattern;
- **coupling zone**: lower-amplitude environment that dynamically tracks and responds to the object;
- **far field**: weak distributed P/J characteristic that may carry interaction-relevant information without reproducing the full object pattern.

This supports defining the object boundary using the **joint P/J relational characteristic**, not a simple P threshold.

P and J must not be interpreted as independent absolute fields. They are complementary components of the self-reflexive state:

`Gamma^(n) = (P^(n), J^(n))`

and the operator maps this to the next joint state. Therefore P inhomogeneity and J inhomogeneity are mutually coupled aspects of the same evolving state.

## Consequence for inverse stabilization

The stabilization target should not be “hold core P fixed.”

The more appropriate target is persistence of the dynamical relational class:

`G_core <-> G_coupling <-> G_far`

A future inverse-background search should therefore identify which P-only background perturbations reduce drift out of this joint P/J orbit/class, particularly by controlling the coupling-zone phase relations and higher-order J response.

Any successful artificial stabilizing background remains an experimental proxy only. It must later be inverted to ask what autonomous global R4 evolution under the unchanged operator could generate the same local background trajectory.

## Files generated in the experiment

- `object_environment24_raw_shells.csv`
- `object_environment24_radial_profile.csv`
- `object_environment24_detected_boundaries.csv`
- `object_environment24_regime_summary.csv`
