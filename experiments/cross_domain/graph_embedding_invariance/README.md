# Graph embedding invariance test

Goal: falsify hidden dependence on the coordinate lattice. The same closed P/J graph orbit is trained and released under two graph-isomorphic representations. The test treats coordinates only as labels; dynamics use adjacency and P/J relations.

The unchanged live-transfer law is used in graph form:

- alpha_ij = Delta_ij / sum_k Delta_ik
- beta_ij = Jprev_ij / sum_k Jprev_ik
- C_i = mean positive Delta_ij
- J_ij = C_i * alpha_ij / (1 + beta_ij)

No metric, distance, time, Lorentz law, stabilizer, damping, or physical force is inserted.

Important scope: this experiment isolates the existing-node transfer sector. The current point-birth rule in `self_reflexive_operator.py` uses an explicit opposite-direction pairing (`opp`), so birth carries additional local oriented structure beyond bare adjacency. Therefore a full representation-invariance claim for the complete scanner, including birth, is NOT made here.

Tests:
1. Adapter parity: graph-form transfer versus coordinate implementation on the same fixed neighborhood.
2. Random relabeling invariance: same graph state under a random node relabeling.
3. Closed graph-orbit training: same graph automorphism orbit trained for 3 periods, then 6 free steps in two isomorphic representations.
4. Coordinate-readout contrast: show that Euclidean/RMS coordinate size can change under a distorted embedding while the P/J graph dynamics remain identical.
