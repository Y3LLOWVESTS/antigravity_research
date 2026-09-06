"""Regression tests for configurable AGMINER energy policy."""

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.energy import hard_energy_gate
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.storage import Storage


def test_policy_defaults_to_strict_sub_10_mj():
    policy = current_energy_policy()
    assert policy["limit_j"] == 1.0e7
    assert policy["unit"] == "MJ"
    assert policy["comparison"] == "LT"
    assert not policy["inclusive"]


def test_environment_override_to_5_mj(monkeypatch):
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_VALUE", "5")
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_UNIT", "MJ")
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_COMPARISON", "LT")
    policy = current_energy_policy()
    assert policy["limit_j"] == 5.0e6
    assert hard_energy_gate(4.999999e6).passed
    assert not hard_energy_gate(5.0e6).passed


def test_equivalent_mj_and_gj_targets_share_policy_id(monkeypatch):
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_VALUE", "10")
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_UNIT", "MJ")
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_COMPARISON", "LT")
    first = current_energy_policy()["policy_id"]
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_VALUE", "0.01")
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_UNIT", "GJ")
    second = current_energy_policy()["policy_id"]
    assert first == second


def test_objective_rejection_reopens_if_policy_changes(tmp_path, monkeypatch):
    storage = Storage(tmp_path / "agminer.sqlite3")
    candidate = Candidate(
        family_id="POLICY_TEST",
        family_version="1",
        params={"energy_j": 12.0e6},
        physical_model_version="P1",
        energy_ledger_version="L1",
    )
    storage.record_candidate(candidate)
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_VALUE", "10")
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_UNIT", "MJ")
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_COMPARISON", "LT")
    decision = hard_energy_gate(12.0e6)
    storage.reject(
        candidate.candidate_id,
        state=str(decision.state),
        failure_code=str(decision.failure_code),
        gate="energy_objective",
        energy_j=12.0e6,
        run_id="TEST",
    )
    assert storage.is_terminal(candidate.candidate_id)
    monkeypatch.setenv("AGMINER_ENERGY_TARGET_VALUE", "20")
    assert not storage.is_terminal(candidate.candidate_id)
    storage.close()
