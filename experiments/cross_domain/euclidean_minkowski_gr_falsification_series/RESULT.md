# Euclidean -> Minkowski -> GR structural falsification series

## Goal
Test whether the unchanged self-reflexive P/J operator can support a sequence of increasingly structured geometry-like regimes using one common family of graph/PJ-native diagnostics, without inserting Euclidean, Minkowski, GR, c, metric tensors, forces, curvature laws, or any other physical equations.

This is NOT a derivation of real physics. Real physics is used only as an external analog/falsification target. The question is whether one P/J system remains structurally capable of a refinable possible physics and whether any fatal contradiction appears.

## Operator
Unchanged current scanner operator from `src/scanner/self_reflexive_operator.py`:

- alpha_ij = Delta_ij / sum_k Delta_ik
- beta_ij = Jprev_ij / sum_k Jprev_ik
- C_i = mean positive Delta_ij
- J_ij = C_i * alpha_ij / (1 + beta_ij)

No extra stabilization, threshold, damping, metric, time law, force law, synchronization law, or physical parameter was added.

## Common graph/PJ-native descriptors
The same diagnostics were used across E, M and G regimes:

1. normalized first-order P edge variation `P_grad1`
2. normalized antipodal second P difference `P_second`
3. normalized outgoing-J orientation magnitude `J_orient_mag`
4. global orientation coherence `J_global_coherence`
5. neighbor-to-neighbor orientation roughness `J_orient_rough`
6. local J-activity roughness `J_activity_rough`
7. mean J activity

These are structural readouts only. They are not yet emergent physical distance, time, curvature, energy, or mass.

---

# Test E — homogeneous / Euclidean-like baseline

A constant 4D P state with J=0 was evolved for 4 operator steps on a fully populated 9^4 lattice. Interior points only were read out to avoid boundary contamination.

Result for every step:

- P_grad1 = 0
- P_second = 0
- J_orient_mag = 0
- J_global_coherence = 0
- J_orient_rough = 0
- J_activity_rough = 0
- mean_activity = 0

Interpretation: the homogeneous state stays exactly featureless. The operator does not create a preferred direction or spontaneous geometry-like anisotropy from a homogeneous state.

This is structurally compatible with an Euclidean-like homogeneous baseline, but does not derive Euclidean metric distance.

---

# Test M — homogeneous directed / Minkowski-like structural regime

An affine P field was used with a small constant gradient. No physical time axis was assumed.

Representative fourth-channel affine case, step 1:

- P_grad1 = 0.00250225395356
- P_second = 1.45e-18 (numerically zero)
- J_orient_mag = 1.0
- J_global_coherence = 1.0
- J_orient_rough = 0
- J_activity_rough = 0
- mean_activity = 0.0200

By step 4:

- P_grad1 = 0.00200071141735
- P_second = 0.000127693269166
- J_orient_mag = 1.0
- J_global_coherence = 1.0
- J_orient_rough = 0
- J_activity_rough = 0.0178571
- mean_activity = 0.00850

The system therefore supports a regime with globally coherent directed flow and essentially no initial second-order spatial inhomogeneity.

## Coordinate-permutation control
The same affine state was placed first along coordinate 1 and then along coordinate 4. After swapping the corresponding coordinate and direction labels back, the two runs were exactly identical for all 4 tested steps:

- max |Delta P| = 0
- max |Delta J| = 0

Interpretation: the raw operator does NOT contain a built-in physical time direction. A 3+1 split, if it exists, must emerge from state structure/readout rather than from the coordinate label itself.

This is important and not a failure: it prevents us from falsely interpreting the fourth grid axis as physical time.

---

# Test G — localized inhomogeneity / GR-like structural regime

A smooth localized 4D P bump was evolved with the same operator and same diagnostics.

For amplitude 0.35, step 1:

- P_grad1 = 0.0118740151278
- P_second = 0.00326272006160
- J_orient_mag = 0.473289572817
- J_global_coherence ~ 0
- J_orient_rough = 0.151526493414
- J_activity_rough = 0.147918423797
- mean_activity = 0.0313585743115

At step 4:

- P_grad1 = 0.00691841582474
- P_second = 0.00168752441642
- J_orient_mag = 0.456480038231
- J_global_coherence ~ 0
- J_orient_rough = 0.146572226954
- J_activity_rough = 0.0985149221998
- mean_activity = 0.0141742446977

Thus the localized state is structurally distinct from both E and M:

- nonzero second-order P structure appears;
- global directional coherence disappears;
- local orientation and activity roughness become nonzero.

This is only a curvature/backreaction ANALOG candidate, not GR curvature.

## Localized-amplitude sweep
The bump amplitude was swept through:

0.05, 0.10, 0.20, 0.35, 0.50, 0.80, 1.20

