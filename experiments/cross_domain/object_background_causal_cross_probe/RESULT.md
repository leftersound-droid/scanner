# Object-background causal cross probe — result

## Question
Does one complete taught object cycle write a persistent/periodic trace into an otherwise unexcited P/J background, and conversely can the currently used fourth-direction background pulse write a state that later affects an object? Does simultaneous/continued background driving improve the released object orbit?

## Methodological status
Structural control only. The periodic 4D lattice is a boundary-free numerical representation. No inertia, synchronization, torque, damping, stabilizer, angular-momentum law, or physical metric was added. The operator is the unchanged live-neighbour algebra:

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

with `alpha` from current positive P differences and `beta` from normalized previous J on currently live downhill edges.

The object teacher is one complete 48-state rotation cycle of the same compact marked ring-like P/J object used in the preceding synchronization probes. The background pulse is the same analog/control representation used previously: a sinusoidal previous-flow contribution along the +/- fourth-direction channel.

## Protocols
1. `O_only_release`: one full object cycle on an initially homogeneous/unexcited background, then 96 free frames. Tests O -> B.
2. `B_only_release`: one full background-pulse cycle on homogeneous P with no object, then release. Tests whether the current B representation can store itself.
3. `B_then_O`: one full B-only cycle, then one full O teacher cycle, then release. Tests whether prior B training changes later O dynamics.
4. `O_release_B_on`: one full O cycle with no B pulse, then O teacher off while the B pulse is switched on. Tests B -> O on an already existing object state.
5. `OB_train_release`: O and B taught together for one cycle, then both off.
6. `OB_train_B_continues`: O and B taught together for one cycle, then O off while B continues.

The environment is never reset between stages within a protocol.

## Key results

### O -> B is nonzero
After one full object cycle, the far-field background contains a persistent P disturbance:

- far-field `P_rms` at release start: `0.0424375632`
- far-field `P_rms` after 96 free frames: `0.0422692522`

Thus the object writes a long-lived state trace into the background.

However the far-field J activity relaxes strongly:

- far-field J activity at release start: `0.00327901165`
- after 96 free frames: `4.03341113e-05`

No autonomous periodic background clock was detected. The surviving trace is predominantly a slowly relaxing/static P redistribution, not a self-sustaining P/J cycle.

### B-only write is exactly zero in the present representation
On perfectly homogeneous P, one full imposed longitudinal previous-flow background cycle leaves:

- `max |P-BACKGROUND| = 0`
- `max |J| = 0`

at the end of the cycle.

Reason: previous J enters only through beta on currently live downhill P edges. Homogeneous P has no positive Delta P, so the imposed previous-flow signal cannot generate a new J or alter P.

Therefore this current background representation cannot serve as an autonomous memory oscillator by itself.

### B pretraining therefore has exactly zero later effect
`B_then_O` is numerically identical to `O_only_release` after the object cycle:

- object free phase progress: `-0.1077960319` cycles in both cases
- object marker retention: `0.0002425125` in both cases
- far-field P/J diagnostics: identical to numerical precision

This is a structural consequence of the B-only null state, not evidence that a genuinely emergent background oscillator could not affect an object.

### A continuing B pulse can modify an existing released object, but does not stabilize it
For `O_only_release`:

- free object phase progress: `-0.1077960319` cycles
- marker retention after 96 frames: `0.0002425125`

For `O_release_B_on`:

- free object phase progress: `-0.0633940307` cycles
- marker retention: `8.14583278e-05`

Thus the continued background pulse changes the release trajectory, proving a nonzero B -> O coupling when the object supplies P gradients. But the object decays even more strongly; no stable orbit is created.

### Simultaneous O+B training also does not create a closed orbit
`OB_train_release`:

- free phase progress: `-0.1063414663` cycles
- marker retention: `0.0002465960`

`OB_train_B_continues`:

- free phase progress: `-0.0660339528` cycles
- marker retention: `6.82817977e-05`

These are small perturbations of the same relaxing family, not phase-locked rigid rotation.

## Causal interpretation
The present numerical representation is strongly asymmetric:

`O -> B` : yes, because the object creates P gradients and therefore writes a persistent environmental P state.

`B -> O` : yes only when an object/nonuniform P already exists, because the imposed B signal modifies beta on live edges.

`B -> B` : no on homogeneous P in the current representation.

So the existing fourth-direction previous-flow pulse is not a genuine autonomous background oscillator. It is better interpreted as a modulation channel acting on already active P/J structure.

## Strongest justified conclusion
> The current raw operator demonstrably lets a taught object write a long-lived environmental P trace, and a continuing fourth-direction background-flow signal can modify an existing object. But the currently used background-pulse representation cannot write or preserve itself on homogeneous P, and the object-written trace does not become a periodic background oscillator. Therefore the present simulation is not yet a symmetric O <-> B memory test.

## Consequence for the synchronization hypothesis
The previous absence of phase locking is now easier to interpret: one of the supposed oscillators (the background pulse) was not an autonomous dynamical oscillator at all. It existed only as externally supplied previous-flow modulation. Therefore testing spontaneous synchronization between two emergent periods requires first finding or constructing, using only the raw operator and admissible initial state, a background P/J orbit that persists after its teacher is removed.

The next discriminating experiment is therefore to search for a free background P/J periodic orbit first, measure its emergent phase, and only then couple a local object orbit to it without externally continuing either clock.