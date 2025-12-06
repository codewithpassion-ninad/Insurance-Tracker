from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import json
import uuid
import os
import tempfile

from orchestrator import process_claims_batch
from define_agents import AgentWrapper
from llm_init import llm

# ---------------------------------------------------
# CREATE ONLY ONE FASTAPI INSTANCE
# ---------------------------------------------------
app = FastAPI()

# ---------------------------------------------------
# CORS MIDDLEWARE
# ---------------------------------------------------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = AgentWrapper(llm)

# ---------------------------------------------------
# MODELS
# ---------------------------------------------------



# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Fraud Detection API Running"}


# ---------------------------------------------------
# SINGLE CLAIM EVALUATION (with files)
# ---------------------------------------------------
@app.post("/evaluate")
async def evaluate(files: List[UploadFile] = File(...)):
    """
    Accepts PDF/image files from frontend, saves them temporarily,
    and passes them to the run_full_investigation function.
    """

    if not files:
        return {"status": "error", "message": "No files uploaded"}

    # Save uploaded files temporarily
    document_paths = {}
    temp_dir = tempfile.mkdtemp()
    try:
        for file in files:
            # Save each file with its original filename in temp directory
            temp_path = os.path.join(temp_dir, file.filename)
            with open(temp_path, "wb") as f:
                content = await file.read()
                f.write(content)
            # Use filename (without extension logic) as key or full name if you want
            key = os.path.splitext(file.filename)[0].lower()  # e.g., "bill.pdf" -> "bill"
            document_paths[key] = temp_path

        # Run the full investigation
        results = agent.run_full_investigation(document_paths)

        return {
            "status": "success",
            "results": results
        }

    finally:
        # Optionally delete temp files after processing
        for path in document_paths.values():
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


# ---------------------------------------------------
# BATCH PROCESSING
# ---------------------------------------------------
@app.post("/process_batch")
def run_batch(
    claims_csv: str,
    docs_map_json: str,
    policy_text: str,
    employee_csv: str
):
    docs_map = json.loads(docs_map_json)

    out_file = f"outputs/batch_{uuid.uuid4().hex}.jsonl"

    process_claims_batch(claims_csv, docs_map, policy_text, employee_csv, out_file)

    return {"status": "done", "output_file": out_file}


# ---------------------------------------------------
# FETCH HIGH-RISK CLAIMS
# ---------------------------------------------------
@app.get("/claims/highrisk")
def get_high_risk_claims():
    df = pd.read_json("outputs/latest_results.jsonl", lines=True)
    high_risk = df[df["summary"].str.contains("high", case=False, na=False)]
    return high_risk.to_dict(orient="records")


# ---------------------------------------------------
# FETCH CLAIM BY ID
# ---------------------------------------------------
@app.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    df = pd.read_json("outputs/latest_results.jsonl", lines=True)
    row = df[df["claim_id"] == claim_id]

    if row.empty:
        return {"error": "not_found"}

    return row.iloc[0].to_dict()


# ---------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------
# @app.post("/chat")
# def chat(req: ChatRequest):
#     response = llm.run("safety_check_agent", nl_prompt=req.query)
#     return {"response": response}


# ---------------------------------------------------
# DOCUMENT UPLOAD
# ---------------------------------------------------
@app.post("/upload_document")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    # your real text extraction logic will go here
    extracted_text = f"Extracted text placeholder for file: {file.filename}"

    return {"filename": file.filename, "extracted_text": extracted_text}
