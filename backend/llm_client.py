import os
from dotenv import load_dotenv
from typing import Dict, Any
from langchain_openai import ChatOpenAI
import httpx
import json


load_dotenv()

# -------------------------
# Define LLMClient first
# -------------------------
class LLMClient:
    def __init__(self, api_key: str, endpoint: str, model: str):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.prompts: Dict[str, str] = {}

    def register_prompt(self, name: str, template: str):
        """Register a prompt template with a name."""
        self.prompts[name] = template

    # Example method to call the LLM (you can customize)
    def generate(self, prompt: str) -> str:
        # Here you would use ChatOpenAI or httpx to call your LLM endpoint
        return f"Generated response for: {prompt}"
    
    def run(self, prompt_name: str, **kwargs) -> str:
        """
        Execute a registered prompt by name with keyword variables.
        Example:
            llm.run("policy_check_agent", policy="text", claim={...})
        """
        if prompt_name not in self.prompts:
            raise ValueError(f"Prompt '{prompt_name}' not registered.")

        template = self.prompts[prompt_name]

        # Convert dict arguments to JSON-friendly strings
        processed = {
            key: (json.dumps(value) if isinstance(value, dict) else value)
            for key, value in kwargs.items()
        }

        # Format template using {variable} placeholders
        prompt_text = template.format(**processed)

        return self.generate(prompt_text)


# -------------------------
# Then define get_llm
# -------------------------
def get_llm():
    api_key = os.getenv("LLM_API_KEY")
    endpoint = os.getenv("LLM_ENDPOINT")
    model = os.getenv("LLM_MODEL")

    missing = [name for name, val in {
        "LLM_API_KEY": api_key,
        "LLM_ENDPOINT": endpoint,
        "LLM_MODEL": model,
    }.items() if not val]

    if missing:
        raise ValueError(f"Missing required env vars: {', '.join(missing)}")

    return LLMClient(
        api_key=api_key,
        endpoint=endpoint,
        model=model,
    )

# -------------------------
# Initialize the client
# -------------------------
try:
    llm = get_llm()
except Exception as e:
    print("[llm_init] Warning:", e)
    llm = None

# Register prompts conditionally
if llm:
    llm.register_prompt(
        "fraud_cql_generator",
        "Put your template here."
    )
else:
    print("[llm_init] Prompt registration skipped (LLM not initialized)")
