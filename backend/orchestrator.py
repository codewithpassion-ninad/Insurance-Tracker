# orchestrator.py
import pandas as pd
from define_agents import AgentWrapper
from llm_client import LLMClient
import json
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    api_key = os.getenv("LLM_API_KEY")
    endpoint = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")

    missing = [name for name, val in {
        "LLM_API_KEY": api_key,
        "LLM_BASE_URL": endpoint,
        "LLM_MODEL": model,
    }.items() if not val]

    if missing:
        raise ValueError(f"Missing required env vars: {', '.join(missing)}")

    return LLMClient(
        api_key=api_key,
        endpoint=endpoint,
        model=model
    )

try:
    llm = get_llm()
except Exception as e:
    print("[Orchestrator] Warning:", e)
    llm = None


def process_claims_batch(claims_csv: str, documents_map: dict, policy_text: str, employee_csv: str, out_jsonl: str):
    """
    claims_csv: path to claims CSV (structured + synthetic)
    documents_map: dict mapping claim_id -> {"medical_report": path, "prescription": path, ...}
    outputs a JSONL file with each claim's structured data + agent verdicts + features
    """
    df = pd.read_csv(claims_csv)
    agent = AgentWrapper(llm)
    with open(out_jsonl, "w", encoding="utf8") as fout:
        for _, row in tqdm(df.iterrows(), total=len(df)):
            claim_id = row.get("claim_id")
            docs = documents_map.get(claim_id, {})
            res = agent.run_full_investigation(row.to_dict(), docs, employee_csv)
            out = {"claim_id": claim_id, "structured": res.get("structured"), "summary": res.get("summary"), "agent_results": res.get("agent_results"), "fraud_label": row.get("fraud_label")}
            fout.write(json.dumps(out) + "\n")
    print("Done. Wrote", out_jsonl)
