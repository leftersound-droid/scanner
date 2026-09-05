# R4 shape–dynamics / environment mapping — 2026-09-05

Status: **partial numerical result / structural map**, not a physical derivation. The self-reflexive operator was not modified. The experiment used the same local live-neighbour P/J algebra as the scanner on a fully populated periodic R4 numerical domain so that boundary birth did not contaminate the shape/dynamics comparison.

## Question
Map how R4 object shape and internal periodic dynamics change the object–environment relation. The specific hypothesis was that a periodically moving asymmetry (for example a rotating anisotropic object) can write an oriented P/J memory into the environment, which subsequently feeds back into the object.

## Teacher families
Shapes, all defined as continuous R4 profiles before sampling:
- isotropic sphere (symmetry control),
- ellipsoid,
- two-lobe object,
- asymmetric sphere with a localized bump.

Dynamics:
- static,
- breathing/pulsation,
- rotation in the xy plane,
- rotation in the xw plane,
- xy rotation + breathing,
- double R4-plane rotation.

Two backgrounds were compared:
- static homogeneous background,
- symmetric dynamic R4 background mode.

The teacher was applied as frame-to-frame state difference, rather than overwriting the full P field, so previously generated environmental P/J memory was retained.

## Readouts
The object case was compared with a background-only control. Measured quantities included:
- environmental P RMS difference,
- environmental directional J-vector difference,
- higher-order local variation of the environmental J-vector magnitude,
- oriented circulation proxies in xy and xw,
- object/background contrast during the free phase.

These are readouts only; none feeds back into the operator.

## Main coarse-map result
The symmetry control is decisive: rotating the isotropic R4 sphere produces essentially the same state as the static sphere. Its circulation proxies remain at numerical zero. Therefore rotation by itself is not enough; a shape degree of freedom must actually change under the rotation.

Asymmetric objects behave differently. Ellipsoids and two-lobe objects generate plane-specific environmental circulation when rotated. A two-lobe xy rotation produces an xy circulation component; rotating the same object in xw transfers the response to the xw component.

At n=16 with continuum-corrected object strength, static background:
- two-lobe + xy rotation: c_xy/h = 1.9587e-5, c_xw/h = -1.1642e-6;
- the same two-lobe + xw rotation: c_xy/h = -1.1642e-6, c_xw/h = 1.9587e-5.

With the dynamic symmetric R4 background the same plane swap occurs:
- xy rotation: c_xy/h = 1.3183e-5, c_xw/h = -9.228e-7;
- xw rotation: c_xy/h = -9.228e-7, c_xw/h = 1.3183e-5.

This strongly supports an R4-orientation-covariant environmental response rather than a preferred lattice plane artifact.

## Rotation-direction reversal
For simple asymmetric rotating objects, omega -> -omega reverses the sign of the corresponding circulation while leaving the higher-order response magnitude approximately similar.

Examples after continuum-corrected sampling:

n=16, static background:
- two-lobe xy rotation: c_xy/h = +1.96e-5 vs -2.1e-5 for reversed rotation; H/h = 0.01347 vs 0.01367.
- ellipsoid xy rotation: c_xy/h = +4.46e-5 vs -4.8e-5; H/h = 0.01283 vs 0.01298.

n=12, static background:
- ellipsoid xy rotation: c_xy/h = +3.51e-5 vs -5.2e-5; H/h = 0.01181 vs 0.01180.

Interpretation: the sign-sensitive part is genuinely orientation/chirality-like, while the scalar magnitude of the environmental deformation is largely even under reversal. This is stronger than a simple amplitude effect.

The combined rotation+breathing cases are less perfectly antisymmetric under reversal because the two teacher phases are coupled; they should not yet be interpreted as a clean chirality invariant.

## Shape + dynamics interaction
The strongest higher-order environmental response in the coarse map appeared repeatedly for the two-lobe object with rotation + breathing. This is not reproduced by rotating a sphere, and simple breathing alone does not generally give the same oriented response.

After correcting the continuum input normalization, selected n=16 values were:

