# Pilot result — full R3 return rotating P/J orbit

The unchanged `scanner.self_reflexive_operator.operator_step` was used. The R3 training pattern co-rotates in two planes with partial periods 4 and 6 frames, giving the first complete R3 P/J return after 12 frames. This 12-frame orbit was used as the minimum training length. Four R4 carrier families were compared.

## Release comparison

Ratios below compare release step 2 to release step 1 after teacher removal.

| R4 carrier | Q ratio | R3 RMS ratio | w RMS ratio | PR3 ratio | PR4 ratio |
|---|---:|---:|---:|---:|---:|
| compact | 0.9827 | 1.0382 | 1.0271 | 2.0654 | 3.5359 |
| linear | 0.9328 | 1.0482 | 1.0357 | 3.1277 | 3.8972 |
| pulsing | 1.0831 | 0.9976 | 1.0035 | 1.8367 | 2.7222 |
| sqrt | 0.9508 | 1.0396 | 1.0357 | 2.3599 | 2.3129 |

The pulsing R4 carrier preserved the coarse projected R3 RMS size best over the first two free steps (`R3 RMS ratio ~ 0.998`) while the other three expanded by about 3.8–4.8%. Its w extent was also nearly unchanged (`~1.0035`). This is only a short release result and does not establish a stable particle.

PR3 and PR4 still change strongly in all cases, so none of the four representations has yet passed the stronger relational/dynamical compactness condition. The result therefore distinguishes coarse projected size preservation from full recurrent compactness.

## Interpretation

This pilot supports keeping R3 compactness and R4 compactness as separate observables. A non-compact or time-dependent R4 carrier can transiently preserve a compact R3 projection at least as well as a fixed compact R4 carrier. The next test must extend training to multiple complete R3 return periods and check whether recurrence/PR stabilization improves rather than imposing any stabilizer.
