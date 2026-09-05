# Background dimensionality / object-coupling series

Date: 2026-09-05

## Purpose
Test the GR-branch hypothesis that the background is not static and may carry a coupled P/J pulsation. Compare four background hypotheses under the same unchanged self-reflexive operator and the same dynamic object teacher:

1. static background control;
2. preselected 1D longitudinal background mode;
3. symmetric 4D background mode;
4. mixed/object-coupled 4D mode whose preferred direction is taken from the object's own 4D state/orientation rather than from a fixed grid axis.

The operator itself was not changed and no physical force, metric, damping, clock law, phase-lock law, or stabilizer was added.

## Numerical representation
Periodic 4D grids, n = 10, 12, 14, used only as numerical representations. The local live-neighbour transfer algebra was the scanner operator:

- Delta_ij = (P_i - P_j)_+
- alpha_ij = Delta_ij / sum_k Delta_ik
- beta_ij = Jprev_ij / sum_k Jprev_ik
- C_i = mean positive Delta
- J_ij = C_i alpha_ij / (1 + beta_ij)

The teacher was applied by incremental state difference rather than complete P-frame overwrite, preserving the operator-generated environmental P/J memory.

Training length: 24 frames.
Free evolution: 24 frames.
The imposed teacher-cycle angular rate was approximately 2*pi/12 = 0.524 rad/frame.

## Background families

### Static
No background oscillatory mode.

### 1D
A single selected longitudinal mode in one 4D direction. This deliberately represents the hypothesis that the 3+1 time-like direction is already selected before the background pulsation is read.

### Symmetric 4D
Equal phase-related modes over all four directions. No direction is privileged by the background teacher.

### Object-coupled mixed mode
The background mode direction follows a 4D orientation extracted from the teacher object's evolving state. This tests the hierarchy

R4 background + object state -> local preferred / longitudinal component

without assigning a permanent time axis to the operator.

## Main result 1: no autonomous background oscillator yet
After the training phase, none of the three dynamic backgrounds continued at the taught angular rate.

Representative n=12 free-phase modal phase rates:

- 1D: ~0.0087 rad/frame
- symmetric 4D: ~-0.102 rad/frame
- object-coupled mixed: ~0.098 rad/frame

versus the teacher rate ~0.524 rad/frame.

Therefore the current test does **not** demonstrate a self-sustaining background clock or autonomous P/J vacuum oscillator.

This is a negative result and was not repaired by adding any phase-lock or oscillation law.

## Main result 2: residual background state depends strongly on dimensional organization
At n=12, after 24 free frames, the retained amplitude of the trained background mode with the object present was approximately:

- 1D: 9.4%
- symmetric 4D: 10.8%
- object-coupled mixed: 21.9%

However this ordering was not monotonic across resolution. The mode-retention ratios were:

| n | 1D | symmetric 4D | object-coupled |
|---:|---:|---:|---:|
| 10 | 0.105 | 0.391 | 0.370 |
| 12 | 0.094 | 0.108 | 0.219 |
| 14 | 0.251 | 0.117 | 0.147 |

Thus modal retention itself is still grid/readout sensitive and cannot yet be interpreted as a continuum physical observable.

## Main result 3: background-only control separates memory from oscillation
Background-only runs showed that the symmetric 4D state often retained a substantial static modal deformation, but essentially no continuing phase motion. At n=12:

- 1D background-only retained ~3.1% amplitude, free phase slope ~0.00056 rad/frame;
- symmetric 4D background-only retained ~37.0% amplitude, free phase slope ~-0.00004 rad/frame;
- object-coupled teacher geometry without object retained ~11.0% amplitude, free phase slope ~0.00055 rad/frame.

Therefore large residual amplitude is **not** evidence of pulsation. In the symmetric 4D case the operator preserves a remnant deformation much better than an oscillatory phase orbit.

## Main result 4: a dynamic background changes object relaxation
A separate object-contrast readout was measured after the teacher was removed. Across n=10,12,14 the same ordering was obtained:

static < mixed/object-coupled < 1D < symmetric 4D

for retained object contrast.

Retained object contrast after 24 free frames:

| n | static | mixed | 1D | symmetric 4D |
|---:|---:|---:|---:|---:|
| 10 | 0.116 | 0.132 | 0.167 | 0.202 |
| 12 | 0.182 | 0.212 | 0.262 | 0.293 |
| 14 | 0.241 | 0.281 | 0.339 | 0.371 |

This ordering is considerably more stable than the background-mode retention itself.

Interpretation: the background dynamical organization genuinely changes how the object relaxes under the unchanged operator. The symmetric 4D dynamic background is the strongest of the tested backgrounds in preserving object contrast.

This is **not** evidence that the real background is 4D-pulsating; it is only a structural result within this teacher family.

## H1 / H2 / H3 assessment

### H1: purely emergent 1D longitudinal background
Status: weakly supported as an interaction background, not supported as an autonomous clock.

The 1D dynamic background improves object retention relative to a static background, but it requires a preselected direction and does not sustain the trained phase after teacher removal.

### H2: fundamental symmetric 4D background pulsation
Status: strongest structural support for object stabilization, but no autonomous pulsation.

The symmetric 4D background gives the most robust object-contrast retention across the tested resolutions. It also respects the ontology that no time direction must be chosen at the operator level. However its free remnant is largely phase-static rather than oscillatory.

### H3: 4D -> 3+1 mixed / object-coupled background
Status: qualitatively promising but not quantitatively robust.

The mixed mode can retain more dynamic phase character than background-only controls and at n=12 preserved more trained modal amplitude than the 1D and symmetric-4D object runs. But this advantage did not survive monotonically across n=10..14.

Thus the specific mixed construction used here is not yet a continuum-stable realization of emergent longitudinal time.

## Important interpretation
The test separates three notions that should not be conflated:

1. **background state memory**: a nonzero deformation remains;
2. **object-background dynamical coupling**: the background changes object relaxation;
3. **autonomous oscillation / clock**: a phase orbit continues with its own stable frequency.

The present operator + teacher family clearly shows (1) and (2), but not yet (3).

## Current best conclusion
The static-background assumption is disfavoured within this experiment because every dynamic background tested changes the free object decay, and the symmetric 4D background most consistently improves object retention.

However the deeper hypothesis

background P/J orbit -> emergent local time direction

is **not yet demonstrated**, because no tested background sustains its taught phase cycle after release.

The strongest next test should therefore not impose another sinusoid. It should search for a **joint autonomous (object, background) phase orbit** produced by the unchanged operator, then ask whether a 3+1 longitudinal component can be read from that orbit. Only after such an orbit exists does it make sense to distinguish whether the observed longitudinal pulsation is fundamentally 1D, fundamentally 4D, or an emergent projection of a 4D coupled cycle.
