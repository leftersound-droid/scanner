# P/J ratio regime-map pilot

## Question
Can the unchanged self-reflexive operator exhibit qualitatively different emergent object regimes when dimensionless P/J ratio pairs are varied across many orders of magnitude?

## Scope
This is an inverse structural parameter-space probe. The operator is unchanged. No stabilizer, damping, force law, inertia law, synchronization law, threshold, or extra state variable was added. The periodic lattice is only a numerical representation used to avoid boundary/birth contamination.

A compact rotating P/J teacher orbit was sampled over one complete cycle. After release the state evolved freely.

Two main ratio axes were swept logarithmically:

- overall taught previous-flow magnitude relative to local positive P difference: `J/dP = 1e-3 ... 1e3`
- tangential-to-longitudinal taught flow ratio: `J_tan/J_long = 1e-3 ... 1e3`

A separate control swept the object P amplitude itself over `1e-3 ... 1e3`.

## Main result 1 — absolute taught J amplitude is almost invisible
Across six orders of magnitude in `J/dP`, the released qualitative behavior is nearly unchanged for fixed directional composition. The reason is structural:

`beta_ij = Jprev_ij / sum_k Jprev_ik`

so multiplying all local previous-flow components by a common factor leaves beta unchanged. The current operator therefore discards most absolute previous-J amplitude information before computing the next frame.

This was visible numerically: changing `J/dP` by factors up to one million did not generate new qualitative regimes. Free orientation progression stayed near a small backward drift and the marker/shape relaxed rather than becoming a long-lived periodic object.

## Main result 2 — directional J ratios matter more than overall J magnitude
Changing `J_tan/J_long` changes the normalized directional distribution and therefore beta. This produced modest quantitative differences, for example free phase progression varied roughly from about `-0.048` to `-0.062` cycles and localization/concentration retention changed at the ~several-to-ten-percent level depending on the directional ratio.

However no tested directional ratio produced a qualitatively distinct long-lived rotating regime. All tested cases remained in the same broad relaxing/diffusive class.

## Main result 3 — P amplitude is approximately scale-homogeneous
The object P amplitude was independently swept from `1e-3` to `1e3`. The qualitative free decay remained nearly the same:

- marker retention after the free interval: approximately `0.19 ... 0.20`
- concentration retention: approximately `0.90 ... 0.93`

The generated J scaled approximately with P amplitude, so after normalization by the imposed P scale the current behavior was similar. Thus the current periodic live-neighbour operator is close to homogeneous under overall P-amplitude rescaling in this test.

## Structural interpretation
The original inverse hypothesis was that moving P/J ratios by several orders of magnitude might cross qualitative regime boundaries and create different object classes. The present raw operator cannot fully test that hypothesis because two important amplitude degrees of freedom are largely removed by its algebra:

1. overall previous-J amplitude is normalized away in beta;
2. overall P amplitude largely rescales the live transfer capacity without changing the normalized local geometry of the state.

Therefore the effective regime space of the current operator is much smaller than the nominal `(P scale, J scale)` parameter space.

The variables that remain dynamically visible are mainly relative/local distributions, for example:

- directional P-difference ratios (`alpha` structure),
- directional previous-J ratios (`beta` structure),
- spatial/topological pattern of P,
- relative phase/topology between P and directional J.

## Strongest justified conclusion

> In the current raw operator, sweeping overall P and J amplitudes across many orders of magnitude does not produce different emergent object classes because those amplitudes are largely scale-invariant or normalized away. Directional P/J ratio structure affects the dynamics, but the tested range remains in one broad relaxing regime.

This does **not** show that a P/J-only emergent model cannot have qualitatively distinct ratio regimes. It shows that the present operator representation cannot express the specific absolute/relative amplitude mechanism proposed in the inverse hypothesis.

## Consequence for the next inverse search
The next regime map should therefore not spend computation on overall P or J amplitude unless the operator/state representation is intentionally changed. With the current operator, the meaningful parameter space is the scale-free relational one: directional alpha/beta patterns, local phase relations, topology, object/background relational ratios, and teacher-orbit structure.

Any future modification that makes absolute or cross-scale P/J ratios dynamically meaningful would be a change to the operator and must be treated explicitly as a new hypothesis rather than silently introduced as tuning.