Static background:
- sphere static: H/h = 0.01457, object contrast = 0.2873;
- ellipsoid xy rotation: H/h = 0.01283, contrast = 0.3417;
- two-lobe xy rotation: H/h = 0.01347, contrast = 0.3491;
- two-lobe xy rotation + breathing: H/h = 0.01595, contrast = 0.4402.

Dynamic symmetric R4 background:
- sphere static: H/h = 0.01737, contrast = 0.3333;
- ellipsoid xy rotation: H/h = 0.01597, contrast = 0.3924;
- two-lobe xy rotation: H/h = 0.01644, contrast = 0.4004;
- two-lobe xy rotation + breathing: H/h = 0.01956, contrast = 0.4922.

Thus the dynamic R4 background increases retention/environmental response, and the combined asymmetric periodic object gives the largest response among the selected controls.

This supports the weak structural hypothesis:

`shape asymmetry + periodic internal motion -> richer oriented environmental P/J memory`

but does not establish a particle, spin, charge, gravity, or any known physical interaction.

## Important grid/input correction
A serious teacher-to-grid error was identified during refinement. Keeping raw sum(P_object) fixed while refining the R4 grid makes the continuum object strength shrink because the correct quadrature control is

`h^4 * sum(P_object) = constant`.

The initial resolution runs therefore artificially weakened the object at finer n. The decisive refinement was rerun with object amplitude scaled as 1/h^4 and with the teacher-cycle sampling density increased with resolution.

After this correction the qualitative hierarchy survives across n=10,12,14,16:
- rotating sphere remains a symmetry-null control;
- asymmetric rotation creates plane-specific response;
- rotation+breathing two-lobe remains among the strongest responses;
- dynamic R4 background enhances object retention compared with the static background.

The absolute higher-order readout is still not fully converged, so the precise continuum functional remains open.

## Environmental-memory reset control
For the dynamic R4 background, resetting the environment to its background-only state while preserving the trained object core strongly reduces the later higher-order response and object contrast.

Examples for two-lobe rotation+breathing:

n=12:
- full trained environment: H/h = 0.02018, contrast = 0.4175;
- environment reset: H/h = 0.00627, contrast = 0.3021.

n=16:
- full trained environment: H/h = 0.01956, contrast = 0.4922;
- environment reset: H/h = 0.00658, contrast = 0.3597.

This is direct evidence, within this numerical representation, that the state written into the environment affects the object's later free evolution.

The same reset on a perfectly static background creates a sharp artificial object/background interface and therefore inflates local derivative readouts; that branch is not a valid quantitative memory measure and should not be used as evidence.

## Current interpretation
The experiment separates three effects:

1. **Symmetry:** an R4-symmetric object does not acquire a new oriented environmental mode merely by being numerically 'rotated'.
2. **Asymmetry:** a shape with a real orientational degree of freedom writes a direction-dependent environmental response.
3. **Periodic dynamics:** coupling asymmetry to periodic rotation/pulsation can substantially increase the persistent higher-order object–environment relation.

The most interesting current candidate is therefore not a static particle shape but a joint state orbit

`(object asymmetry, periodic internal motion, environmental P/J memory)`.

The data are consistent with, but do not yet prove, a self-reproducing loop of the form

`O_n -> B_(n+1) -> O_(n+2)`.

## Remaining open questions / next tests
- Find whether a self-sustaining object+environment orbit exists after the teacher is fully removed.
- Replace the current local derivative-like higher-order readout with a continuum-stable surface/integral functional.
- Sweep asymmetry continuously to determine whether the transition is smooth or has a regime boundary.
- Sweep teacher period after continuum time-sampling correction and test for preferred relative object/background periods.
- Test more general R4 double rotations and whether distinct rotation classes remain distinguishable after axis permutation.
- Repeat memory-reset controls without creating an artificial sharp interface, using a smooth state-matched environmental replacement.

No operator modification, force law, damping, stabilizer, metric, spin law, charge law, or physical interaction term was added.