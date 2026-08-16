from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "run-data" / "cross_domain" / "field_mass_charge_series"
OUT = OUT_DIR / "result.json"

N = 512
MEAN_BIN = 5
HF_BIN = 79


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def cosine(a, b):
    na, nb = norm(a), norm(b)
    if na == 0 or nb == 0:
        return None
    return dot(a, b) / (na * nb)


def pearson(a, b):
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    da = [x - ma for x in a]
    db = [x - mb for x in b]
    return cosine(da, db)


def basis(k, phase=0.0):
    return [math.sin(2.0 * math.pi * k * i / N + phase) for i in range(N)]


def project_amplitude(signal, k):
    s = basis(k)
    c = [math.cos(2.0 * math.pi * k * i / N) for i in range(N)]
    a = 2.0 * dot(signal, s) / N
    b = 2.0 * dot(signal, c) / N
    return math.sqrt(a * a + b * b)


def residual_rms(signal, amps):
    recon = [0.0] * N
    for k, a, phase in amps:
        wave = basis(k, phase)
        recon = [r + a * w for r, w in zip(recon, wave)]
    err = [x - y for x, y in zip(signal, recon)]
    return math.sqrt(sum(e * e for e in err) / N)


def signal(mean_amp, hf_amp, hf_sign=1.0, mean_phase=0.0, hf_phase=0.3):
    m = basis(MEAN_BIN, mean_phase)
    h = basis(HF_BIN, hf_phase)
    return [mean_amp * x + hf_sign * hf_amp * y for x, y in zip(m, h)]


def measure(sig):
    return {
        "mean_amp": project_amplitude(sig, MEAN_BIN),
        "hf_amp": project_amplitude(sig, HF_BIN),
    }


