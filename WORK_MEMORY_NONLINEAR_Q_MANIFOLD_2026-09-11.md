# Work memory — nonlinear Q-state response geometry pilot

Date: 2026-09-11
Status: exploratory numerical pilot / readout geometry. No operator change.

## Goal

Continue the effective-particle mapping after the first linear response-matrix pilot showed strong amplitude dependence. The purpose here was to avoid interpreting dQ/depsilon as a physical susceptibility and instead map the finite, nonlinear response geometry in the current effective state space Q.

## Constraints

- Fixed self-reflexive P/J operator.
- P-only probes; J never externally forced.
- Numerical lattice/update index are scanner variables, not assumed physical space/time.
- No new force, damping, stabilizer, physical law, or hard particle boundary was added.
- Q is a readout coordinate system, not yet a physical observable list.

## Setup

Pilot resolution: 16^4.

Same class of localized m=3 object and broad w-localized background proxy as in the preceding response-matrix pilot.

The baseline object was prepared first, then four P-only probe families were applied to the same baseline state:

1. isotropic localized perturbation,
2. R3 x-gradient perturbation,
3. w/radial gradient perturbation,
4. tangential m=1 perturbation.

Each probe was scanned over signed amplitudes

-0.0075, -0.005, -0.00375, -0.0025, -0.00125, 0,
+0.00125, +0.0025, +0.00375, +0.005, +0.0075.

Each perturbed state was then evolved for the same fixed number of operator updates before readout. The amplitude is therefore only a controlled scanner perturbation parameter.

## Effective state coordinates

The same current Q coordinates were used:

C_P, C_J, T_P, T_J,
H_Pq, H_Jq, H_Pf, H_Jf,
Phi_Pcq, Phi_Jcq, R34_excess.

Important: R34_excess is the background-subtracted excess-J ratio and is not identical to the previously observed global J_R3/J_w ~ 3 invariant candidate.

## Main geometric result

The response sets are not well described as one-dimensional straight susceptibility axes.

Across all probe families, PCA/SVD of the baseline-relative Q displacements gave approximate global variance fractions:

PC1: 0.7980
PC2: 0.1286
PC3: 0.0626
PC4: 0.0075
PC5: 0.0030

Thus about 98.9% of the sampled finite-response geometry lies in the first three principal directions, but a single direction is insufficient.

Per probe, the affine dimension required to explain 95% of the sampled variance was:

- isotropic: 2
- tangential m1: 2
- R3 x-gradient: 3
- w-gradient: 3

This supports treating the finite response as a low-dimensional nonlinear manifold in Q-space rather than a single linear susceptibility coordinate.

## Signed-branch structure

For each probe the +epsilon and -epsilon branches were compared.

Odd-fraction measure (relative contribution of antisymmetric branch component):

- R3 x-gradient: 0.4403
- isotropic: 0.5090
- tangential m1: 0.4646
- w-gradient: 0.5658

Perfectly odd response would approach 1. The observed values near 0.44-0.57 indicate strong even/non-odd contributions.

A direct sign-antisymmetry cosine was also computed, where +1 would mean Q(-epsilon)-Q0 approximately equals -(Q(+epsilon)-Q0):

- R3 x-gradient: -0.7911
- isotropic: -0.3110
- tangential m1: -0.7262
- w-gradient: +0.4637

Therefore none of the tested probe families shows a simple universal odd response; only the w-gradient has a moderately positive antisymmetry score in this pilot.

## Curvature / path geometry

A simple path tortuosity measure in the first three PCs was:

- R3 x-gradient: 8.8252
- isotropic: 6.0352
- w-gradient: 3.6807
- tangential m1: 2.5817

All exceed 1, so the sampled finite-response paths are curved rather than straight chords in the reduced state space.

This is one reason the preceding linear-response matrix was unstable under changes of epsilon.

## Probe-family separation

Using a parameterization-independent secant direction from the most negative to most positive sampled amplitude, cosine similarities between response families were:

- R3 x-gradient vs isotropic: +0.309
- R3 x-gradient vs tangential m1: -0.485
- R3 x-gradient vs w-gradient: +0.364
- isotropic vs tangential m1: -0.099
- isotropic vs w-gradient: +0.500
- tangential m1 vs w-gradient: -0.870

The strongest separation is between tangential m1 and w-gradient. This suggests that the current Q-state already distinguishes at least some tangential versus radial environmental perturbation structure without adding a physical interaction law.

This must not yet be interpreted as spin, charge, or another named particle property.

## Hysteresis status

True hysteresis was NOT tested here. Each amplitude was launched independently from the same baseline state and relaxed for the same number of updates. Therefore path curvature and signed-branch asymmetry are established only as finite-response geometry, not memory/hysteresis.

A proper hysteresis test would require sequentially sweeping the same state through increasing and decreasing probe amplitudes and comparing Q on the return branch.

## Interpretation

The best current description is:

G_P/J -> Q-state -> low-dimensional nonlinear response manifold.

The particle candidate should not currently be represented by a fixed vector plus a linear susceptibility matrix. A more suitable next abstraction is a family of intrinsic response manifolds/orbits in Q-space.

Possible future physical properties should be identified only if a particular response geometry remains stable across:

- scanner resolution,
- preparation phase,
- weak changes of background,
- perturbation amplitude parameterization,
- repeated independent preparations.

## Next autonomous test

The next most informative step is a true sequential loop test on the two most clearly separated probe classes:

- tangential m1,
- w-gradient.

Protocol:

1. start from the same prepared object/background state;
2. ramp epsilon from 0 to +epsilon_max;
3. return to 0;
4. ramp to -epsilon_max;
5. return to 0;
6. keep the operator fixed and apply only the P-only probe at each step;
7. compare the outgoing and return paths in Q-space.

This will test whether the response manifold carries path memory/hysteresis beyond simple instantaneous nonlinear response.
