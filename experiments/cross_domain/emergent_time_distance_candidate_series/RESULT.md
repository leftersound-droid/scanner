# Emergent time–distance candidate series — structural result

## Goal
Search, without modifying the raw self-reflexive operator, for dimensionless emergent time and distance readout candidates built only from P, J, alpha and beta that satisfy the previously defined relational hierarchy:

1. first-order R4 relation -> low-complexity projected 3+1 kinematic readout;
2. second-order relation -> projected velocity/acceleration-like inhomogeneity;
3. higher-order relation -> object-dependent local deformation capable in principle of becoming GR-like when the relational graph is sufficiently resolved.

This is a **candidate/falsification series**, not a derivation of Euclidean, Minkowski or GR metrics. Grid coordinates and iteration count are numerical ordering only.

The live-neighbour operator is unchanged:

`J_ij = C_i * alpha_ij / (1 + beta_ij)`

with alpha rebuilt from current positive P differences and beta from normalized previous J on currently live downhill edges.

## Candidate family A — directional 3+1 complement

At each active state point normalize the actual local outgoing flow:

`gamma_a = J_a / sum_b J_b`.

The raw six spatial channels and two fourth-direction channels cannot be compared directly because there are three spatial dimensions but only one fourth dimension. Therefore use **per-dimension shares**:

`S3 = (gamma_x+ + gamma_x- + gamma_y+ + gamma_y- + gamma_z+ + gamma_z-) / 3`

`T4 = gamma_w+ + gamma_w-`

and renormalize only between these two projected sectors:

`D = S3 / (S3 + T4)`

`T = T4 / (S3 + T4)`.

Thus, whenever both sectors are active,

`D + T = 1`.

The corresponding odds are exact reciprocals:

`V1 = D/T`, `R1 = T/D`, `V1*R1 = 1`.

This reciprocal relation is a property of the readout construction, not yet a discovered physical law. Its usefulness must therefore be judged by whether the same readout distinguishes the E/M/G relational hierarchy and responds correctly to object-generated inhomogeneity.

## Test A1 — homogeneous and axis controls

A homogeneous P state produces no active J and therefore no artificial time or distance direction.

A pure affine gradient along one of the first three projected spatial axes gives `D=1, T=0` on active interior points.

The same affine gradient moved to the fourth numerical direction gives `D=0, T=1`.

The underlying raw operator remains axis-permutation equivariant; the 3+1 distinction enters only at the **projected readout stage**. Therefore the numerical fourth coordinate is not fundamental time. This candidate is meaningful only after selecting the R3-linked subspace being measured.

## Test A2 — isotropic 4D localized state

For a smooth isotropic 4D localized P bump, the raw directional flow has approximately 3/4 of its total activity in the six spatial channels and 1/4 in the two fourth-direction channels, simply because of dimension count.

After per-dimension correction, the projected complement becomes near-balanced. In the four-step run the mean values stayed close to the same order, with the exact complement condition holding to machine precision.

This is the first useful result: an isotropic R4 state is not artificially interpreted as 75% distance and 25% time merely because R3 has three axes. Per-dimension normalization removes that representation multiplicity.

## Test A3 — anisotropic fourth-direction width sweep

A localized state was given the same spatial width `sigma_3 = 1.5` while the fourth-direction width was swept:

| sigma_4 | mean D | mean T |
|---:|---:|---:|
| 0.6 | 0.46998 | 0.53002 |
| 0.9 | 0.49880 | 0.50120 |
| 1.2 | 0.52457 | 0.47543 |
| 1.5 | 0.54550 | 0.45450 |
| 2.0 | 0.60134 | 0.39866 |
| 3.0 | 0.71630 | 0.28370 |
| 4.0 | 0.77886 | 0.22114 |

The two readouts move monotonically in opposite directions across the sweep. This satisfies the **weak complementarity requirement**:

`D up <=> T down`.

It does not establish that physical distance and time are exact reciprocals.

## Candidate family B — first-order projected velocity

For states with both projected sectors active, define the dimensionless first-order kinematic candidate

`v_em^(1) = D/T`.

This uses no grid distance and no iteration-as-time. It is simply the odds between the current R3-directed and fourth-directed local flow shares.

### Test B1 — mixed affine first-order states

A first-order P state was constructed with a spatial affine component and a fourth-direction affine component. Let `r` be the fourth-gradient / spatial-gradient ratio. On interior points after one operator step:

| r | D | T | D/T |
|---:|---:|---:|---:|
| 0.125 | 0.72727 | 0.27273 | 2.66667 |
| 0.25 | 0.57143 | 0.42857 | 1.33333 |
| 0.5 | 0.40000 | 0.60000 | 0.66667 |
| 1 | 0.25000 | 0.75000 | 0.33333 |
| 2 | 0.14286 | 0.85714 | 0.16667 |
| 4 | 0.07692 | 0.92308 | 0.08333 |
| 8 | 0.04000 | 0.96000 | 0.04167 |

The candidate is smooth, monotonic and reciprocal under exchange of the projected spatial/fourth dominance. This is structurally compatible with a Minkowski-like **first-order kinematic** role, but no Lorentz metric, c, or physical velocity law has been inserted or derived.

## Candidate family C — relational derivative hierarchy

