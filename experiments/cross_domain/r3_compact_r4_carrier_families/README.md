# R3-compact / R4-carrier-family experiment

## Question

Can the same compact periodic R3 training profile coexist with materially different R4 carrier characteristics, and after training does the unchanged operator preserve a compact R3 projection even if the R4 support is compact, expanding, pulsing, or sublinearly expanding?

This explicitly separates **R3 compactness** from **R4 compactness**. A compact R3 object is not assumed to be compact in R4.

## Representation families

All cases use the same normalized compact R3 profile and the same total excess. Only the fourth-coordinate width is changed during training:

- `compact`: constant width;
- `linear`: width grows linearly with training frame;
- `pulsing`: width oscillates;
- `sqrt`: width grows sublinearly as sqrt(frame).

These are provenance `A` (analog/representation inputs). They are not new operator laws.

## Readouts

- `R3_rms`: projected three-coordinate RMS extent;
- `W_rms`: fourth-coordinate RMS extent;
- `R4_rms`: combined RMS extent;
- `PR3`: participation-number compactness after projection over w;
- `PR4`: participation-number compactness in full R4;
- `Q_plus`: positive excess above the common background.

No readout is called physical distance, time, mass, or energy.

## Guardrail

The experiment imports `scanner.self_reflexive_operator.operator_step` unchanged. No stabilizer, threshold, Compton relation, mass law, metric law, c, or energy formula is fed back into the dynamics. The finite L1 domain is chosen so the training support plus all executed nearest-neighbour frames cannot causally reach the boundary.
