# agents/safety_agent.py
from llm_client import get_llm
from llm_client import LLMClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("LLM_API_KEY", "sk-u89exSyhUYtZPjoUCvxS0A")
endpoint = os.getenv("LLM_ENDPOINT", "https://genailab.tcs.in")
model = os.getenv("LLM_MODEL", "azure_ai/genailab-maas-DeepSeek-V3-0324")

from llm_client import get_llm

llm = get_llm()

def safety_check_agent(llm_instance, user_text: str) -> bool:
    """Return True if safe, False otherwise."""
    resp = llm.run(prompt_name="safety_check_agent", nl_prompt=user_text)
    return resp.strip().lower() == "safe"
