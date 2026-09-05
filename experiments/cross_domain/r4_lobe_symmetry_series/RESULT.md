# R4 2/3/4-lobe symmetry series — 2026-09-05

Status: **partial numerical structural result**, not a physical derivation. The self-reflexive operator was not modified.

## Purpose
Extend the previous R4 shape–dynamics/environment map from the two-lobe case to discrete 2-, 3-, and 4-lobe object families, and test whether the environment records only the strength of asymmetry or also the object's discrete symmetry order.

## Numerical setup
The experiment used the same live-neighbour algebra as the current scanner on a fully populated periodic R4 domain, so no birth event occurs inside this comparison:

`Delta_ij=(P_i-P_j)_+`

`alpha_ij=Delta_ij/sum_k Delta_ik`

`beta_ij=Jprev_ij/sum_k Jprev_ik`

`C_i=mean(positive Delta_ij)`

`J_ij=C_i*alpha_ij/(1+beta_ij)`

The dense array implementation is algebraically equivalent to the scanner live-neighbour step; no stabilizer, damping, force law, metric, chirality law, spin term, or extra coupling was introduced.

Object teachers were continuous R4 profiles sampled on the grid. 2, 3, and 4 identical Gaussian lobes were placed at equal angular intervals in the xy plane, with a common transverse zw profile. Object strength was continuum-normalized through `h^4 sum(P_object)=constant`.

Teacher dynamics:
- pure rotation,
- rotation + breathing/pulsation.

Both `+omega` and `-omega` were tested.

Backgrounds:
- static homogeneous,
- symmetric dynamic R4 background mode.

The teacher was added differentially frame to frame so generated environmental memory was not overwritten. After two teacher cycles the teacher was removed and the system evolved freely.

Primary resolutions used for the decisive comparison: `n=12` and `n=16`.

## Readouts
Two kinds of readout were used.

### Coarse environmental response
- late free-phase higher-order J-variation proxy `H`,
- late free-phase object/background contrast,
- oriented xy circulation proxy `c_xy`.

### Discrete symmetry harmonics
For the final free state, angular harmonics of the object-induced environment were measured in the xy plane:

`M_m(P) = |sum DeltaP * w * exp(-i m theta)| / sum |DeltaP| w`

and analogously for the object-induced J-vector magnitude. These are diagnostic readouts only and do not feed back into the evolution.

## Main result 1 — 2, 3, and 4 lobes produce distinct symmetry channels
The decisive n=16 harmonic result is that the environment retains the discrete symmetry order of the teacher object.

### Dynamic R4 background, pure rotation
Averaging the two rotation directions:

- 2 lobes: `P_m2 = 0.4543`, `Jmag_m2 = 0.1930`; the dominant P and J-magnitude harmonics are both m=2.
- 3 lobes: `P_m3 = 0.1389`, `Jmag_m3 = 0.1004`; the dominant P and J-magnitude harmonics are both m=3.
- 4 lobes: `P_m4 = 0.0131`, `Jmag_m4 = 0.0247`; the dominant P and J-magnitude harmonics are both m=4.

### Static background, pure rotation
The same ordering appears:

- 2 lobes: `P_m2 = 0.4420`, `Jmag_m2 = 0.1882`; dominant m=2.
- 3 lobes: `P_m3 = 0.1389`, `Jmag_m3 = 0.1251`; dominant m=3.
- 4 lobes: `P_m4 = 0.0142`, `Jmag_m4 = 0.0337`; dominant m=4.

Thus the weak structural statement supported by this test is:

`object discrete symmetry order k -> persistent environment harmonic m=k`

This is stronger than a simple amplitude effect. The environment does not merely show more or less deformation; it contains information distinguishing the 2-, 3-, and 4-lobe classes.

## Main result 2 — why the 3-lobe case looked weak in the earlier circulation readout
The simple xy circulation proxy is mostly an m=1-like aggregate quantity. In the 3-lobe case it is not a faithful detector of the object's natural symmetry channel.

At n=16, dynamic background, pure rotation:
- k=2 late |c_xy| average ~`5.41e-7`,
- k=3 late |c_xy| average ~`7.22e-8`,
- k=4 late |c_xy| average ~`8.15e-8`.

This initially makes the three-lobe case appear weak. However its direct m=3 harmonic is strong and dominant (`P_m3 ~ 0.139`, `Jmag_m3 ~ 0.100`). Therefore the earlier apparent weakness was substantially a **readout mismatch**, not absence of an environmental response.

