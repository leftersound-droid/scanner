# Hyperslab reflection / self-excitation prerequisite test — 2026-09-05

Status: **negative prerequisite result / structural diagnostic**, not a falsification of the entire hyperslab hypothesis. The self-reflexive operator was not modified.

## Hypothesis tested
The model-level hypothesis is that a quasi-homogeneous R4 hyperslab may support a longitudinal P/J pulsation between an inner and an outer wall. An object can modulate that background; after one round trip the returning modulation may meet the object with a favorable phase relation and reduce its effective dissipation without increasing total P. In the strongest case, a joint object–background orbit could become quasi-stable.

The minimal prerequisite is therefore:

`localized P/J modulation -> longitudinal propagation -> return/reflection -> phase-carrying recurrence`

before any claim about reduced object decay can be tested.

## Representation
No new reflection law was inserted into the operator. A reflecting interval in the fourth direction was represented by the standard unfolded construction: the physical slab is mirrored into a doubled periodic numerical domain. This allows a wall return to be represented without altering the local operator.

The transverse xyz directions were periodic and quasi-homogeneous. The fourth coordinate used the doubled unfolded interval. The domain was fully populated, so the scanner birth branch was inactive and the exact live-neighbour algebra remained

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

with alpha from current positive P differences and beta from normalized previous local J distribution.

## Test A — P-only longitudinal background seed
A localized longitudinal P excess was initialized in the unfolded slab and then released with no external forcing.

Across fourth-direction resolutions nw = 24, 32, 40:
- total P was conserved to about 1e-16 relative precision;
- the longitudinal first Fourier-mode amplitude decayed monotonically;
- finer resolution slowed the numerical decay;
- the mode phase remained essentially fixed rather than advancing and returning.

At t = 40, mode-1 amplitude retention was approximately:
- nw=24: 0.597
- nw=32: 0.745
- nw=40: 0.826

At t = 79:
- nw=24: ~0.342
- nw=32: ~0.541
- nw=40: ~0.671

However the first-mode phase excursion over the useful-amplitude interval was only about 5.5e-4, 4.2e-4, and 1.2e-3 rad respectively. Therefore the apparent persistence is not a traveling/reflecting oscillation; it is a slowly smoothing stationary longitudinal deformation.

## Test B — initial directional J memory
Because the model hypothesis concerns a P/J background pair rather than P alone, the same P seed was repeated with an initial previous-flow bias in either +w or -w.

The absolute J-seed scale was swept through 0.01, 0.03, 0.10, 0.30 in the same numerical units.

Result:
- reversing the J direction produced a tiny sign-reversed initial longitudinal displacement/phase bias;
- the modulation still did not become a propagating pulse;
- no round-trip phase evolution or reflection appeared;
- changing the absolute J-seed amplitude over the 30x range produced essentially the same later evolution.

For nw=32, the first-mode phase excursion remained only about 9.25e-3 rad with directional J seeding. At t=95 the amplitude retention remained about 0.478, versus 0.473 without the J seed.

The near-independence of the result from absolute J-seed amplitude is consistent with the current operator structure: beta retains normalized previous-flow direction shares, while absolute previous-J magnitude is mostly discarded.

## Interpretation
With the current operator and this minimal hyperslab representation, the required prerequisite

`P/J modulation -> longitudinal traveling mode -> reflected return`

was **not obtained**.

The current dynamics behaves more like redistribution/smoothing of P with directional previous-J memory than like a signed longitudinal wave carrying an absolute flow amplitude. Therefore a genuine object self-excitation test based on wall-return phase cannot yet be performed without inserting an extra propagation/reflection mechanism, which would violate the fixed-operator methodology.

This result does **not** show that the conceptual hyperslab hypothesis is impossible. It shows that the present scanner operator/representation does not yet generate the specific longitudinal return channel from the tested P/J initial states.

## Methodological consequence
It would be invalid to impose an external delayed reinjection or hand-written reflection rule and then count reduced object decay as emergent evidence. Before testing self-excitation, the model must first produce a free background state with an observable phase-carrying longitudinal orbit under the unchanged operator.

A valid next search is therefore not an object-stability sweep but a **background-state orbit search** over admissible P/J initial relational states, looking for:

1. nonzero longitudinal phase velocity;
2. reversal/return in the unfolded hyperslab representation;
3. approximately recurring P/J phase after a round trip;
4. total-P conservation;
5. persistence under grid refinement.

Only after such a background orbit exists should an object-generated m=k modulation be placed on it and the open-vs-return decay rate compared.

## Data files produced in the run
- `hyperslab_reflection_background_autonomous.csv`
- `hyperslab_reflection_background_recurrence_summary.csv`
- `hyperslab_reflection_background_mode_phase.csv`
- `hyperslab_reflection_background_phase_summary.csv`
- `hyperslab_reflection_Jseed_timeseries.csv`
- `hyperslab_reflection_Jseed_summary.csv`
