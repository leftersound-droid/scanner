from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MEMORY_PATH = ROOT / "memory" / "graph.json"
OUT_DIR = ROOT / "run-data" / "cross_domain" / "two_identical_electron_recursive"
OUT = OUT_DIR / "result.json"


def load_relevant_memory() -> list[dict]:
    data = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    relevant = []
    for node in data.get("nodes", []):
        tags = set(node.get("tags", []))
        label = str(node.get("label", "")).lower()
        if tags & {"electron", "charge", "clock", "time", "uncertainty", "binding"} or any(
            k in label for k in ("electron", "charge", "time", "clock", "eotvos")
        ):
            relevant.append(node)
    return relevant


def add_fact(state: dict, key: str, value: str, basis: list[str], status: str = "identified") -> bool:
    if key in state["facts"]:
        return False
    state["facts"][key] = {"value": value, "basis": basis, "status": status}
    return True


def derive_until_closure(memory_nodes: list[dict]) -> dict:
    state = {
        "facts": {},
        "iterations": [],
        "assumptions": [
            "exactly two particles are identical by construction",
            "no external clock, mass standard, charge standard or external calibrated field is available",
            "no phenomenological force law is inserted",
            "current scanner resolution includes pairwise relations, memory retrieval and orientation-free common monotonic order",
        ],
    }

    memory_ids = [n.get("id") for n in memory_nodes]
    memory_text = " ".join((n.get("label", "") + " " + n.get("summary", "")) for n in memory_nodes).lower()

    add_fact(state, "particle_identity", "particle_1 and particle_2 belong to the same observed structural class", ["experiment premise"])
    add_fact(state, "common_order_capability", "an orientation-free common monotonic ordering is representable at current scanner resolution", ["current latent common-order scanner"])
    add_fact(state, "absolute_calibration", "no external absolute calibration is present", ["experiment constraints"], "boundary")

    if "simple complement is not charge complement" in memory_text:
        add_fact(state, "simple_complement_charge", "simple amplitude/orientation complement cannot currently be identified with charge-sign reversal", memory_ids, "negative")
    if "dynamic/history graph improved odd field-response closure" in memory_text:
        add_fact(state, "history_charge_channel", "history-sensitive structure carries more charge-like response information than static structure in prior scans", memory_ids, "measured_prior")
    if "curvature/inertia-like channel remained unresolved" in memory_text:
        add_fact(state, "inertia_channel", "inertia-like closure remains unresolved in prior electron scan", memory_ids, "unresolved")
    if "strong representation dependence" in memory_text:
        add_fact(state, "clock_representation_dependence", "clock reconstruction is representation-dependent in prior scans", memory_ids, "measured_prior")
    if "no heisenberg-like reciprocal law emerged" in memory_text:
        add_fact(state, "uncertainty_reciprocal_law", "no reciprocal Heisenberg-like law emerged in prior multiclock uncertainty scan", memory_ids, "negative")

    for depth in range(1, 16):
        # Strict recursion: this layer may only depend on facts that existed at
        # the start of the layer. Newly created facts become usable next layer.
        f = dict(state["facts"])
        proposals: list[tuple[str, str, list[str], str]] = []

        def propose(k: str, v: str, basis: list[str], status: str = "identified"):
            if k not in state["facts"] and not any(p[0] == k for p in proposals):
                proposals.append((k, v, basis, status))

        if "common_order_capability" in f:
            propose("emergent_time_identifiable_part", "only relational event order is identifiable at this resolution; it is not yet physical time", ["common_order_capability"])
            propose("time_orientation_gauge", "order reversal cannot be given an absolute past/future sign without an independent causal orientation", ["common_order_capability", "absolute_calibration"], "gauge_boundary")
            propose("time_parameter_gauge", "any strictly monotonic reparameterization preserves the currently reconstructed order, so zero and metric scale are not identifiable", ["common_order_capability", "absolute_calibration"], "gauge_boundary")

        if "particle_identity" in f:
            propose("mass_identifiable_part", "the two particles can be placed in the same inertia/mass class, but equality does not determine an absolute common mass value", ["particle_identity", "absolute_calibration"])
            propose("charge_identifiable_part", "the two particles can be placed in the same charge-response class if their measured response is identical, but the class cannot be named + or - absolutely", ["particle_identity", "absolute_calibration"])
            propose("particle_exchange_invariance", "swapping particle labels 1 and 2 changes no intrinsic statement available from two identical particles", ["particle_identity"], "invariant")

        if "charge_identifiable_part" in f:
            propose("charge_global_sign_gauge", "a simultaneous global sign relabeling of the two identical charge classes is observationally indistinguishable at this resolution", ["charge_identifiable_part"], "gauge_boundary")
            propose("absolute_charge_magnitude", "absolute charge magnitude is not identifiable without a calibrated coupling/field response scale", ["charge_identifiable_part", "absolute_calibration"], "unresolved")

        if "mass_identifiable_part" in f:
            propose("absolute_mass_scale", "absolute common mass scale is not identifiable from identity alone without calibrated dynamics or an external mass reference", ["mass_identifiable_part", "absolute_calibration"], "unresolved")

        if "mass_identifiable_part" in f and "charge_identifiable_part" in f:
            propose("mass_charge_coupling", "no unique mass-charge coupling law can be inferred from two identical particles without measured independent perturbation channels", ["mass_identifiable_part", "charge_identifiable_part", "absolute_calibration"], "unresolved")

        if "history_charge_channel" in f and "simple_complement_charge" in f:
            propose("charge_best_current_representation", "current evidence favors a history/response relational fingerprint over a simple static complement label for charge-like structure", ["history_charge_channel", "simple_complement_charge"], "current_best")

        if "inertia_channel" in f and "mass_identifiable_part" in f:
            propose("mass_best_current_representation", "mass can currently be constrained only as same-class/relative inertia; the dynamical inertia channel itself is not closed", ["inertia_channel", "mass_identifiable_part"], "current_best")

        if "emergent_time_identifiable_part" in f and "clock_representation_dependence" in f:
            propose("time_best_current_representation", "the strongest current time statement is a common relational ordering whose metric realization remains representation-dependent", ["emergent_time_identifiable_part", "clock_representation_dependence"], "current_best")

        if "time_best_current_representation" in f and "mass_best_current_representation" in f and "charge_best_current_representation" in f:
            propose("joint_system_current_resolution", "time, mass and charge do not yet collapse to one uniquely identifiable latent scalar: time is order-like, mass is same-class/relative inertia, charge is history-sensitive response class", ["time_best_current_representation", "mass_best_current_representation", "charge_best_current_representation"], "current_limit")

        if "joint_system_current_resolution" in f:
            propose("next_information_needed", "to go beyond the present boundary requires new independent measurements, not more recursion: raw two-particle operator trajectories with controlled independent perturbation/response channels and no added physical law", ["joint_system_current_resolution", "absolute_mass_scale", "absolute_charge_magnitude", "mass_charge_coupling"], "theoretical_boundary")

        created = []
        for k, v, basis, status in proposals:
            if add_fact(state, k, v, basis, status):
                created.append(k)
        state["iterations"].append({"depth": depth, "new_facts": created})
        if not created:
            state["closure_depth"] = depth
            state["last_productive_depth"] = depth - 1
            break

    state["memory_evidence"] = memory_nodes
    state["summary"] = {
        "time": {"identified": "orientation-free common relational order", "not_identified": "absolute zero, orientation and metric time scale; physical-time interpretation"},
        "mass": {"identified": "same mass/inertia class for the two identical particles", "not_identified": "absolute mass scale; closed inertia law"},
        "charge": {"identified": "same response class; prior evidence favors history-sensitive response fingerprint", "not_identified": "absolute +/- naming, absolute magnitude, unique topological carrier"},
        "joint": {"identified": "separate relational invariants and their gauge freedoms", "not_identified": "a unique common latent time-mass-charge generator"},
    }
    return state


def main() -> None:
    nodes = load_relevant_memory()
    result = {
        "experiment": "two_identical_particle_recursive_time_mass_charge_map",
        "status": "recursive identifiability closure at current scanner resolution",
        "guardrail": "No extra physical law or synthetic electron dynamics inserted.",
        "result": derive_until_closure(nodes),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
