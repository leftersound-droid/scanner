# Moving-object local and statistical characteristic analysis

Source data: `spacetime_inertial_r3_control` full raw journal, successful GitHub Actions run 32031281986.

No operator change was made. The existing experiment uses the same m=3 object and the same isotropic relational background while only the constant +x translation cadence changes. Cadence is a synthetic lattice-coordinate shift per frame and is not identified with physical velocity.

The additional analysis compares:

- local moments in coordinates centered on the imposed object center;
- local positive excess and negative deficit around that center;
- local anisotropy along x versus the transverse y/z/w directions;
- the fixed-laboratory-frame time-averaged positive-excess envelope.

Summary:

| cadence | local centroid x rel. | local x/trans anisotropy | local negative deficit | local negative fraction | local phi std | lab x variance | lab x/trans anisotropy |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.00314 | 1.57342 | 0.00000 | 0.00000 | 0.07867 | 3.99512 | 1.56671 |
| 0.25 | 0.14775 | 1.55793 | 2.96382 | 0.01529 | 0.09557 | 4.27227 | 1.70496 |
| 0.50 | 0.09645 | 1.63030 | 10.08356 | 0.03399 | 0.11867 | 5.21072 | 2.13339 |
| 0.75 | -0.08583 | 1.73845 | 21.43104 | 0.03871 | 0.15320 | 6.65307 | 2.81916 |
| 1.00 | -0.44674 | 1.73768 | 34.48674 | 0.03665 | 0.20132 | 7.50104 | 3.24258 |

Relative to the stationary cadence, lab-frame x variance rises by approximately 6.9%, 30.4%, 66.5% and 87.8% for cadences 0.25, 0.5, 0.75 and 1.0. Lab-frame x/transverse anisotropy rises by approximately 8.8%, 36.2%, 79.9% and 107.0%.

The local field variance also rises monotonically with cadence; at cadence 1.0 it is about 156% above the stationary case. A negative-potential deficit appears for every moving case and increases strongly in total amount with cadence.

Interpretation limit: this is a kinematic moving-object control. It shows that the unchanged local operator produces a cadence-dependent local field character and a motion-direction-elongated statistical envelope. It does not establish Lorentz contraction, relativistic kinematics, inertial mass or a physical velocity law.
