# R4 continued-periodic-background phase test — 2026-09-05

Status: **partial numerical result / structural comparison**, not a physical derivation. The self-reflexive operator was not modified.

## Question
Test the model hypothesis that, after the object-teaching phase ends, the local R4 background may remain under a quasi-stable periodic excitation representing a larger/global R4 dynamical state. The specific question is whether continued periodic background excitation changes the persistence and phase dynamics of previously trained 2-, 3-, and 4-lobe objects.

## Numerical construction
The test used the exact live-neighbour scanner algebra on a fully populated periodic R4 domain, so the birth branch is never entered:

`alpha_ij = Delta_ij / sum_k Delta_ik`

`beta_ij = Jprev_ij / sum_k Jprev_ik`

`C_i = mean(positive Delta_ij)`

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

No stabilizer, force law, damping, metric, synchronization term, or object-specific operator parameter was added.

Object teachers were continuous R4 Gaussian-envelope k-lobe profiles (`k=2,3,4`) in the xy angular sector, continuum-normalized so `h^4 * sum(P_object)` stayed fixed under refinement. They rotated with period `T_object=16` frames during a 32-frame teacher phase.

The background teacher was a 4D permutation-symmetric periodic scalar mode

`P_B = B0 + A_B sin(2 pi t/T_B) * [cos(pi x)+cos(pi y)+cos(pi z)+cos(pi w)]/4`

with `T_B=16` and no m=2,3,4 angular component. Thus it does not directly paint the lobe symmetry into the object.

## Paired post-teacher branches
Every object case was split from the **same trained state** into two branches:

A. **released background** — both object teacher and background teacher are switched off; only free P/J evolution remains.

B. **continued periodic background** — the object teacher is switched off, but the same background differential excitation continues with unchanged period and amplitude.

Each branch was compared with a matching background-only control, so the reported object/environment modes are excess signals over the corresponding background state.

Resolutions tested: `n=12` and `n=16`.

## Main result
Continued background driving does **not** preserve all lobe classes equally.

At `n=16`, comparing the late post-teacher state in the continuously driven-background branch with the fully released-background branch:

- `k=2` object-harmonic amplitude ratio: **1.48x**
- `k=3` object-harmonic amplitude ratio: **3.04x**
- `k=4` object-harmonic amplitude ratio: **0.97x**

Late core-contrast ratios (driven/released):

- `k=2`: **1.10x**
- `k=3`: **1.13x**
- `k=4`: **1.01x**

Late environmental J-harmonic ratios (driven/released):

- `k=2`: **7.01x**
- `k=3`: **2.91x**
- `k=4`: **1.18x**

Therefore the continued symmetric R4 background clearly changes the object/environment relaxation, but in a **symmetry-selective** way rather than as a uniform generic stabilization.

## Resolution behavior
The exact numerical ratios are not yet continuum-converged. At `n=12`:

- `k=2` object-harmonic late ratio: 1.17x
- `k=3`: 7.85x
- `k=4`: 0.71x

Core contrast was enhanced for all three classes at n=12, but the detailed harmonic response changed with resolution. Therefore the present result is structural, not yet a continuum quantitative law.

## Phase dynamics
The continued background does **not** make the object resume the teacher's original angular rotation speed. Post-teacher object-mode phase slopes remain small and resolution-dependent.

At `n=16`:

- k=2 object phase slope: released `+0.00349`, driven `+0.00405` rad/frame
- k=3: released `+0.00045`, driven `+0.01612` rad/frame
- k=4: released `-0.01350`, driven `-0.01494` rad/frame

Environmental J-mode phase slopes also change, but no clean 1:1 angular phase locking to the scalar background cycle is established.

This matters because the background excitation is R4-symmetric and has no angular lobe phase. It can modulate the P/J environment and sustain specific object modes, but it cannot trivially impose an xy rotational orientation.

## Interpretation
The experiment supports the following weak structural statement:

`continued periodic R4 background -> class-dependent modification of autonomous object/environment persistence`

and, more specifically in the tested state family:

`k=2 and k=3 modes are supported more strongly than k=4 by this background orbit`.

This is compatible with the hypothesis that a pre-existing global R4 background dynamics can participate in maintaining local object states after the local object teacher is removed.

It does **not** yet establish:

- that this background waveform is the correct emergent hyperband background;
- that the background is autonomous rather than externally prescribed;
- a physical time direction;
- resonance as a law;
- a stable particle state;
- or a continuum-invariant coupling strength.

## Important methodological distinction
In this experiment the background remains **externally prescribed after object release**. Therefore this is a reduced local-system test of the hypothesis

`global R4 state -> persistent local periodic background`

rather than a derivation of the global R4 background itself.

The stronger future test is to first obtain a quasi-periodic R4 background from the unchanged operator's own free evolution, then insert/train an object within a local region of that already self-generated background.

## Next decisive comparisons
1. Repeat with a purely longitudinal one-direction background pulse versus the present symmetric 4D pulse.
2. Sweep `T_object / T_background` without changing the operator to test whether particular relative periods improve persistence.
3. Increase refinement and replace local harmonic amplitudes with a continuum-stable integral/surface readout.
4. Test whether a self-generated free background orbit reproduces the same symmetry-selective support.

Raw output files generated in the experiment session:

- `r4_continued_background_compare_summary.csv`
- `r4_continued_background_compare_timeseries.csv`
- `r4_continued_background_effect.csv`

