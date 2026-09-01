# Long-training R4 carrier stability test

This experiment tests the same full-return rotating R3 P/J orbit with two R4 carrier families:

- `compact`: constant finite R4 thickness,
- `pulse02`: bounded low-amplitude pulsation around the same mean thickness.

The R3 orbit contains two simultaneous rotational components with periods 4 and 6 operator frames, so the first full return of the complete R3 P/J pattern is `T_full = lcm(4,6) = 12` frames.

Requested training lengths are `1T, 2T, 4T, 8T` = 12, 24, 48, 96 operator frames.

## Guardrails

- The self-reflexive operator law is unchanged.
- No stabilizer, damping, physical force, mass, energy, metric, Compton or Lorentz law is inserted.
- The carrier family is an analog/training input only.
- Compactness is measured separately as R3 RMS size, R4-width RMS, R3 participation ratio (PR3), R4 participation ratio (PR4), and projected-orbit phase similarity.
- Long runs must not use a causally reachable finite boundary. The reference implementation therefore treats the homogeneous background implicitly and grows the computed support only where the disturbance can propagate.

## Current execution status

The boundary-free implicit implementation was run completely for `1T` for both carriers. The `2T/4T/8T` cases are computationally much larger because the causally affected R4 support grows rapidly; they are intentionally not replaced by periodic, reflecting or clipped boundaries.

See `RESULT.md` for the completed 1T measurements and the unresolved long-run requirement.
