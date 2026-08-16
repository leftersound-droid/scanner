from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "run-data" / "cross_domain" / "spectral_mass_charge_split"
OUT = OUT_DIR / "result.json"

N = 256
MEAN_FREQ = 3.0
HF_FREQ = 41.0
MEAN_AMP = 1.0
HF_AMP = 0.08


def signal(mean_amp: float, hf_amp: float) -> list[float]:
    values = []
    for i in range(N):
        x = i / N
        mean = mean_amp * math.sin(2.0 * math.pi * MEAN_FREQ * x)
        hf = hf_amp * math.sin(2.0 * math.pi * HF_FREQ * x + 0.37)
        values.append(mean + hf)
    return values


def projection_amplitude(values: list[float], freq: float) -> float:
    c = 0.0
    s = 0.0
    for i, v in enumerate(values):
        x = i / N
        angle = 2.0 * math.pi * freq * x
        c += v * math.cos(angle)
        s += v * math.sin(angle)
    return 2.0 * math.sqrt(c * c + s * s) / N


def summarize(values: list[float]) -> dict:
    mean_amp = projection_amplitude(values, MEAN_FREQ)
    hf_amp = projection_amplitude(values, HF_FREQ)
    residual = math.sqrt(max(0.0, sum(v * v for v in values) / N - 0.5 * mean_amp**2 - 0.5 * hf_amp**2))
    return {
        "mean_component_amplitude": mean_amp,
        "hf_component_amplitude": hf_amp,
        "hf_to_mean_ratio": hf_amp / mean_amp if mean_amp else None,
        "residual_rms_after_two_component_projection": residual,
    }


def cosine(a: tuple[float, float], b: tuple[float, float]) -> float:
    na = math.sqrt(a[0] ** 2 + a[1] ** 2)
    nb = math.sqrt(b[0] ** 2 + b[1] ** 2)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return abs((a[0] * b[0] + a[1] * b[1]) / (na * nb))


def main() -> None:
    symmetric = signal(MEAN_AMP, 0.0)
    asymmetric = signal(MEAN_AMP, HF_AMP)

    # Deliberately coupled negative control: the same latent factor changes both bands.
    coupled_low = signal(0.75, 0.06)
    coupled_high = signal(1.25, 0.10)

    sym = summarize(symmetric)
    asym = summarize(asymmetric)
    cl = summarize(coupled_low)
    ch = summarize(coupled_high)

    asymmetry_delta = (
        asym["mean_component_amplitude"] - sym["mean_component_amplitude"],
        asym["hf_component_amplitude"] - sym["hf_component_amplitude"],
    )
    coupled_delta = (
        ch["mean_component_amplitude"] - cl["mean_component_amplitude"],
        ch["hf_component_amplitude"] - cl["hf_component_amplitude"],
    )

    ideal_mean_axis = (1.0, 0.0)
    ideal_hf_axis = (0.0, 1.0)

    result = {
        "experiment": "spectral_mass_charge_split_control",
        "status": "synthetic representation control; not physical emergence evidence",
        "guardrails": {
            "mass_value_inserted": False,
            "charge_value_inserted": False,
            "coulomb_lorentz_newton_inserted": False,
            "internal_particle_structure_specified": False,
            "scientific_threshold_used": False,
        },
        "control_parameters": {
            "sample_count": N,
            "mean_frequency_bin": MEAN_FREQ,
            "hf_frequency_bin": HF_FREQ,
            "hf_to_mean_frequency_ratio": HF_FREQ / MEAN_FREQ,
            "nominal_hf_to_mean_amplitude_ratio": HF_AMP / MEAN_AMP,
            "interpretive_chi": "dimensionless internal/propagation speed ratio is conceptual only in this control; no propagation model is inserted",
        },
        "cases": {
            "symmetric": sym,
            "asymmetric": asym,
            "coupled_negative_control_low": cl,
            "coupled_negative_control_high": ch,
        },
        "contrasts": {
            "asymmetry_switch_delta_mean_hf": list(asymmetry_delta),
            "asymmetry_delta_alignment_with_hf_axis": cosine(asymmetry_delta, ideal_hf_axis),
            "asymmetry_delta_alignment_with_mean_axis": cosine(asymmetry_delta, ideal_mean_axis),
            "coupled_delta_mean_hf": list(coupled_delta),
            "coupled_delta_alignment_with_mean_axis": cosine(coupled_delta, ideal_mean_axis),
            "coupled_delta_alignment_with_hf_axis": cosine(coupled_delta, ideal_hf_axis),
            "coupled_band_ratio_stability": ch["hf_to_mean_ratio"] - cl["hf_to_mean_ratio"],
        },
        "interpretation": {
            "positive_representation_result": "Turning on asymmetry should add a distinct HF component while leaving the mean component unchanged within numerical precision.",
            "negative_information_pattern": "If future operator data show mean and HF components varying in one locked direction, the mass/charge separation hypothesis or the experimental representation is undercut.",
            "physical_limit": "This control tests separability only. Existence of a real mean/inertial and HF/charge split must be tested on raw finite-vortex operator trajectories.",
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