From normalized local flow gamma define a local four-component orientation vector. Then use graph-local finite-difference proxies only as numerical representations of the continuum relational derivatives:

- order 1: local orientation magnitude;
- order 2: neighbour-to-neighbour variation of the orientation field;
- order 3: neighbour variation of the order-2 field.

These are not final formulas. They test whether increasing relational order detects increasingly local structure.

Representative four-step values:

### Homogeneous E state

All orders are zero.

### First-order directed M state

A spatial affine state gives approximately:

- order 1: `0.987 -> 0.798`
- order 2: `0.0577 -> 0.0739`
- order 3: `0.0118 -> 0.0112`

The higher-order signals here are dominated by the finite periodic numerical boundary / relaxation of the affine control and remain small compared with the localized G state.

### Localized G state

A smooth localized 4D bump gives approximately:

- order 1: `0.556 -> 0.553`
- order 2: `0.1225 -> 0.1413`
- order 3: `0.0238 -> 0.0351`.

Thus the same readout hierarchy distinguishes a localized inhomogeneous state by stronger second- and third-order relational structure.

This supports, but does not prove, the intended hierarchy:

`first relational order -> velocity-like projected quantity`

`second relational order -> acceleration/curvature-like projected variation`

`third/higher order -> object/environment feedback structure`.

## Test C2 — object-induced deformation of the first-order candidate

To test the GR-like requirement qualitatively, a mixed first-order background state was used as a uniform projected kinematic reference. A localized smooth object-like P bump was then added without changing the operator.

With no bump, `v_em^(1)=D/T` is uniform over the interior:

- mean = `0.333333`
- standard deviation ~ `9e-16`
- neighbour roughness ~ `1.6e-16`.

Increasing the localized bump amplitude produces a local deformation of the **same** velocity candidate:

| bump amp | mean v | std(v) | neighbour roughness | core mean | outer mean |
|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.3333 | ~0 | ~0 | 0.3333 | 0.3333 |
| 0.05 | 0.4274 | 0.5605 | 0.0813 | 1.0524 | 0.3759 |
| 0.10 | 0.5264 | 0.5922 | 0.1390 | 1.1678 | 0.4492 |
| 0.20 | 0.6559 | 0.7843 | 0.2220 | 1.1333 | 0.5482 |
| 0.35 | 0.8670 | 1.2321 | 0.4451 | 1.0494 | 0.8195 |
| 0.50 | 0.9321 | 1.2039 | 0.4037 | 1.0309 | 0.9046 |
| 0.80 | 1.1499 | 1.6151 | 0.5153 | 1.0207 | 1.1640 |
| 1.20 | 1.0752 | 1.2236 | 0.4251 | 1.0171 | 1.0795 |

The dependence is not globally monotonic at large amplitude, so no simple GR-like source law is claimed. The important structural result is that the low-order uniform candidate becomes locally nonuniform **because of the object-like P/J structure itself**, with no geometry deformation law inserted.

This satisfies a necessary qualitative condition for a later GR-like readout: object dynamics can distort a kinematic background variable generated by the same P/J algebra.

## Distance and time interpretation status

The strongest currently surviving interpretation is therefore:

1. `D` is a **local distance-direction share candidate**, not distance itself.
2. `T` is a **local fourth-direction / time-share candidate**, not time itself.
3. `D/T` is a **first-order projected velocity candidate**.
4. Integrating a local spatial increment derived from D together with an independently validated emergent clock increment derived from T / global measure growth may produce a distance candidate.
5. The graph-local derivatives of `D/T`, alpha, beta and J provide natural second- and higher-order candidates for acceleration/curvature-like relations.

A final physical distance still requires a path integral over emergent local increments and a continuum/state-dependent measure. A final physical time still requires consistency with the global monotonic 4D-measure growth and local distribution/entropy modulation. Neither grid edge count nor iteration number is accepted as physical distance/time.

## Falsification findings

### Not falsified

- a common P/J readout family can separate low-order homogeneous, first-order directed and higher-order localized states;
- a projected R3/fourth-direction complement can be defined without grid length or iteration time;
- the complementary shares show opposite monotonic character under controlled fourth-direction anisotropy;
- the same first-order candidate is locally distorted by an object-like inhomogeneity, satisfying a necessary GR-like qualitative condition;
- higher graph-derivative order responds more strongly to localized structure.

### Rejected / still invalid

- fourth grid coordinate = physical time;
- iteration count = physical time;
- grid edge count = physical distance;
- Shannon entropy alone = universal global time;
- D/T = physical velocity as an established law;
- exact reciprocal distance-time law as a derived result;
- any claim that Euclidean, Minkowski or GR metrics have already been recovered.

## Main conclusion

The most promising candidate architecture found in this series is not a direct formula for distance or time, but a hierarchy:

`P,J -> alpha,beta -> normalized directional flow gamma`

`gamma -> projected complementary shares (D,T)`

`D/T -> first-order velocity-like readout`

`local derivatives of D/T, alpha, beta, J -> second/higher-order acceleration/curvature-like readouts`

`path/measure integration -> future distance and time candidates`.

The decisive next test is continuum/refinement convergence of this same hierarchy and construction of a monotonic clock increment compatible simultaneously with (a) the local T share and (b) global 4D active-measure growth. If that cannot be done with one common readout family, the candidate architecture fails.