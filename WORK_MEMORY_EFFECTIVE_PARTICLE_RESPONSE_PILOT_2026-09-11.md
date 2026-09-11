# Work memory — effective particle response pilot

Date: 2026-09-11
Status: exploratory pilot / negative linear-response result. No operator change.

## Purpose

Test the next step after the v0.1 effective-particle formalization:

G_(P/J) -> Q^(0) -> response to weak P-only probes.

The goal was to identify which Q coordinates are robust and whether a differential response matrix

chi_ab = dQ_a / d epsilon_b

is presently well-defined.

## Constraints

- Fixed self-reflexive P/J operator core.
- P-only preparation and probes; J never externally forced.
- No added damping, force, clipping, stabilizer or physical law.
- 16^4 dense finite scanner used only as a pilot readout environment.
- Numerical coordinates and update index are not interpreted as physical distance/time.
- Background and object preparation remain scanner proxies, not axioms.

## Pilot preparation

Background proxy:

P_bg,initial = 0.035 + 0.045 exp[-(w/0.38)^2].

Object teacher: localized positive m=3 P-only pattern with R4 Gaussian envelope sigma=0.22 and modulation 1+0.35 cos(3 theta). The object was taught for 20 updates and the total baseline trajectory was evolved for 36 updates.

A matched background control used the same initial background and unchanged operator with no object teacher.

The object readout was not assigned a hard physical radius. Baseline joint excess E=(Delta P_+)^2+||Delta J||^2 was used only to construct scanner readout partitions. The cumulative 25% and 75% boundaries were at scanner radii approximately 0.833 and 1.229. These are not physical radii.

## Q coordinates used

Q = (C_P,C_J,T_P,T_J,H_Pq,H_Jq,H_Pf,H_Jf,Phi_Pcq,Phi_Jcq,R_34).

The first four are core/far and coupling/core P/J contrast ratios. H terms are m=3 harmonic transfer ratios. Phi terms are core-coupling relative m=3 phase readouts. R_34 is the R3/radial excess-flow ratio in this pilot readout.

Important: this pilot's R_34 definition uses absolute excess J relative to the matched background. Its baseline value (~1.375) is therefore not numerically identical to the earlier global J_R3/J_w ~3 invariant candidate. The two readouts must not be conflated.

## Probe family

Four paired +/- epsilon P-only probes were applied to the exact same baseline state, followed by 8 unchanged operator steps:

1. isotropic localized probe,
2. R3 x-gradient probe,
3. w/radial gradient probe,
4. tangential m=1 orientation probe.

The central finite-difference response was estimated at epsilon=0.0025.

## First sensitivity pattern

At epsilon=0.0025, the smallest normalized response magnitudes were observed for:

- T_P: max |eta| ~0.033,
- C_P: max |eta| ~0.045,
- pilot R_34: max |eta| ~0.321.

C_J and T_J were more responsive, with max normalized response near 1.

Harmonic and phase-transfer coordinates were much more sensitive, with |eta| from tens to hundreds depending on probe.

The four probe response directions were not identical. Example cosine similarities:

- isotropic vs tangential m1: ~-0.759,
- R3 x-gradient vs tangential m1: ~+0.886,
- R3 x-gradient vs w-gradient: ~-0.755.

SVD of the normalized response matrix gave variance fractions approximately:

- mode 1: 0.8997,
- mode 2: 0.0734,
- mode 3: 0.0258,
- mode 4: 0.0011.

This suggests a dominant response direction plus smaller independent directions, but this interpretation is provisional because the linearity test failed.

## Critical linearity control

The same central response calculation was repeated at epsilon = 0.00125, 0.0025 and 0.005.

The resulting response coefficients were not stable under probe-amplitude scaling. Median coefficient-of-variation across epsilon was approximately:

- H_Jq 0.696,
- H_Pq 0.817,
- H_Jf 0.840,
- H_Pf 0.902,
- pilot R_34 0.906,
- T_P 0.977,
- C_P 1.009,
- T_J 1.055,
- C_J 1.160,
- Phi_Pcq 1.201,
- Phi_Jcq 1.548.

Therefore the present differential susceptibility matrix chi=dQ/d epsilon is NOT established.

## Main result

The next-step experiment produced a useful negative result:

The current Q^(0) readout combined with an 8-step relaxed P-only perturbation does not exhibit a clean local linear-response regime over the tested amplitudes.

Consequently:

- large harmonic/phase response numbers must not be interpreted as charge-like, spin-like or other physical properties;
- current C_P, T_P robustness rankings are only finite-perturbation observations, not intrinsic invariance proofs;
- chi_ab should not yet be used as the effective-particle property map.

## Interpretation

This does not require any operator modification. Two possibilities remain open and should be separated experimentally:

1. the object response is genuinely nonlinear even for weak practical probes;
2. Q^(0) is a poor local coordinate system for the recurrent particle class, so small graph changes produce large coordinate changes.

The correct next step is therefore not to tune the dynamics. It is to replace the premature differential susceptibility with a finite, reparameterization-independent response geometry in Q/state space and test whether different probe amplitudes lie on common probe-specific curves/manifolds.

Candidate next analysis:

- parametric response curves Q_b(Q_a) across probe amplitude,
- state-space arc/shape comparison without physical time,
- probe-sign symmetry/asymmetry,
- recurrence-class displacement rather than dQ/d epsilon,
- resolution repetition after a stable geometric response coordinate is found.
