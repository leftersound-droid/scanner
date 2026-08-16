# Probe particle m-binding map

This experiment uses two externally prescribed finite R4 probe objects with equal total excess potential and the same center-motion protocol:

- `symmetric`
- `asymmetric`

The environment evolves with `src/scanner/self_reflexive_operator.py`. The Scanner receives fixed-length framewise observables and runs its existing direct relation scan. No mass, charge, gravity, electric-field law, or exact higher-order `m` characteristic is inserted.

Neutral measurement channels:

- `substrate_response`: mean absolute environmental excess potential near the probe
- `motion_response`: signed environmental moment along the imposed center change
- `odd_response`: signed x-odd environmental moment
- `alpha_mean`, `alpha_std`
- `beta_mean`, `beta_std`
- `live_transfer`

Post-hoc candidate reading only:

- substrate response -> space/background-response candidate
- motion response -> inertia/mass-response candidate
- odd response -> symmetry/charge-response candidate

The desired output is only an `m` binding/connectivity map: which channels co-vary at this representation level. There is no edge threshold and no claim that any measured relation is a physical law.

Point birth is not used to interpret the Scanner map. Birth counts and birth transfer are logged only as diagnostics so we can see whether the finite initial substrate boundary became relevant during the run.

The GitHub Actions workflow runs the symmetric and asymmetric cases together so their binding maps are directly comparable.
