# Result — graph embedding invariance pilot

## 1. Adapter parity

On a fixed 4D L1 neighborhood, with births excluded by the test scope, the graph-form implementation of the unchanged live-transfer law was compared against the coordinate-direction implementation for 3 free operator steps.

Maximum P difference by step:

- step 1: 0.0
- step 2: 0.0
- step 3: 0.0

So the graph adapter reproduces the existing-node transfer sector exactly for this control.

## 2. Random node relabeling

The same graph and P/J state were randomly relabeled, preserving only adjacency. After 6 free steps the maximum mapped P difference was 0.0 at every step.

## 3. Closed graph-orbit training and release

A closed graph automorphism orbit was used as the teacher. The teacher is stored/transported as a graph permutation rather than recomputed from geometric coordinates. It was trained for 3 full periods and then released for 6 steps in two isomorphic representations.

Mapped differences after release:

- P max difference: 0.0 for all 6 steps
- J max difference: 0.0 for all 6 steps

Thus the tested transfer dynamics and the graph-defined training orbit are exactly invariant under node relabeling / embedding change.

## 4. Coordinate readout is representation dependent

For one identical final graph state, two arbitrary coordinate embeddings were used only for a Euclidean RMS readout:

- embedding A RMS: 2.2514084271
- distorted embedding B RMS: 4.1166448120
- ratio B/A: 1.8284753501

The underlying P/J graph state and dynamics were identical. Therefore coordinate RMS is not an invariant compactness measure.

The same final state had structural participation ratio PR = 157.7190858; this value is unchanged by node relabeling because it depends only on the state values, not their coordinate embedding.

## Main conclusion

For the existing-node transfer sector, the current alpha/beta/C/J rule is compatible with the interpretation

`lattice -> adjacency/topology`, not `lattice -> metric`.

A graph-defined teacher can also be representation-independent.

However, the current point-birth rule is not yet proven invariant under arbitrary graph representation because it explicitly uses opposite-direction pairs (`opp`). This means the complete scanner presently contains more local structure than bare adjacency: an oriented/pairing structure on incident edges. Whether that structure is intended topology or unwanted lattice geometry must be decided before claiming full representation independence.

No physical distance, time, volume, or stable-particle claim is made by this pilot.
