from llm_client import LLMClient
import json

def policy_check(llm: LLMClient, policy_kb: str, claim: dict) -> dict:
    # Use keys matching your template placeholders
    resp = llm.run(
        "policy_check_agent",
        policy_kb=policy_kb,
        claim=claim
    )

    try:
        return json.loads(resp)
    except Exception:
        return {"verdict": "unknown", "reasons": [resp]}
