# R4 characteristic stability scan

## Goal
Test which imposed R4 carrier characteristic best preserves the same full-return rotating R3 P/J orbit after release, without modifying the operator.

## Orbit definition
Two simultaneous R3 rotational components with periods 4 and 6 scanner frames. The first full return of the complete P/J pattern is therefore `LCM(4,6)=12` frames. Training length was exactly one full return period. External P and J teaching were then removed and two free operator frames were measured.

## R4 carrier families
- compact: constant sigma_w = 0.60
- linear: sigma_w = 0.60 + 0.07 frame
- sqrt: sigma_w = 0.60 + 0.18 sqrt(frame)
- pulsing: sigma_w = 0.60 [1 + A sin(2 pi frame / 12)], with A = 0.20, 0.40, 0.60

The R3 teacher orbit was identical in every case. R4 carrier law was analog input only. No stabilizer, mass, energy, metric, Compton or gravity law was added to the operator.

## Results
Ratios below are free-frame-2 / free-frame-1.

| R4 carrier | Q ratio | R3 RMS ratio | W RMS ratio | PR3 ratio | PR4 ratio | mean phase cosine |
|---|---:|---:|---:|---:|---:|---:|
| compact | 1.0285 | 1.0176 | 1.0154 | 1.1811 | 2.0030 | 0.6532 |
| linear | 0.9826 | 1.0264 | 1.0211 | 1.9815 | 2.3528 | 0.6007 |
| sqrt | 0.9494 | 1.0449 | 1.0276 | 2.5061 | 2.4835 | 0.5734 |
| pulsing A=0.20 | 1.0804 | 1.0082 | 0.9969 | 1.4032 | 2.1955 | 0.6291 |
| pulsing A=0.40 | 1.2404 | 0.9569 | 0.9425 | 1.9786 | 3.3528 | 0.6247 |
| pulsing A=0.60 | 1.1721 | 0.9906 | 0.9569 | 2.7022 | 3.3407 | 0.6264 |

## Interpretation
The low-amplitude pulsing carrier gives the smallest change in coarse R3 geometric size (`R3 RMS`) and in W RMS. However, the strictly compact R4 carrier preserves the finer projected distributional compactness (`PR3`) best and also gives the highest phase similarity to the continued teacher orbit.

Thus the current pilot does not support the claim that pulsing R4 is generally more stable. Under the stricter criterion that object stability includes preservation of the R3 distributional pattern and orbit phase, the compact R4 carrier is the strongest candidate in this scan.

The result is compatible with the older finite-thickness R3-in-R4 band picture, but does not establish it. PR4 still changes strongly in every case, so no released configuration is yet a stable particle.

## Next test
Repeat compact and low-amplitude pulsing carriers after 2, 4 and 8 full R3 return periods. The key question is whether long training makes PR3 and phase recurrence converge while R4 thickness remains bounded. If so, estimate the selected bounded W-characteristic rather than imposing it.
