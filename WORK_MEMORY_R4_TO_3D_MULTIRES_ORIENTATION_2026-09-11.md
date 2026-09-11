# Work memory — R4→3D projection robustness across resolution and orientation

Date: 2026-09-11
Status: experimental partial result / working interpretation. No operator change.

## Goal

Test whether the previously observed 4D→3D microstate compression is robust across scanner resolution and object orientation/phase.

## Constraints

- Fixed self-reflexive P/J operator.
- P-only object preparation and P-only micro-perturbations.
- J always emergent.
- Scanner coordinates and update count remain numerical readouts, not assumed physical space/time.
- 3D projection is the current simple w-integration proxy, not yet identified with the physical 4D→3+1D transformation.

## Setup

Resolutions: 16^4, 20^4, 24^4.

For each resolution, three m=3 object phases were used: 0, pi/6, pi/3.

For each phase, six localized zero-sum P-only microstate variants were generated around the same prepared object macrostate.

At matched update indices n = 0, 4, 8, 12, the distance between each microstate variant and the unperturbed reference was measured in both the full 4D excess distribution and its w-integrated 3D projection using the same total-variation metric.

Compression ratio:

C_P = D_P(3D) / D_P(4D)
C_J = D_J(3D) / D_J(4D)

Values below 1 mean that the 3D projection suppresses microstate differences.

## Main results

At update 12:

| resolution | C_P | C_J |
|---|---:|---:|
| 16^4 | 0.19289 | 0.37830 |
| 20^4 | 0.13192 | 0.35241 |
| 24^4 | 0.11852 | 0.33566 |

Thus the 3D projection suppresses roughly 81–88% of P microstate variation and roughly 62–66% of J microstate variation at the final sampled state.

The effect persists at all tested resolutions and becomes stronger with increasing resolution for the later sampled states.

## Orientation/phase sensitivity

Phase dependence of the compression ratio was small at later updates.

At update 12 the across-phase coefficient of variation was:

- 16^4: P 1.66%, J 0.69%
- 20^4: P 1.49%, J 1.66%
- 24^4: P 0.56%, J 0.63%

This indicates that the observed compression is not primarily an artifact of the chosen m=3 orientation.

## Resolution trend

From 16^4 to 24^4 at update 12:

- P compression ratio changed from 0.19289 to 0.11852, about -38.6%.
- J compression ratio changed from 0.37830 to 0.33566, about -11.3%.

The P ratio has not yet clearly converged; a simple 1/N extrapolation gives an unphysical negative asymptote and therefore should not be used as a physical extrapolation.

The J ratio is much more regular under a simple 1/N diagnostic, with fitted asymptote about 0.250 and R^2 about 0.9999, but with only three resolutions this remains diagnostic rather than a validated limit.

## Interpretation

The robust finding is not a particular asymptotic number, but the existence of a resolution- and orientation-robust information reduction:

many distinct R4 P/J microstates -> substantially closer 3D projected statistical states.

This supports the working picture that the external 3+1D physical representation may be a coarse-grained statistical transformation of a much richer R4 object/environment graph rather than a one-to-one reading of raw P or J.

The stronger compression of P than J suggests that directional/flow information retains more of the underlying R4 microstate than projected potential density.

## Important limitations

- w-integration is only a scanner proxy for the unknown physical transformation T_(4D graph -> 3+1D physics).
- The prepared object is not yet an autonomous stable particle.
- Microstate perturbations were artificial P-only probes.
- No physical observable, wavefunction, charge, spin, or mass is identified here.
- No claim is made that the compression ratios are physical constants.

## Consequence

The next stage should search for a transformation family T[G] that preserves the robust cross-resolution projected characteristics while reducing microstate dependence, rather than attempting direct one-to-one mapping of raw P/J graph variables to current quantum observables.