def main():
    # Synthetic controls only. Values are chosen to make the analysis path testable;
    # they are not particle physics parameters.
    symmetry_levels = [0.0, 0.02, 0.05, 0.08, 0.12]
    mean_levels = [0.60, 0.80, 1.00, 1.20, 1.40]

    # S1: persistent mean channel represented in isolation.
    s1_signal = signal(mean_amp=1.0, hf_amp=0.0)
    s1 = measure(s1_signal)
    s1["residual_rms"] = residual_rms(s1_signal, [(MEAN_BIN, 1.0, 0.0)])

    # S2: asymmetry changes only HF in the separated positive control.
    s2_rows = []
    for a in symmetry_levels:
        sig = signal(mean_amp=1.0, hf_amp=a)
        row = {"asymmetry_control": a, **measure(sig)}
        s2_rows.append(row)

    s2_mean = [r["mean_amp"] for r in s2_rows]
    s2_hf = [r["hf_amp"] for r in s2_rows]

    # S3: independent sweep: mean and HF controls intentionally decorrelated.
    hf_independent = [0.12, 0.02, 0.08, 0.00, 0.05]
    s3_rows = []
    for m, h in zip(mean_levels, hf_independent):
        sig = signal(mean_amp=m, hf_amp=h)
        s3_rows.append({"mean_control": m, "asymmetry_control": h, **measure(sig)})
    s3_mean = [r["mean_amp"] for r in s3_rows]
    s3_hf = [r["hf_amp"] for r in s3_rows]

    # Negative control: HF locked proportionally to mean.
    s3_locked_rows = []
    for m in mean_levels:
        h = 0.08 * m
        sig = signal(mean_amp=m, hf_amp=h)
        s3_locked_rows.append({"mean_control": m, "hf_control": h, **measure(sig)})
    s3_locked_mean = [r["mean_amp"] for r in s3_locked_rows]
    s3_locked_hf = [r["hf_amp"] for r in s3_locked_rows]

    # S4: two-object channels. No force law; pair responses are generic observables.
    # Pair A/B are identical in the mean channel. Complement only flips the HF sign.
    pair_cases = {
        "symmetric": {"mean_pair": 1.0, "hf_pair": 0.0},
        "asym_A": {"mean_pair": 1.0, "hf_pair": 0.08},
        "asym_B_complement": {"mean_pair": 1.0, "hf_pair": -0.08},
        "mean_changed_A": {"mean_pair": 1.25, "hf_pair": 0.08},
        "mean_changed_B_complement": {"mean_pair": 1.25, "hf_pair": -0.08},
    }

    # S5: mean invariance under complement/asymmetry at fixed mean-control.
    s5 = {
        "mean_delta_symmetric_to_asym_A": pair_cases["asym_A"]["mean_pair"] - pair_cases["symmetric"]["mean_pair"],
        "mean_delta_asym_A_to_complement": pair_cases["asym_B_complement"]["mean_pair"] - pair_cases["asym_A"]["mean_pair"],
        "mean_delta_changed_A_to_complement": pair_cases["mean_changed_B_complement"]["mean_pair"] - pair_cases["mean_changed_A"]["mean_pair"],
    }

    # S6: HF disappears for symmetry and reverses under complement in the control.
    s6 = {
        "hf_symmetric": pair_cases["symmetric"]["hf_pair"],
        "hf_asym_A": pair_cases["asym_A"]["hf_pair"],
        "hf_complement": pair_cases["asym_B_complement"]["hf_pair"],
        "hf_complement_sum": pair_cases["asym_A"]["hf_pair"] + pair_cases["asym_B_complement"]["hf_pair"],
        "hf_changed_complement_sum": pair_cases["mean_changed_A"]["hf_pair"] + pair_cases["mean_changed_B_complement"]["hf_pair"],
    }

    result = {
        "experiment": "field_mass_charge_series",
        "status": "synthetic pipeline validation; not physical emergence evidence",
        "guardrails": {
            "physical_force_law_inserted": False,
            "mass_value_inserted": False,
            "charge_value_inserted": False,
            "gravity_law_inserted": False,
            "electric_law_inserted": False,
            "potential_well_law_inserted": False,
            "particle_internal_structure_specified": False,
            "quantization_assumption_inserted": False,
            "scientific_threshold_used": False,
        },
        "representation": {
            "sample_count": N,
            "mean_frequency_bin": MEAN_BIN,
            "hf_frequency_bin": HF_BIN,
            "frequency_ratio": HF_BIN / MEAN_BIN,
            "note": "Frequency bins are synthetic analysis controls, not inferred physical frequencies.",
        },
        "S1_potential_well_mean_map": {
            "question": "Can a persistent mean channel be represented and measured separately?",
            "metrics": s1,
            "physical_claim": "none",
        },
        "S2_symmetry_map": {
            "question": "Can asymmetry change HF while leaving mean unchanged in the positive control?",
            "rows": s2_rows,
            "mean_range": max(s2_mean) - min(s2_mean),
            "hf_range": max(s2_hf) - min(s2_hf),
            "pearson_asymmetry_to_mean": pearson(symmetry_levels, s2_mean),
            "pearson_asymmetry_to_hf": pearson(symmetry_levels, s2_hf),
        },
        "S3_mean_hf_separation": {
            "independent_rows": s3_rows,
            "independent_mean_hf_pearson": pearson(s3_mean, s3_hf),
            "locked_negative_control_rows": s3_locked_rows,
            "locked_mean_hf_pearson": pearson(s3_locked_mean, s3_locked_hf),
            "note": "No threshold classifies success; raw coupling metrics are reported.",
        },
        "S4_two_object_map": {
            "pair_cases": pair_cases,
            "note": "Generic pair observables only; no interaction law is used.",
        },
        "S5_gravity_candidate_structure": {
            "metrics": s5,
            "interpretation": "Mean-channel complement invariance is only a gravity-candidate structural property.",
        },
        "S6_electric_candidate_structure": {
            "metrics": s6,
            "interpretation": "HF disappearance at symmetry and complement reversal are only electric-candidate structural properties.",
        },
        "series_conclusion": {
            "what_this_run_can_establish": "The six-stage measurement pipeline can keep mean-like and asymmetry/HF-like channels distinct and can expose deliberate coupling or complement reversal in controlled data.",
            "what_this_run_cannot_establish": "It cannot show that a primitive R4 vortex actually creates a potential well, inertia, gravity, charge or an electric field.",
            "next_required_input": "Raw finite-vortex/operator trajectories with the same observables measured under symmetry/asymmetry and two-object conditions.",
            "quantization_branch": "Deferred. Test lobe/mode/front-thickness quantization only after real operator data first reproduce a stable mean/HF split.",
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
