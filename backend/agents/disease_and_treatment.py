# agents/disease_and_treatment.py
from llm_client import LLMClient
import json

def disease_treatment_check(llm: LLMClient, claim_type: str, treatment: str) -> dict:
    # quick LLM check using the binary_validator prompt
    facts = {"diagnosis": claim_type, "treatment": treatment}
    resp = llm.run(prompt_name="binary_validator", nl_prompt=None, context=f"Validate treatment for diagnosis", facts=json.dumps(facts))
    try:
        return json.loads(resp)
    except:
        return {"verdict":"invalid","reason":resp,"confidence":0.0}
