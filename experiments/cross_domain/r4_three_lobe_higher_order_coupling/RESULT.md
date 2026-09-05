# R4 three-lobe higher-order coupling test — 2026-09-05

Status: **partial numerical result / structural coupling test**, not a physical derivation. The self-reflexive operator was not modified.

## Question
Test whether a teacher-driven rotating R4 object writes its dynamical information into the environment only through raw P/J changes, or whether higher-order relational characteristics (alpha, beta, first- and second-order graph variation) carry a stronger or more persistent phase-structured memory. Also test whether delayed environment->object and object->environment correlations are both present after teacher removal.

## Setup
A continuum-defined three-lobe R4 object was rotated in the xy plane during a 32-frame teacher phase and then released for 32 free frames. The numerical domain was fully populated and periodic, so the scanner birth branch was inactive and only the exact live-neighbour operator algebra was used.

The object was continuum-normalized by keeping h^4 * sum(P_object) fixed under sampling.

The environment shell excluded the object core, so the measured m=3 harmonics were not direct object-core readouts.

Measured environmental fields/readouts:

- P: object-induced P excess,
- J: magnitude of the directional J-vector,
- A: norm of the local alpha distribution,
- B: norm of the local beta distribution,
- G1: first graph-gradient magnitude of |J|,
- G2: absolute second graph/Laplacian-like variation of |J|.

For each field X, the complex m=3 mode was measured as

`Z_3^X = A_3^X exp(i 3 phi_3^X)`.

No readout fed back into the operator.

## Teacher-phase phase locking
At n=16 the phase-lock magnitude between the rotating object and the environmental m=3 mode was:

- P: 0.9982
- J: 0.5650
- alpha characteristic A: 0.9929
- beta characteristic B: 0.8844
- G1: 0.2171
- G2: 0.9193

The strongest phase coding was therefore not confined to raw P. Alpha and the second-order G2 characteristic were also strongly phase locked to the rotating object.

Interpretation: the rotating object writes its orientation history into multiple relational layers simultaneously. The alpha/beta/G2 channels carry structured phase information beyond a simple scalar environmental amplitude change.

## Free-phase persistence
After teacher removal, none of the measured channels formed a clean autonomous m=3 orbit. Approximate free phase slopes (rad/frame, using orientation phase phi_3 rather than raw 3*phi phase) were:

- P: +0.00111
- J: -0.03159
- A: +0.03306
- B: +0.03431
- G1: +0.01572
- G2: -0.01623

Amplitude retention from the first four to last four free frames was:

- P: 4.0%
- J: 5.5%
- A: 10.8%
- B: 7.5%
- G1: 13.3%
- G2: 6.8%

Thus the raw P-mode mostly freezes/decays, whereas some relational characteristics retain a small drifting phase for longer. This is structural evidence for distributed relational memory, but not for a self-sustaining higher-order oscillator.

## Delayed bidirectional coupling check
During the free phase, phase-increment cross-correlations were measured in both directions.

Best non-negative-lag environment -> object correlations:

- P: lag 2, corr +0.712
- J: lag 2, corr -0.820
- A: lag 0, corr -0.470
- B: lag 1, corr -0.119
- G1: lag 7, corr -0.360
- G2: lag 3, corr -0.443

Best non-negative-lag object -> environment correlations:

- P: lag 3, corr -0.812
- J: lag 0, corr -0.621
- A: lag 0, corr -0.470
- B: lag 3, corr -0.313
- G1: lag 7, corr +0.163
- G2: lag 5, corr -0.603

These correlations are suggestive but **not causal proof**. The free segment is short, the fields are dynamically dependent, and several readouts are deterministic transforms of the same P/J state.

The strongest delayed two-way correlation currently appears in raw P/J. Higher-order fields, especially G2, carry strong phase structure and delayed correlation, but this experiment does not establish that they are a separate causal channel.

## Main result
The current evidence supports the weaker structural statement:

`rotating object -> phase-structured environmental state at several relational orders -> delayed coupled free evolution`

rather than the stronger statement:

`higher-order characteristic alone is the coupling carrier`.

The most important positive result is that alpha, beta and G2 retain object-specific m=3 phase information in the environment outside the object core. This supports the hypothesis that self-reflexive object/environment memory is not adequately described by raw P/J amplitudes alone.

At the same time, the strongest delayed correlation remains in raw P/J, so the data currently favor a **joint multilevel P/J relational state** rather than a clean separation into a distinct higher-order field.

## Required next falsification
A stronger test requires interventions that preserve low-order P/J statistics while selectively destroying higher-order spatial correlations, or vice versa, without changing the operator. If object free evolution changes systematically after such state-matched interventions, that would distinguish low-order from higher-order memory more causally.

Resolution refinement and longer free runs are also required before any continuum claim.

Raw result tables generated in the experiment:

- `r4_three_lobe_higher_order_phase_timeseries.csv`
- `r4_three_lobe_higher_order_phase_summary.csv`
- `r4_three_lobe_higher_order_lag_coupling.csv`
- `r4_three_lobe_directionality.csv`
