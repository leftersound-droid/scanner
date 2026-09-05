# R3 inertial-motion / environment coupling series — 2026-09-05

Status: **partial numerical structural result**, not a derivation of Newtonian inertia. The self-reflexive operator was not modified.

## Question
Test what environmental P/J and higher-order relational changes are produced when the same asymmetric R4 object is teacher-translated through the emergent R3 directions at approximately constant numerical velocity, then released. The aim is to distinguish static shape effects from motion-direction memory and to test whether the environment carries a delayed signature that correlates with later object motion.

## Setup
- Object: same three-lobe continuous R4 profile used in the higher-order coupling test, with fixed internal orientation.
- Teacher motion only: center translated along the numerical x direction, no internal rotation.
- Teacher velocities: `v = 0, +/-0.01, +/-0.02, +/-0.03` grid-domain units/frame.
- Resolutions: `n=12,16`.
- Continuum object normalization: `h^4 * sum(P_object) = constant`.
- Full periodic R4 numerical domain, therefore no boundary birth branch participates.
- Teacher phase followed by complete free evolution; no inertial law, force, damping, stabilizer, metric, or velocity term was inserted into the operator.

## Readouts
For the environment around the moving object, relative to the object's instantaneous center:
- front/back asymmetry of P,
- front/back asymmetry of J magnitude,
- alpha-field magnitude,
- beta-field magnitude,
- first-order graph variation `G1`,
- second-order graph variation `G2`,
- longitudinal/transverse anisotropy,
- object-center drift during the free phase,
- delayed correlation between environmental asymmetry and later object center increments.

These are readouts only and never feed back into the operator.

## Main result: motion writes an odd-symmetry environmental trace
The static control is approximately front/back symmetric. Translational teacher motion creates a persistent front/back asymmetry after release. Reversing the teacher velocity reverses the sign of the dominant odd component.

At `n=16`, the P front/back odd component, defined from the +/-v pair as half their difference, is approximately:

- `|v|=0.01`: `0.1293`
- `|v|=0.02`: `0.1280`
- `|v|=0.03`: `0.1355`

The corresponding J odd components are approximately:

- `0.1140`, `0.0497`, `0.0311`.

Alpha and beta also retain sign-sensitive relational asymmetry. The second-order graph readout G2 shows a strong sign-sensitive response but is not monotonic and is not yet continuum-calibrated.

Thus the environmental response is not merely increased deformation magnitude. It contains information about the **direction** of the imposed R3 translation.

## Free motion after teacher removal
The object does not continue with Newtonian inertia. The free center speed is only a small fraction of the imposed teacher speed.

At `n=16`:

- teacher `+0.01` -> free center speed `+0.000285` (~2.85% retention)
- teacher `-0.01` -> `-0.000195` (~1.95%)
- teacher `+0.02` -> `+0.001543` (~7.71%)
- teacher `-0.02` -> `-0.000844` (~4.22%)
- teacher `+0.03` -> `+0.002106` (~7.02%)
- teacher `-0.03` -> `-0.000999` (~3.33%).

Therefore the current teacher state does preserve a weak direction-dependent drift, but it does **not** produce an autonomous inertial object orbit.

## Environmental memory and delayed correlations
During the free phase, environmental front/back readouts show strong delayed correlation with later object center increments. Examples at `n=12` include P correlations near `0.98-0.99` with delays of roughly 1-5 frames for several velocities, while J and higher-order fields also show strong but sign-dependent delayed correlations.

These correlations are evidence of a structured common evolution, but are **not yet proof of causation**, because P, J, alpha, beta, G1 and G2 are all derived from the same coupled state and the free trajectory is short.

## Structural interpretation
The experiment supports the weak chain

`teacher R3 translation -> directional environmental P/J + relational memory -> weak direction-preserving free drift`.

This is qualitatively different from the rotational experiments:

- internal rotation mainly wrote harmonic/phase structure into the environment;
- R3 translation writes a front/back, longitudinally oriented wake-like relational structure.

The higher-order alpha/beta/G2 channels remain asymmetric after release, so the memory cannot yet be reduced to a single raw P or J scalar. However, no separate higher-order physical field is inferred; these are readouts of the same P/J relational state.

## Important negative result
There is still no emergent Newtonian inertia. The free velocity is far below the teacher velocity and the retention varies with velocity and resolution. The experiment therefore does not justify identifying teacher frame displacement with physical velocity.

## Next decisive tests
1. Repeat the motion experiment with a smooth continuum trajectory whose teacher sampling density scales with resolution.
2. Test whether a dynamically periodic hyperslab background changes the weak free-drift retention.
3. Compare pure translation, pure internal rotation, and translation+rotation using the same object family.
4. Perform a matched-state memory intervention: preserve low-order P/J statistics while destroying selected spatial correlations, then compare free center evolution.
5. Search for a P/J state orbit that regenerates its translational relation without continuous teacher motion.

Raw numerical outputs are stored outside the repository as:
- `r3_inertial_motion_environment_timeseries.csv`
- `r3_inertial_motion_environment_summary.csv`
- `r3_inertial_motion_directionality.csv`
- `r3_inertial_motion_sign_pair_summary.csv`
- `r3_inertial_motion_resolution_summary.csv`
