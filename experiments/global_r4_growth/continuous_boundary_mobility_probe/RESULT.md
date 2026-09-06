# Continuous boundary-mobility probe — preliminary result

Date: 2026-09-06
Status: working-hypothesis test; not a validated continuum result.

## Purpose
Test the new continuous interpretation of the former discrete birth mechanism without treating lattice-point creation as physical. The numerical grid is only a sampling carrier. The emergent support is the nonzero P/J state.

## Model tested
The live-neighbour operator keeps the same local alpha/beta/capacity structure. Outward channels into currently zero-P numerical samples are assigned an effective mobility

`M_vac = q(1-q)/(1+P/C)`

with

`q = J_opp / <J_other>`

for `0<q<1`; otherwise outward mobility is zero. This factor changes flux rate only; it does not remove P. Interior channels use `M=1`.

There is no physical point-birth event. P flowing into previously zero samples is interpreted only as growth of the emergent P/J support. Numerical samples already exist as representation.

## Initial condition and perturbation
One central P seed with total initial P=1. A short P-only perturbation is applied for 10 numerical frames: 0.015 P per frame distributed over four random nearby numerical samples. J is never externally modified. After frame 10 the system evolves freely.

## Emergent readouts
- `V_em = exp(-sum p_i log p_i)`
- `V_pr = (sum P)^2 / sum P_i^2`
- `d tau_em = sum J / sum P`
- support/front from nonzero P and zero-P neighbours only, not coordinate radius
- boundary P fraction
- boundary accumulation ratio = mean P on support boundary / mean P on support
- outward/vacuum flux fraction
- effective number of used R4 axes from directional-current entropy

Raw frame count and grid coordinates are not interpreted as physical time or distance.

## Numerical-integrity rule
The run is accepted only before P reaches the outer numerical box boundary. A no-barrier control reached that boundary before the perturbation ended, so it is not used as a physical comparison.

## Main result
The dynamic boundary-mobility branch remained uncontaminated by the numerical box through a useful post-perturbation free interval. After the P pump was switched off, total P remained effectively constant at about 1.15 until numerical-boundary contact.

The branch showed a strong initial boundary-congestion state that relaxed while the effective support volume continued to grow:

- at tau_em ≈ 3.16: boundary P fraction ≈ 0.737, boundary accumulation ratio ≈ 0.828, V_em ≈ 231;
- at tau_em ≈ 5.20: boundary P fraction ≈ 0.439, accumulation ≈ 0.614, V_em ≈ 1187;
- at tau_em ≈ 7.09: boundary P fraction ≈ 0.306, accumulation ≈ 0.511, V_em ≈ 3722;
- at tau_em ≈ 10.07: boundary P fraction ≈ 0.163, accumulation ≈ 0.346, V_em ≈ 15426.

The outward flux fraction stayed very small and decreased from about 0.0053 to about 0.0012 while the support volume grew. The four numerical R4 directions remained almost equally represented (`axis_eff` close to 4).

## Interpretation
This is qualitatively consistent with the first half of the working hypothesis:

`P perturbation -> internal current -> slowed outward mobility -> boundary accumulation -> redistribution / support growth`.

The result does **not** yet show a repeated congestion–release oscillation. In the available free interval it looks like one relaxation episode rather than a stable cycle. Boundary accumulation and V_em growth rate were strongly anticorrelated; accumulation decreased while volume growth accelerated. Therefore the present evidence supports a transient backlog/release interpretation, not yet a periodic self-generated front oscillator.

No R3 hyperslab claim is made from this test. The next required tests are:
1. adaptive/sparse domain so the run is not limited by a fixed numerical box;
2. longer free evolution to test whether congestion reappears periodically;
3. continuum/refinement comparison of V_em(tau_em), boundary accumulation and flux ratios;
4. perturbation-family tests using P-only inputs while leaving J fully operator-generated;
5. search for a relational front/hyperslab readout independent of coordinate radius.

## Data files generated locally
- `continuous_boundary_dynamic_clean.csv`
- `continuous_boundary_control_clean.csv`
- `continuous_boundary_common_tau_clean.csv`
- `continuous_boundary_cycle_correlations.csv`
- `continuous_boundary_cycle_lags.csv`
- `continuous_boundary_emergent_profile.csv`
