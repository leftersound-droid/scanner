# Emergent phase-orbit pilot

## Question
Can a localized P/J excitation form a dynamically stable periodic object when both training assumptions and readout are kept independent of grid position, grid radius, and iteration count?

## Setup
The production self-reflexive operator was left unchanged. Two compact initial P/J states were compared on a fully populated 13^4 box with constant P=1 background and zero boundary gradient before the disturbance reaches the edge.

- `3plus1`: compact anisotropic bump with three equal short principal scales and one longer principal scale; initial longitudinal J phase seeded in one antipodal direction pair.
- `4d`: compact isotropic four-dimensional bump with the same type of initial longitudinal J phase.

The bump itself was a compact C-infinity profile `q=exp(-1/(1-r^2))` for `r^2<1`, zero outside, added to the background. No teacher was applied after initialization.

Only the pre-birth interval was used for the phase-orbit conclusion, so boundary/domain-growth events were not interpreted as object dynamics.

## Coordinate-independent candidate readout
Each frame was reduced to a graph/state vector using only P values, local adjacency, and directional J relations:

- coefficient of variation and skewness of P,
- mean normalized edge contrast,
- `D_P`: effective directional participation of P edge gradients across the four antipodal direction pairs,
- directional-gradient anisotropy,
- local J direction entropy,
- antipodal J asymmetry,
- normalized local flow,
- `D_J`: effective directional participation of J across the four antipodal direction pairs,
- J pair anisotropy,
- active donor fraction.

`D_P=4` or `D_J=4` means equal participation of all four antipodal direction pairs; values below 4 indicate directional anisotropy. These are direction-channel invariants: they do not identify a specific x/y/z/w axis.

## Results
### 3+1 anisotropic seed
Pre-birth frames: 0..6. First birth occurred at update 7 (12 new points).

- P coefficient of variation: `0.01023 -> 0.00273`
- normalized mean edge contrast: `0.00056 -> 0.00031`
- `D_P`: `3.84855 -> 3.98520`
- P directional anisotropy CV: `0.19837 -> 0.06095`
- normalized local flow: after the first operator-created redistribution, `0.06050 -> 0.00100`
- `D_J`: after the first operator-created redistribution, `3.72236 -> 3.98282`

The initial 3+1 anisotropy therefore relaxed toward four-direction equality rather than remaining as a stable internal characteristic.

### 4D isotropic seed
Pre-birth frames: 0..9. First birth occurred at update 10 (72 new points).

- P coefficient of variation: `0.01164 -> 0.00242`
- normalized mean edge contrast: `0.00064 -> 0.00033`
- `D_P`: remained approximately `4.00000` throughout
- P directional anisotropy CV remained near zero (`0.00000` initially; `0.00258` at frame 9)
- normalized local flow: after first redistribution, `0.03925 -> 0.00040`
- `D_J`: `3.94785 -> 3.99980`

The isotropic seed stayed directionally isotropic while its contrast and flow decayed.

## Representation control
The initial state was permuted by exchanging the first and fourth computational coordinate channels, including the J direction labels, then evolved with the same operator and mapped back.

Pre-birth maximum differences:

- 3+1 seed after 6 updates: `max |Delta P| = 4.44e-16`, `max |Delta J| = 8.65e-17`
- 4D seed after 9 updates: `max |Delta P| = 2.22e-16`, `max |Delta J| = 1.44e-16`

The graph/state descriptors agreed to about `1e-15`. Thus the readout and dynamics do not depend on which computational axis carries the initial longitudinal phase.

## Interpretation
This pilot is a negative result for spontaneous periodic-object formation from these two simple localized phase-space seeds.

The trajectories did not form a closed or oscillatory orbit in the candidate emergent state coordinates. The dominant trend was monotonic loss of P contrast and local flow. The 3+1 anisotropy was erased; the 4D isotropic seed remained isotropic but also relaxed.

Therefore neither seed is a dynamically stable object of the required kind under free evolution of the current operator.

This does **not** decide whether a true stable object should be fundamentally 4D or 3+1. It only rejects these particular initial phase-space constructions as self-maintaining candidates.

The useful positive result is methodological: a grid-independent phase-space readout can distinguish anisotropic and isotropic directional structure without assigning physical meaning to a named grid coordinate, and exact coordinate permutation gives the same trajectory.

## Limitation and next step
The phase seed was supplied only as an initial previous-flow state. No closed P/J phase relation was constructed that couples P and J through an emergent phase variable. The next experiment should therefore search over families of initial **P/J phase relations**, not over static geometric shapes, while keeping the same coordinate-independent readout and permutation/refinement controls.
