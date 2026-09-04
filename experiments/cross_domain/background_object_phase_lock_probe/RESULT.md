# Background–object phase-lock probe — pilot result

## Question
Can the unchanged self-reflexive P/J operator spontaneously preserve or enforce phase synchronization between a periodically pulsing fourth-direction background and a trained rotating object after the object teacher is released?

## Methodological status
This is a **structural control**, not a physical-emergence result. The 4D periodic lattice is a boundary-free numerical representation. The imposed longitudinal background pulse is an analog/control input. The object orientation marker is a representation diagnostic, not yet an emergent physical angle.

No synchronization law, inertia law, torque, angular-momentum conservation, damping, stabilizer, or extra feedback was added.

The live-neighbour transfer algebra is unchanged:

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

with `alpha` rebuilt from current positive P differences and `beta` from normalized previous J on currently live downhill edges.

## Teacher
The object was taught for exactly **one full rotation period** using `T_obj = 48` distinct phase samples. The surrounding P/J environment was not reset between teacher frames. After the 48th teacher frame the object teacher was removed completely. The fourth-direction background pulse continued during the free interval.

Thus the test contains one full period of new object information, not repeated copies of the same cycle.

## Test 1 — period-ratio sweep
The background period `T_B` was swept across both commensurate and non-commensurate values. Representative cases:

| T_B | T_obj/T_B | free orientation progress |
|---:|---:|---:|
| 8 | 6.000 | -0.0425 cycles |
| 12 | 4.000 | -0.0386 cycles |
| 16 | 3.000 | -0.0427 cycles |
| 24 | 2.000 | -0.0447 cycles |
| 32 | 1.500 | -0.0420 cycles |
| 40 | 1.200 | -0.0442 cycles |
| 48 | 1.000 | -0.0478 cycles |
| 56 | 0.857 | -0.0501 cycles |
| 64 | 0.750 | -0.0425 cycles |
| 72 | 0.667 | -0.0422 cycles |
| 96 | 0.500 | -0.0421 cycles |

No resonance peak appears at 1:1, 2:1, 3:1, 4:1, or the other tested rational ratios. In particular, exact 1:1 synchronization (`T_B = T_obj = 48`) is not better than neighboring values.

Across the dense 1:1-neighborhood `T_B = 42..54`, including half-step detunings 47.5 and 48.5, free orientation progress stays only between approximately `-0.0393` and `-0.0478` cycles over one expected object period.

The object marker amplitude at the end of the free interval retains only about `13.8%..14.6%` of its release value in this dense sweep, indicating relaxation rather than rigid periodic motion.

## Test 2 — relative-phase sweep at exact 1:1
With `T_B = T_obj = 48`, the initial background phase was swept through eight values separated by 45 degrees.

Free orientation progress remains between approximately:

`-0.0444 .. -0.0478 cycles`

and marker retention remains between:

`0.1397 .. 0.1474`.

Therefore no privileged relative phase or narrow phase-locking window appears in the tested set.

## Test 3 — background pulse amplitude control
To check whether the failure to lock was simply due to weak coupling, the longitudinal background-flow amplitude was swept through:

`0, 0.005, 0.015, 0.05, 0.15, 0.5`

for `T_B = 46, 48, 50`.

Increasing the imposed background amplitude by two orders of magnitude does not produce sustained rotation or a special 1:1 resonance. Free orientation progress remains near a few percent of a cycle and the object marker still decays strongly.

## Relative-phase behavior
In the exact 1:1 case the observed object orientation becomes nearly stationary after release while the background phase continues to advance. Consequently the object–background relative phase drifts approximately linearly rather than approaching a constant value.

This is the opposite of phase locking:

`d/ds (Phi_obj - Phi_B) != 0`

and no spontaneous reduction toward zero drift was observed.

## Interpretation
Within **this specific representation of the background pulse and teacher**, the current operator shows neither:

1. selection of commensurate period ratios as especially stable;
2. spontaneous entrainment toward 1:1 synchronization;
3. a privileged initial relative phase;
4. stronger locking under stronger background pulse amplitude.

The simplest reading is that the present `J_prev -> beta` channel does not carry enough of the phase-history relation required for the background to pull the released object into a self-sustaining synchronized orbit.

However this does **not** falsify the broader continuous synchronization hypothesis. The current background is represented as an imposed sinusoidal previous-flow component along the fourth lattice direction, and the object teacher is still defined through a sampled rotating numerical profile. A genuinely emergent background phase and emergent object phase have not yet been reconstructed.

## Strongest justified conclusion

> Under the unchanged current operator, with one complete 48-sample object period written into a continuously evolving P/J environment, the tested fourth-direction longitudinal background pulse does not induce or preserve phase locking after release. Exact rational synchronization ratios are not preferentially stable in this pilot.

## Next discriminating test
The next useful step is not to add a synchronization rule. It is to search the raw free P/J state for a **background phase variable generated by the operator itself**, then repeat the same detuning/phase-lock analysis in those emergent coordinates. Only then can the continuous-model claim—stable object states exist only when object and background periods form a closed self-reflexive orbit—be tested without importing the clock through the numerical teacher.
