# llm_init.py
from llm_client import LLMClient
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
import os
from llm_client import LLMClient

def get_llm():
    api_key = os.getenv("LLM_API_KEY")
    endpoint = os.getenv("LLM_ENDPOINT")
    model = os.getenv("LLM_MODEL")

    missing = [
        name for name, val in {
            "LLM_API_KEY": api_key,
            "LLM_ENDPOINT": endpoint,
            "LLM_MODEL": model,
        }.items() if not val
    ]

    if missing:
        raise ValueError(
            f"Missing required env vars for LLMClient: {', '.join(missing)}"
        )

    return LLMClient(
        api_key=api_key,
        endpoint=endpoint,
        model=model,
    )

# DO NOT instantiate the LLM here!
llm = None

try:
    llm = get_llm()
except Exception as e:
    print("[llm_init] Warning:", e)


# Safety agent prompt
llm.register_prompt(
    "safety_check_agent",
    """
    You are a safety classifier. Answer ONLY "Safe" or "Unsafe".
    Classify the user's query. If it includes disallowed dangerous instructions, explicit personal data extraction or illegal acts -> "Unsafe".
    User Query: {nl_prompt}
    """
)

# A generic validator prompt template for investigation agents.
llm.register_prompt(
    "binary_validator",
    """
    You are a validation assistant. You will be given CONTEXT and FACTS to validate.
    Return JSON only with keys:
    - verdict: 'valid' or 'invalid'
    - reason: short sentence
    - confidence: 0-1 (float)
    Input:
    CONTEXT: {context}
    FACTS: {facts}
    """
)

# Policy checker prompt
llm.register_prompt(
    "policy_check_agent",
    """
    You are a policy validation agent. Given policy_text and claim_facts, decide:
    - verdict: 'compliant'|'non_compliant'
    - reasons: short list
    - matched_rules: list
    Return JSON only.
    Policy: {policy_kb}
    Claim: {claim}
    """
)

# Medical doc validator
llm.register_prompt(
    "medical_doc_validator",
    """
    You are a medical document validator. Given extracted_text and expected_fields (like diagnosis, discharge_date, doctor, procedure),
    return JSON:
    - ok: true/false
    - missing_fields: []
    - suspicious_phrases: []
    - confidence: 0-1
    """
)

# You can register more targeted prompts (hospital_check, employee_check...) using the binary_validator/policy templates above.


llm.register_prompt(
    "fraud_cql_generator",
    """
    You are a fraud-pattern CQL generation expert.
    Given the input:
    - fraud_scenario: a description of suspicious behaviour (e.g., abnormal claims, repeated patterns, unusual doctor-patient frequencies)
    - schema_info: optional database schema details (tables, relationships, fields)

    Produce **multiple CQL queries** (3-7 queries) that investigate:
      - anomalies
      - unusual frequencies
      - duplicate patterns
      - cross-patient correlations
      - doctor-level irregularities
      - claim inflation indicators

    Output STRICT JSON:
    {
      "queries": [
        {"description": "...", "cql": "..."},
        ...
      ],
      "risk_level": "low | medium | high",
      "confidence": 0-1
    }
    """
)
