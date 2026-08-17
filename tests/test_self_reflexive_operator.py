from scanner.self_reflexive_operator import operator_step


def test_conservation_and_birth():
    # Center has a weak opposite flow and a stronger orthogonal flow.
    # The recovered ratio-capacity rule therefore opens a missing-neighbour birth branch.
    c = (0, 0, 0, 0)
    phi = {
        c: 10.0,
        (-1, 0, 0, 0): 9.0,   # weak +x birth reference via -x live edge
        (0, 1, 0, 0): 0.0,    # stronger orthogonal live edge
    }
    before = sum(phi.values())
    out, flow, diag = operator_step(phi, {})
    after = sum(out.values())

    assert abs(after - before) < 1e-12
    assert diag.births > 0
    assert (1, 0, 0, 0) in out
    assert out[(1, 0, 0, 0)] > 0.0
    assert flow


def test_raw_alpha_is_distribution_fraction():
    c = (0, 0, 0, 0)
    phi = {
        c: 10.0,
        (-1, 0, 0, 0): 9.0,
        (1, 0, 0, 0): 7.0,
    }
    _, _, diag = operator_step(phi, {})
    vals = sorted(diag.alpha_samples)
    assert len(vals) == 2
    assert abs(vals[0] - 0.25) < 1e-12
    assert abs(vals[1] - 0.75) < 1e-12


def test_flow_feedback_is_frame_derived_and_braking():
    c = (0, 0, 0, 0)
    phi = {
        c: 10.0,
        (-1, 0, 0, 0): 8.0,
        (1, 0, 0, 0): 8.0,
    }
    # First frame: symmetric potential distribution, no previous flow preference.
    _, flow0, _ = operator_step(phi, {})

    # Feed a deliberately concentrated previous-frame local edge distribution back in.
    prev = {(c, 0): 9.0, (c, 1): 1.0}
    _, flow1, diag = operator_step(phi, prev)

    # Same potential deltas; the edge carrying the larger previous share is more braked.
    assert flow1[(c, 0)] < flow1[(c, 1)]
    assert any(abs(b - 0.9) < 1e-12 for b in diag.beta_samples)
    assert any(abs(b - 0.1) < 1e-12 for b in diag.beta_samples)

    # No hidden alpha/beta state is required: only the supplied frame flow matters.
    _, flow2, _ = operator_step(phi, {})
    assert abs(flow2[(c, 0)] - flow0[(c, 0)]) < 1e-12
    assert abs(flow2[(c, 1)] - flow0[(c, 1)]) < 1e-12
