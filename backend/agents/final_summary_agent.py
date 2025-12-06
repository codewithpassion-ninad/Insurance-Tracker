# agents/final_summary_agent.py
from typing import List, Dict

def aggregate_results(agent_results: List[Dict]) -> Dict:
    score = 0.0
    reasons = []
    for r in agent_results:
        if not r: continue
        # r expected to have keys like 'valid' (bool) or 'verdict', 'issues', 'confidence'
        if isinstance(r, dict):
            if r.get("valid") is False or r.get("verdict") in ["invalid", "non_compliant", "invalid"]:
                score += 1.0
                reasons.append(r.get("reason") or r.get("issues") or r.get("verdict"))
            # use confidence to moderate
            if "confidence" in r:
                score += (1 - float(r["confidence"])) * 0.2
            if r.get("issues"):
                score += len(r["issues"]) * 0.5
    # normalize to 0-1
    max_possible = max(1.0, len(agent_results) * 1.0 + 1.0)
    norm = min(1.0, score / max_possible)
    if norm < 0.3:
        level = "low"
    elif norm < 0.7:
        level = "medium"
    else:
        level = "high"
    return {"risk_score": norm, "risk_level": level, "reasons": reasons}
