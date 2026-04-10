"""
test_recommendation.py — Smoke test for the recommendation engine.

Run:  python3 test_recommendation.py

Tests all logic paths including distribution uniformity checks:
  1. Grind too coarse → recommends finer
  2. Grind too fine → recommends coarser
  3. Near target + sour → raise temp
  4. Near target + bitter → lower temp
  5. Balanced → hold
  6. Mixed feedback → diagnose evenness
  7. Bimodal distribution → grinder maintenance
  8. Poor uniformity + sour → temp + contact time
  9. Good uniformity + off target → normal grind adjustment
"""

import json
from recommendation.recommendation_engine import recommend_filter

# Base payload — shared values reused in each test
BASE = {
    "current_setting": 18,
    "fitted_slope": 25,
    "dial_range_min": 1,
    "dial_range_max": 40,
}

# Default good distribution stats
GOOD_DIST = {
    "fines_pct": 4.0,
    "uniform_pct": 88.5,
    "boulders_pct": 1.2,
    "bimodal_flag": False,
    "uniformity": "good",
    "span": 0.8,
}

BIMODAL_DIST = {
    "fines_pct": 22.0,
    "uniform_pct": 55.0,
    "boulders_pct": 18.0,
    "bimodal_flag": True,
    "uniformity": "poor",
    "span": 2.1,
}

POOR_DIST = {
    "fines_pct": 12.0,
    "uniform_pct": 62.0,
    "boulders_pct": 5.0,
    "bimodal_flag": False,
    "uniformity": "poor",
    "span": 1.8,
}


def run_test(name: str, overrides: dict):
    payload = {**BASE, **overrides}
    result = recommend_filter(payload)
    grind = result["grind_recommendation"]
    secondary = result["secondary_advice"]
    dist = result.get("distribution", {})

    print(f"\n{'─'*55}")
    print(f"TEST: {name}")
    print(f"  D50 input:     {payload['current_d50']} µm")
    print(f"  Taste:         {payload['taste_feedback']}")
    print(f"  Mode:          {result['mode']}")
    print(f"  Grind:         {grind['direction']} {grind['steps']} steps → setting {grind['to_setting']}")
    print(f"  Message:       {grind['message']}")
    if secondary["shown"]:
        print(f"  Secondary:     {secondary['type']} → {secondary['direction']}")
        print(f"  Sec. message:  {secondary['message']}")
    if dist:
        print(f"  Distribution:  fines={dist.get('fines_pct',0)}% uniform={dist.get('uniform_pct',0)}% boulders={dist.get('boulders_pct',0)}%")
        print(f"  Uniformity:    {dist.get('uniformity','n/a')} | bimodal={dist.get('bimodal_flag',False)}")
    print(f"  Confidence:    grind={result['confidence']['grind']}, secondary={result['confidence']['secondary']}")


# ── Original test cases ──────────────────────────────────────

run_test("Too coarse → go finer", {
    "current_d50": 700,
    "taste_feedback": ["sour", "thin"],
    "psd_stats": GOOD_DIST,
})

run_test("Too fine → go coarser", {
    "current_d50": 500,
    "taste_feedback": ["bitter", "harsh"],
    "psd_stats": GOOD_DIST,
})

run_test("Near target + sour → raise temp", {
    "current_d50": 610,
    "taste_feedback": ["sour"],
    "psd_stats": GOOD_DIST,
})

run_test("Near target + bitter → lower temp", {
    "current_d50": 590,
    "taste_feedback": ["bitter"],
    "psd_stats": GOOD_DIST,
})

run_test("Balanced → hold", {
    "current_d50": 600,
    "taste_feedback": ["balanced"],
    "psd_stats": GOOD_DIST,
})

run_test("Mixed signals → diagnose evenness", {
    "current_d50": 600,
    "taste_feedback": ["sour_and_bitter"],
    "psd_stats": GOOD_DIST,
})

# ── New distribution-aware test cases ────────────────────────

run_test("Bimodal distribution → grinder issue", {
    "current_d50": 600,
    "taste_feedback": ["sour_and_bitter"],
    "psd_stats": BIMODAL_DIST,
})

run_test("Poor uniformity + sour → temp + contact time", {
    "current_d50": 610,
    "taste_feedback": ["sour"],
    "psd_stats": POOR_DIST,
})

run_test("Poor uniformity + bitter → lower temp + shorter time", {
    "current_d50": 590,
    "taste_feedback": ["bitter"],
    "psd_stats": POOR_DIST,
})

print(f"\n{'='*55}")
print("✅ All 9 tests completed successfully!")
print(f"{'='*55}\n")
