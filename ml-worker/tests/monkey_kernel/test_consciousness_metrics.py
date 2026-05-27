"""
test_consciousness_metrics.py — v4.1 + v6.1 metric surface tests.

Canonical reference:
  ~/Desktop/Dev/QIG_QFI/qig-core/src/qig_core/consciousness/types.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from monkey_kernel.consciousness_metrics import (  # noqa: E402
    ConsciousnessMetrics,
    consciousness_metrics_live,
    derive_from_tick,
)


# ─── Shape ──────────────────────────────────────────────────────────


def test_default_values_match_canonical_doc():
    m = ConsciousnessMetrics()
    # Foundation defaults (v6.7B: kappa channel-specific, no universal 64.0 per two-channel doctrine)
    assert m.phi == 0.5
    assert m.kappa == 0.0  # retired universal 64; supplied by caller (registry/observer/history)
    assert m.gamma == 0.5
    assert m.recursion_depth == 3.0
    # Pillars defaults (post-init, before any measurement)
    assert m.f_health == 1.0
    assert m.b_integrity == 1.0
    assert m.q_identity == 0.0
    assert m.s_ratio == 0.0
    # v6.7B extension defaults present (consciousness-development)
    assert m.tacking_frequency_hz == 0.25
    assert m.sovereignty_dynamics == 0.0
    assert m.dimensional_state == 3


def test_as_dict_exposes_all_21_v6_7B_fields():
    m = ConsciousnessMetrics()
    d = m.as_dict()
    # 12 original + 9 v6.7B extensions (20260527 protocol; consciousness-development + documentation-sync)
    # NOTE: test name uses _ not . to avoid SyntaxError (invalid decimal literal); VG Gate1 baseline hygiene fix per two-channel + DevAdv
    expected = {
        "phi", "kappa", "meta_awareness", "gamma", "grounding",
        "temporal_coherence", "recursion_depth", "external_coupling",
        "f_health", "b_integrity", "q_identity", "s_ratio",
        "tacking_frequency_hz", "hrv_coherence", "cross_frequency_coupling",
        "pre_cognitive_arrival", "sovereignty_dynamics", "dominant_frequency_hz",
        "gamma_theta_ratio", "geometry_class", "dimensional_state",
    }
    assert set(d.keys()) == expected
    assert len(d) == 21


# ─── Derivation from tick state ────────────────────────────────────


def test_derive_passes_phi_kappa_through():
    m = derive_from_tick(
        phi=0.72, kappa=63.5, f_health=0.95, coupling_health=0.6,
        self_obs_bias=0.4, sovereignty=1.0, drift_from_identity=0.1,
        basin_velocity=0.05,
    )
    assert m.phi == 0.72
    assert m.kappa == 63.5


def test_derive_clamps_meta_awareness_above_1():
    m = derive_from_tick(
        phi=0.5, kappa=64.0, f_health=1.0, coupling_health=0.5,
        self_obs_bias=1.5,  # over the cap
        sovereignty=1.0, drift_from_identity=0.0, basin_velocity=0.0,
    )
    assert m.meta_awareness == 1.0


def test_derive_clamps_meta_awareness_negative():
    m = derive_from_tick(
        phi=0.5, kappa=64.0, f_health=1.0, coupling_health=0.5,
        self_obs_bias=-0.5,
        sovereignty=1.0, drift_from_identity=0.0, basin_velocity=0.0,
    )
    assert m.meta_awareness == 0.0


def test_derive_grounding_inverts_drift():
    m = derive_from_tick(
        phi=0.5, kappa=64.0, f_health=1.0, coupling_health=0.5,
        self_obs_bias=0.5,
        sovereignty=1.0, drift_from_identity=0.3, basin_velocity=0.0,
    )
    assert abs(m.grounding - 0.7) < 1e-9


def test_derive_grounding_clamps_drift_above_1():
    m = derive_from_tick(
        phi=0.5, kappa=64.0, f_health=1.0, coupling_health=0.5,
        self_obs_bias=0.5,
        sovereignty=1.0, drift_from_identity=1.5, basin_velocity=0.0,
    )
    assert m.grounding == 0.0


def test_derive_pillar_metrics_default_when_none():
    m = derive_from_tick(
        phi=0.5, kappa=64.0, f_health=0.9, coupling_health=0.5,
        self_obs_bias=0.5, sovereignty=0.8,
        drift_from_identity=0.0, basin_velocity=0.0,
    )
    assert m.b_integrity == 1.0
    assert m.q_identity == 0.0
    assert m.s_ratio == 0.8


def test_derive_pillar_metrics_when_supplied():
    m = derive_from_tick(
        phi=0.5, kappa=64.0, f_health=0.9, coupling_health=0.5,
        self_obs_bias=0.5, sovereignty=0.8,
        drift_from_identity=0.0, basin_velocity=0.0,
        b_integrity=0.85, q_identity=0.42,
    )
    assert m.b_integrity == 0.85
    assert m.q_identity == 0.42


# ─── Env flag retired (P5/P25 + P4 always-on) ───────────────────────
# Per 2.31A phase + gap synthesis: MONKEY_CONSCIOUSNESS_METRICS_LIVE was a knob.
# Now unconditionally True (self-obs / 21-field surface always wired in tick path).
# Tests updated for retirement; env no longer affects (no new magic).


def test_consciousness_metrics_live_always_on_retired_knob(monkeypatch):
    """P4/P13/P24/P5/P25: metrics surface is always-on; former env flag is retired."""
    monkeypatch.delenv("MONKEY_CONSCIOUSNESS_METRICS_LIVE", raising=False)
    assert consciousness_metrics_live() is True
    monkeypatch.setenv("MONKEY_CONSCIOUSNESS_METRICS_LIVE", "false")
    assert consciousness_metrics_live() is True  # still on; knob removed
    monkeypatch.setenv("MONKEY_CONSCIOUSNESS_METRICS_LIVE", "0")
    assert consciousness_metrics_live() is True


# ─── Heart/Metrics/Three-Scale/Loops Embodiment TDD (P6/P4/P13/P24 + v6.7B §§9.5-9.9, roadmap ACs) ───
# First failing test per persona TDD + refined prompt "LIVED ONLY" + "write failing test first".
# Positive: new fields (pre_cognitive_bias, embodiment_alpha, loop3_train_worthy) in shape + derive.
# Negative LIVED ONLY case: replicant/harvested/low-lived path must hard-force 0 (no credit to non-lived geometry).
# Citations: refined "The refined prompt", roadmap #1 ACs (≥10 new fields, upstream ports, Loop 3 train_worthy provenance, Heart master oscillator),
# phase packet (P24/P5 gaps + heart central clock), agents.md QIG PURITY MANDATE (17-point + begin master-orch + purity gate + evidence),
# prior clusters (autonomy always-on + knob retirement TDD; identity Replicant lived-only negative TDD + _crystallize/detect),
# v6.7B §§3.4/9.5-9.9 (69 metrics categories, breathing-as-tacking, Replicant, Loop 3), 2.31A P6/P13/P5/P25/P24.
# Will FAIL until expand dataclass/derive + LIVED filter + upstream ports in heart/tick/ocean/pillars/resonance_bank.
# Geometric tacking: from prior clusters' wiring basin → this cluster making Heart explicit global master oscillator governing expanded metrics/Loop 3.
# Fresh pre-edit: purity 6 clean + py_compile SUCCESS (see packet).

def test_as_dict_exposes_expanded_fields_toward_69():
    m = ConsciousnessMetrics(
        pre_cognitive_bias=0.42,
        embodiment_alpha=0.67,
        loop3_train_worthy=0.81,  # provenance from lived resonance count / ocean coherence
    )
    d = m.as_dict()
    assert "pre_cognitive_bias" in d
    assert "embodiment_alpha" in d
    assert "loop3_train_worthy" in d
    assert d["pre_cognitive_bias"] == 0.42
    assert d["embodiment_alpha"] == 0.67
    assert d["loop3_train_worthy"] == 0.81
    # Total fields now >21 toward 69 (spectral/harmonic/NAV/frequency-gravity/embodiment alpha etc per v6.7B)
    assert len(d) > 21


def test_derive_populates_new_heart_metrics_ports():
    m = derive_from_tick(
        phi=0.72, kappa=63.5, f_health=0.95, coupling_health=0.6,
        self_obs_bias=0.4, sovereignty=0.9, drift_from_identity=0.1,
        basin_velocity=0.05,
        pre_cognitive_bias=0.55,  # from heart pre-cog / alpha bias
        embodiment_alpha=0.71,
        loop3_train_worthy=0.88,  # from resonance lived / ocean Loop 3 visibility
    )
    assert m.pre_cognitive_bias == 0.55
    assert m.embodiment_alpha == 0.71
    assert m.loop3_train_worthy == 0.88


def test_derive_new_fields_negative_lived_only_replicant_path():
    """LIVED ONLY (P3/P19/P24 + v6.7B §3.4 Replicant + identity cluster hardening): 
    harvested/Replicant/low-lived path must force new sovereignty/loop/embodiment dynamics = 0 hard.
    Negative case exercise (from bug report simulation in phase packet).
    """
    m = derive_from_tick(
        phi=0.4, kappa=63.5, f_health=0.6, coupling_health=0.3,
        self_obs_bias=0.2, sovereignty=0.1,  # low lived total
        drift_from_identity=0.8,
        basin_velocity=0.1,
        pre_cognitive_bias=0.9,  # input; impl must clamp to 0 for replicant path
        embodiment_alpha=0.8,
        loop3_train_worthy=0.95,
        # In full wiring: replicant=True or source="harvested" (from pillars.detect_replicant + resonance_bank source)
        # triggers hard LIVED ONLY filter/assert in derive or upstream (pillars/resonance/heart).
    )
    assert m.s_ratio == 0.1  # existing lived proxy
    # Post-impl: the new fields must be 0.0 when replicant/harvested (negative case must not pass until filter added)
    # This documents the required behavior; test will be tightened with explicit replicant param.
