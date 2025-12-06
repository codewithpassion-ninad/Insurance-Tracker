import os
from llm_client import LLMClient


def get_llm():
    """
    Lazy-load LLMClient only when first needed.
    This prevents import-time crashes if env variables are not set.
    """
    api_key = os.getenv("LLM_API_KEY")
    endpoint = os.getenv("LLM_ENDPOINT")
    model = os.getenv("LLM_MODEL")

    missing = []
    if not api_key: missing.append("LLM_API_KEY")
    if not endpoint: missing.append("LLM_ENDPOINT")
    if not model: missing.append("LLM_MODEL")

    if missing:
        raise ValueError(
            f"Missing required environment variables for LLMClient: {', '.join(missing)}"
        )

    return LLMClient(
        api_key=api_key,
        endpoint=endpoint,
        model=model
    )


class FraudCQLAgent:
    """
    Agent responsible for generating multiple CQL queries
    for fraud detection using the registered fraud_cql_generator prompt.
    """

    def __init__(self, llm=None):
        # If no LLM passed, use the lazy loader
        self.llm = llm or get_llm()
        self.prompt_name = "fraud_cql_generator"

    def generate_queries(self, fraud_scenario: str, schema_info: dict = None):
        payload = {
            "fraud_scenario": fraud_scenario,
            "schema_info": schema_info or {}
        }

        return self.llm.run(
            prompt=self.prompt_name,
            data=payload
        )


# Export a safely initialized agent
try:
    fraud_cql_agent = FraudCQLAgent()
except ValueError as e:
    # Do not crash the whole app on import — log the issue instead
    print(f"[FraudCQLAgent] Warning: {e}")
    fraud_cql_agent = None
