# R4 lobe harmonic phase check — 2026-09-05

Status: **partial numerical result / phase-structure test**, not a physical derivation. The self-reflexive operator was not modified.

## Question
Test whether the discrete lobe-symmetry modes found for rotating 2-, 3-, and 4-lobe R4 objects are only amplitude patterns or whether their **complex harmonic phase** follows the object orientation during teaching and retains any autonomous phase motion after the teacher is removed.

## Numerical setup
The experiment reused the same fully populated periodic R4 representation and the same live-neighbour P/J operator algebra as the previous lobe-symmetry series. No birth occurs on the periodic full domain.

Objects were continuous R4 multi-lobe profiles with k = 2, 3, 4, continuum-normalized before grid sampling. The tested dynamics were:
- pure xy-plane rotation;
- xy rotation + breathing;
- both rotation signs;
- static and symmetric dynamic R4 backgrounds;
- n = 12 and 16.

Teacher updates were differential frame-to-frame updates, preserving generated environmental memory. After two teacher cycles the teacher was removed and the system evolved freely.

## Phase readout
To avoid trivially re-reading the object core, the complex harmonic was measured on a smooth **outer environmental shell** with the trained core suppressed.

For each lobe number k:

`Z_k = sum(environment_field * weight * exp(-i k theta))`

The measured quantities were:
- amplitude `|Z_k|` normalized by the weighted absolute field;
- harmonic phase `arg(Z_k)`;
- teacher-lock coherence after removing the expected `-k theta_object` phase trend;
- relative phase lag;
- free phase drift converted to an orientation-like angular velocity `omega_free = -(1/k) d arg(Z_k)/d frame`.

The same construction was applied separately to the environmental P difference and the magnitude of the environmental J-vector difference.

These are readouts only and do not feed back into the operator.

## Main result: strong phase locking during teaching
For pure rotation on the dynamic R4 background at n = 16, the environmental P harmonic is almost perfectly phase-locked to the teacher object for all tested symmetry classes:

- k=2: lock(P) = 0.99963
- k=3: lock(P) = 0.99993
- k=4: lock(P) = 0.99739

The environmental J harmonic is also strongly locked, though less perfectly:

- k=2: lock(J) = 0.97682
- k=3: lock(J) = 0.92341
- k=4: lock(J) = 0.93889

The sign of the measured phase lag reverses when the rotation direction is reversed, as expected for an oriented phase relation.

Thus the previously observed k-specific environmental memory is not merely a static amplitude asymmetry: during the teacher interval its **complex phase co-rotates with the object**.

## Free phase: no full autonomous continuation
After the teacher is removed, none of the tested objects continues at the teacher angular velocity.

For n=16, dynamic R4 background, pure rotation, the mean absolute free/teacher angular-velocity ratios were approximately:

### P harmonic
- k=2: ~0.003
- k=3: ~0.001
- k=4: ~0.138

### J harmonic
- k=2: ~0.062
- k=3: ~0.063
- k=4: ~0.171

Therefore the k=2 and k=3 environmental P phases essentially freeze after teaching. Their J phases retain only a slow oriented drift, about 6% of the teacher rate.

The k=4 case is different: both P and J retain a substantially larger phase drift, roughly 14–17% of the teacher rate at n=16. Reversing the teacher rotation reverses the sign of the free drift.

This is the strongest current phase-memory candidate, but it is **not an autonomous rotating object/background orbit** because the free rate is much smaller than the teacher rate and the mode amplitude decays substantially.

## Resolution caution
At n=12 the free-phase ratios differ significantly from n=16, especially for k=4. Therefore the absolute free angular velocities are not yet continuum-converged. The qualitative observations that remain robust are:

1. strong teacher-phase locking of the k-specific environmental mode;
2. rotation-sign reversal of the phase relation;
3. teacher removal causes a large loss of phase speed;
4. J tends to retain more oriented phase motion than P;
5. k=4 is the strongest free-phase-drift candidate at n=16.

## Rotation + breathing
Adding breathing preserves the strong P phase lock but weakens the J phase-lock coherence, especially for k=3 and k=4, because radial breathing and angular rotation jointly modulate the same environmental state.

At n=16 on the dynamic R4 background:
- k=2: lock(P) ~0.998, lock(J) ~0.948; free J rate ~5–6% of teacher rate;
- k=3: lock(P) ~0.999, lock(J) ~0.805; free J rate ~4%;
- k=4: lock(P) ~0.996, lock(J) ~0.777; free J rate ~16%.

Thus the combined mode remains phase-structured, but it should not yet be interpreted as a cleaner autonomous orbit than pure rotation.

## Interpretation
The experiment supports the structural chain:

`object discrete symmetry + rotation -> phase-locked environmental k-mode -> slow oriented free J-memory`

The important new result is that the environment stores not only the lobe number and response amplitude but also a **phase relation** to the object's orientation.

However, the model has not yet produced a self-sustaining phase oscillator. The present teacher appears to write an oriented phase memory into P/J state, but the free operator dynamics mostly relaxes that memory rather than regenerating the original angular velocity.

This strengthens the hypothesis that the current multi-lobe teachers are still mock-up approximations to an allowed autonomous object/background orbit rather than the orbit itself.

## Next falsification
The next useful test should search the period/asymmetry/background parameter space around the k=4 branch and ask whether there is a state family for which:

- the free `|Z_k|` remains finite;
- `omega_free / omega_teacher -> 1` or approaches a resolution-stable nonzero value;
- the object and environmental J harmonic maintain a bounded relative phase;
- the result survives grid refinement and R4 axis permutation.

Failure to find such a regime would indicate that the current operator/teacher family stores oriented phase memory but does not support an autonomous rotating state of this class.

Local result files from this run:
- `r4_lobe_phase_summary.csv`
- `r4_lobe_phase_timeseries_focus.csv`

No physical spin, charge, angular momentum law, torque, damping, synchronizer, or other property-specific term was added.