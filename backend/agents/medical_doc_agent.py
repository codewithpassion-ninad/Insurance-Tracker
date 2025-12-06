# agents/medical_doc_agent.py
from llm_client import LLMClient
import json

def validate_medical_doc(llm: LLMClient, extracted_text: str, expected_fields: list) -> dict:
    prompt_input = {
        "extracted_text": extracted_text,
        "expected_fields": expected_fields
    }
    resp = llm.run(prompt_name="medical_doc_validator", nl_prompt=None)
    # we assume the prompt returns JSON — safe parsing:
    try:
        return json.loads(resp)
    except:
        return {"ok": False, "missing_fields": [], "suspicious_phrases":[resp], "confidence": 0.0}
