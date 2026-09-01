# Current result — long-training R4 carrier stability

## Completed boundary-free 1T control

Full R3 return period: `T_full = 12` operator frames. Release readout: 3 free frames after removing the external P/J trainer.

| R4 carrier | Q ratio | R3_rms ratio | W_rms ratio | PR3 ratio | PR4 ratio | mean projected phase similarity |
|---|---:|---:|---:|---:|---:|---:|
| compact | 0.99368 | 1.04054 | 1.05104 | 1.89356 | 3.57879 | 0.75911 |
| pulse02 | 0.93697 | 1.07771 | 1.06276 | 1.56797 | 1.89684 | 0.35202 |

Interpretation guardrail: these are short-release stability readouts after exactly one complete trained R3 P/J orbit. They do **not** establish a particle, physical mass, Compton scale, or a unique R4 hyperslab law.

In this stricter boundary-free implementation the compact carrier preserved the trained projected orbit phase much better (`~0.759` vs `~0.352`), while the low-amplitude pulsing carrier had smaller PR3/PR4 growth but lost considerably more phase identity. Therefore the current 1T result does not support judging stability from geometric size alone; orbit identity and distributional compactness pull in different directions.

## 2T / 4T / 8T status

A direct boundary-free 2T run already expands the causally active four-dimensional support toward hundreds of thousands / millions of sites and exceeded the available single-session pure-Python execution budget. The 4T and 8T cases grow much further.

No periodic boundary, reflecting boundary, clipping, damping, coarse graining, or reduced-dimensional substitute was introduced, because each would change the stated experiment. Therefore no fabricated 2T/4T/8T numbers are reported.

The valid next execution target is the same unchanged operator on a larger/optimized backend, retaining the implicit homogeneous-background representation and the exact 12-frame full-return P/J trainer.