Step-1 `P_second` increased monotonically:

- 0.05 -> 0.000503842
- 0.10 -> 0.000994050
- 0.20 -> 0.001936236
- 0.35 -> 0.003262720
- 0.50 -> 0.004496982
- 0.80 -> 0.006731397
- 1.20 -> 0.009317935

At the same time normalized J-orientation roughness remained approximately invariant at ~0.151526 on step 1.

Interpretation: localized P-state strength changes the magnitude of the second-order inhomogeneity readout while the normalized orientation topology remains similar. This is exactly the kind of separation one would want from an amplitude-like source characteristic versus a normalized geometric/directional characteristic, although no physical mass or curvature relation has been derived.

---

# Time-candidate falsification test

To test the idea that global emergent time may be related to 4D active-volume growth / dilution, sparse 3^4 active P seeds were evolved with point birth enabled. No external expansion rule was added.

For an asymmetric seed over 20 steps:

- active points: 97 -> 4358
- Shannon distribution entropy: 4.39311 -> 8.00193
- total P: 89.4380662751 at every step within floating-point precision

For random and affine seeds, active-point count and entropy were also monotone over the 20 tested steps.

However, a symmetric seed produced a decisive counterexample to the strongest simple entropy-clock hypothesis:

- step 4: active points = 225, entropy = 4.94401795354
- step 5: active points = 233, entropy = 4.81258451577

So active measure increased while Shannon entropy decreased.

## Consequence
The hypothesis

`tau_global = monotone function of Shannon entropy alone`

is falsified by this pilot.

The weaker structure remains viable:

- growth of active 4D measure is a stronger monotone global-time candidate;
- distribution dilution/entropy may contribute to local time or local clock-rate modulation;
- the exact state-dependent continuum measure dmu(P,J) is still missing, so active grid-point count is only a representation diagnostic, not emergent physical 4-volume.

This is a useful falsification, not a model failure.

---

# Combined E -> M -> G result

Using one common readout family, the unchanged operator separates three structural regimes:

E: homogeneous static
- zero first and second order structure
- zero J activity

M: homogeneous directed
- first-order P variation
- unit global J orientation coherence
- approximately zero initial second-order P structure
- zero initial orientation roughness

G: localized inhomogeneous
- stronger first-order variation
- nonzero second-order P structure
- near-zero global orientation coherence
- nonzero local orientation/activity roughness

Therefore the structural hierarchy

C0 -> C1 -> C2

is supported again by an independent falsification-oriented series.

It is reasonable to use the analog labels

Euclidean-like -> Minkowski-like -> GR-like

ONLY as external comparison classes. No Euclidean, Minkowski, or GR metric has been derived.

---

# Fatal-contradiction checks

## Not observed
1. No spontaneous preferred coordinate in the homogeneous state.
2. No coordinate-label dependence in the affine permutation control.
3. Localized structure DOES modify the common geometry-like descriptors.
4. Stronger localized P structure produces a stronger second-order P signal monotonically in the tested range.
5. Total P is conserved in the sparse growth tests.
6. The E/M/G regimes remain qualitatively distinguishable under the same operator/readout family.

## One simple hypothesis rejected
Shannon entropy by itself is not a universally monotone emergent time.

## Still unresolved / potentially fatal later
1. No validated emergent distance d_em(P,J) exists yet.
2. No validated emergent time tau_em(P,J,dmu) exists yet.
3. No proof of refinement convergence for an eventual E/M/G metric readout.
4. No demonstrated reciprocal/anti-characteristic relation between emergent R3 distance and fourth-characteristic-dominated time.
5. No autonomous stable matter-like periodic object yet exists in the physically relevant emergent-coordinate sense.
6. No evidence yet that an object modifies an actual emergent metric rather than only P/J structural descriptors.

---

# Strongest justified conclusion

The present operator is NOT falsified by the minimal requirement that one P/J dynamics should admit qualitatively distinct homogeneous-static, homogeneous-directed, and localized-inhomogeneous structural regimes analogous to Euclidean, Minkowski, and GR levels of description.

The same tests also show that the fourth numerical axis cannot simply be declared time, and that Shannon entropy cannot simply be declared emergent time.

The next high-value task is therefore not to fit known metric equations. It is to construct candidate distance/time readouts from the already separated P/J regimes and require them simultaneously to satisfy:

- coordinate/representation invariance;
- continuum refinement convergence;
- monotone global-time behavior;
- E-like isotropy/homogeneity;
- M-like stable distance-time complementarity in directed homogeneous states;
- G-like local deformation in the presence of localized P/J structures;
- no extra physical law or per-regime fitting parameter.

That is the next discriminating stage between a merely descriptive P/J system and a refinable possible-physics generator.
