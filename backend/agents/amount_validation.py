# agents/amount_validation.py

def amount_check(claim_amount: float, claim: int) -> dict:
    if claim == 0:
        policy_limit = 35000
    elif claim == 1:
        policy_limit = 50000
    elif claim == 2:
        policy_limit = 100000

    issues = []
    if claim_amount is None:
        return {"valid": False, "reason": "no_amount"}
    if claim_amount > policy_limit:
        issues.append("above_policy_limit")
    # sample heuristic: if line items sum mismatch
    return {"valid": len(issues)==0, "issues": issues}