This is methodologically important: different object symmetry classes may require the same general readout family evaluated in the corresponding graph/harmonic channel, rather than a single m=1 circulation number.

## Main result 3 — overall response amplitude decreases with lobe number in this teacher family
For the same continuum-normalized object family, n=16 late free-phase higher-order response under pure rotation was approximately:

### Static background
- k=2: `H_late ~ 0.00310`, contrast ~`0.00302`
- k=3: `H_late ~ 0.00171`, contrast ~`0.00229`
- k=4: `H_late ~ 0.00122`, contrast ~`0.00208`

### Dynamic R4 background
- k=2: `H_late ~ 0.00295`, contrast ~`0.00298`
- k=3: `H_late ~ 0.00176`, contrast ~`0.00227`
- k=4: `H_late ~ 0.00117`, contrast ~`0.00205`

So, with the present equal-integral / equal-radius Gaussian-lobe construction, the two-lobe class creates the strongest aggregate environmental deformation. This does **not** mean two lobes are fundamentally preferred; increasing k also makes the object more angularly balanced, so part of the decrease can be a symmetry-cancellation effect of this particular teacher family.

## Main result 4 — rotation direction and symmetry order are separate pieces of information
For k=2 and k=4, the simple xy circulation proxy reverses sign robustly under `omega -> -omega` at n=16 while the scalar higher-order response remains similar.

Example, static background, pure rotation:
- k=2: late `c_xy = +4.58e-7` vs `-5.69e-7`; late H = `0.00312` vs `0.00308`.
- k=4: late `c_xy = +1.60e-7` vs `-1.79e-7`; late H = `0.00121` vs `0.00123`.

For k=3 the m=1 circulation is not a clean chirality detector, but the m=3 amplitude remains stable. A proper phase-sensitive m=3 complex harmonic is therefore the next required chirality readout for this class.

The current evidence separates at least two environmental descriptors:

1. **discrete symmetry order** — carried by the dominant m=k harmonic;
2. **rotation orientation/chirality-like information** — carried by sign/phase-sensitive directional components.

## Rotation + breathing
The combined rotation+breathing runs retain the same k-dependent harmonic structure, but the simple circulation reversal becomes less clean because the rotation and breathing phases are coupled in the teacher.

At n=16, dynamic R4 background:
- k=2: `P_m2 ~ 0.4438`, `Jmag_m2 ~ 0.2119`;
- k=3: `P_m3 ~ 0.1407`, `Jmag_m3 ~ 0.1632`;
- k=4: `Jmag_m4 ~ 0.0550` while the scalar P harmonic is weaker after free evolution.

This indicates that P and J can retain different parts of the object's symmetry memory. In particular, the k=4 rotation+breathing case retains a clearer m=4 signature in J than in P.

## Interpretation
The experiment supports the following structural picture:

`object shape symmetry + periodic dynamics -> symmetry-selective environmental P/J memory`

and, more specifically,

`k-lobe object -> m=k environmental graph/harmonic channel`.

The result does not identify these channels with spin, charge, particle quantum numbers, or any known interaction. It only shows that the unchanged operator can preserve and regenerate distinct discrete relational classes in the object–environment state.

This strengthens the earlier hypothesis that a rotating/pulsating asymmetric object can write more than a scalar deformation into its environment: it can write **structured symmetry information**.

## Important limitations
- The current harmonic readout is defined in an xy projection; a fully R4-covariant representation of the discrete modes is still needed.
- Absolute higher-order amplitudes are not yet continuum-converged observables.
- The lobe teacher is still a constructed state family, not an autonomous object orbit found by the operator.
- The k=4 scalar P harmonic weakens strongly during the free phase while its J harmonic remains clearer, so the P/J role in symmetry memory needs separate analysis.
- A phase-sensitive complex harmonic, not only its magnitude, is needed to test chirality for k=3 and k=4 correctly.

## Next decisive tests
1. Sweep lobe asymmetry/radius continuously for k=2,3,4 to separate symmetry cancellation from lobe number.
2. Measure complex harmonic phase `arg(M_k)` through the teacher and free phases.
3. Test `xy -> xw` and general R4 plane permutations for all k to verify covariance of the k-mode.
4. Test double-plane R4 rotations and whether two independent harmonic labels coexist.
5. Perform environment-memory reset separately for k=2,3,4.
6. Search for whether any k-class becomes a self-sustaining object+environment orbit after teacher removal.

Raw local outputs were saved during the run as:
- `r4_lobe_symmetry_results_focus.csv`
- `r4_lobe_harmonics_results.csv`
