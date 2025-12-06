import streamlit as st
from PIL import Image
import json
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import io
import fitz  # PyMuPDF
import easyocr
from langchain_openai import ChatOpenAI
import numpy as np
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
import httpx
from langchain.schema import HumanMessage
import re
import hashlib


# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()
client = httpx.Client(verify=False)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "admin@123")
API_KEY = os.getenv("API_KEY", "sk-u89exSyhUYtZPjoUCvxS0A")

if not API_KEY:
    raise Exception("❌ OPENAI_API_KEY missing in environment variables")

# ---------------------------------------------------
# OpenAI GPT client
# ---------------------------------------------------
BASE_URL = os.getenv("LLM_BASE_URL", "https://genailab.tcs.in")

CHAT_MODEL = os.getenv("LLM_MODEL", "azure_ai/genailab-maas-DeepSeek-V3-0324")
llm = ChatOpenAI(
    base_url=BASE_URL,
    model=CHAT_MODEL,
    api_key=API_KEY,
    http_client=client,
)

# HTTP client for internal use
http_client = httpx.Client(verify=False)

#openai.api_key = OPENAI_API_KEY

tiktoken_cache_dir = "./tiktoken_cache"
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

# validate
assert os.path.exists(os.path.join(tiktoken_cache_dir,"9b5ad71b2ce5302211f9c61530b329a4922fc6a4"))

# ---------------------------------------------------
# Unique key utilities
# ---------------------------------------------------
def compute_unique_key(props: dict) -> str:
    cleaned_props = {k: str(v).strip().lower() for k, v in props.items()
                     if v is not None and v != ""}
    return hashlib.md5(json.dumps(cleaned_props, sort_keys=True).encode()).hexdigest()


def get_node_unique_key(label, props):
    key = compute_unique_key(props)
    if not label or not isinstance(label, str):
        raise ValueError("Label must be a non-empty string")

    with neo4j_driver.session() as session:
        result = session.run(
            f"MATCH (n:{label} {{unique_key: $key}}) RETURN n.unique_key AS unique_key",
            {"key": key}
        )
        record = result.single()
        return record["unique_key"] if record else key

# ---------------------------------------------------
# Neo4j Connection
# ---------------------------------------------------
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# ---------------------------------------------------
# Dynamic graph insertion (corrected)
# ---------------------------------------------------

def insert_dynamic_graph(graph_data):
    try:
        with neo4j_driver.session() as session:
            # Insert nodes
            for node in graph_data.get("nodes", []):
                if "label" not in node:
                    st.warning(f"Skipping node, missing 'label': {node}")
                    continue
                props = node.get("properties", {})
                unique_key = compute_unique_key(props)
                session.run(
                    f"""
                    MERGE (n:{node['label']} {{unique_key: $unique_key}})
                    SET n += $properties
                    """,
                    {"unique_key": unique_key, "properties": props}
                )

            # Insert relationships
            for rel in graph_data.get("relationships", []):
                if "start_label" not in rel or "end_label" not in rel or "type" not in rel:
                    st.warning(f"Skipping relationship, missing keys: {rel}")
                    continue

                start_props = rel.get("start_properties", {})
                end_props = rel.get("end_properties", {})
                start_key = get_node_unique_key(rel["start_label"], start_props)
                end_key = get_node_unique_key(rel["end_label"], end_props)

                rel_props = rel.get("properties", {})
                rel_unique_key = compute_unique_key({
                    "start": start_key,
                    "end": end_key,
                    "type": rel.get("type"),
                    **rel_props
                })

                session.run(
                    f"""
                    MATCH (a:{rel['start_label']} {{unique_key: $start_key}})
                    MATCH (b:{rel['end_label']} {{unique_key: $end_key}})
                    MERGE (a)-[r:{rel['type']} {{unique_key: $rel_unique_key}}]->(b)
                    SET r += $properties
                    """,
                    {
                        "start_key": start_key,
                        "end_key": end_key,
                        "rel_unique_key": rel_unique_key,
                        "properties": rel_props
                    }
                )
    except Exception as e:
        st.error(f"Neo4j insertion failed: {e}")


# ---------------------------------------------------
# OCR Functions
# ---------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    """
    Extract text from PDF using PyMuPDF (NO POPPLER REQUIRED).
    uploaded_file can be:
       - a file path
       - an UploadedFile object (Streamlit / Django)
    """
    try:
        # If it's an UploadedFile object, read bytes
        if hasattr(uploaded_file, "read"):
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        else:
            doc = fitz.open(uploaded_file)

        text = ""
        for page in doc:
            text += page.get_text()

        return text.strip()

    except Exception as e:
        raise RuntimeError(f"PDF Extraction Error: {e}")

reader = easyocr.Reader(['en'])


def extract_text_from_image(uploaded_file):
    """
    Extract text from images using EasyOCR.
    Supports UploadedFile objects and file paths.
    """
    try:
        if hasattr(uploaded_file, "read"):
            # UploadedFile object → convert to bytes → Pillow image
            import numpy as np
            from PIL import Image
            file_bytes = uploaded_file.read()
            image = Image.open(io.BytesIO(file_bytes))
            image_np = np.array(image)
        else:
            image_np = uploaded_file  # file path or numpy array

        result = reader.readtext(image_np, detail=0)
        return "\n".join(result)

    except Exception as e:
        raise RuntimeError(f"Image OCR Error: {e}")


# ---------------------------------------------------
# LLM Claim Extraction Dynamic 
# ---------------------------------------------------
def extract_claim_data_with_gpt(raw_text):
    """
    Uses GPT model to convert extracted OCR text into structured JSON.
    """
    prompt = f"""
    You are an expert medical-claims information extraction system.

    Extract ALL possible fields from the text.
    - No fixed schema.
    - Include every attribute you detect.
    - Preserve structure and group related fields.
    - Use nested JSON.
    - Use lists where appropriate.

    Return ONLY valid JSON.

    --- TEXT START ---
    {raw_text}
    --- TEXT END ---
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        output_text = response.content

        # Remove markdown ```json ... ``` if present
        match = re.search(r"```json\s*(\{.*?\})\s*```", output_text, re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            json_text = output_text  # fallback if no code block

        claim_json = json.loads(json_text)
        return claim_json

    except Exception as e:
        st.error(f"LLM Extraction Error: {e}")
        return {}

# ---------------------------------------------------
# Fetch Existing Neo4j Schema
# ---------------------------------------------------
def get_existing_neo4j_schema():
    with neo4j_driver.session() as session:
        # Using CALL db.labels() instead of db.schema.nodeTypeProperties()
        node_labels_result = session.run("CALL db.labels()")
        node_labels = [record["label"] for record in node_labels_result]

        # Using CALL db.relationshipTypes() instead of db.schema.relationshipTypeProperties()
        rel_types_result = session.run("CALL db.relationshipTypes()")
        rel_types = [record["relationshipType"] for record in rel_types_result]

        return {"existing_nodes": node_labels, "existing_relationships": rel_types}

# ---------------------------------------------------
# Dynamic Schema Generation via LLM
# ---------------------------------------------------
# ---------------------------------------------------
# Dynamic Schema Generation via LLM (Updated Prompt)
# ---------------------------------------------------
def generate_graph_schema_llm(claim_json, existing_schema):
    """
    Generate dynamic graph schema using GPT.
    Ensures all nodes have 'label' and relationships have start/end/type.
    """
    prompt = f"""
Convert the extracted claim JSON into a Neo4j graph.

RULES:
1. Standard node labels (Patient, Hospital, Doctor, Diagnosis, Bill, Policy)
2. Normalize all properties (_name → name, _id → id, _date → date)
3. Generate 'unique_key' for each node (hash of all properties)
4. Auto-detect relationships between nodes based on context
5. Compare with EXISTING NEO4J SCHEMA; avoid duplicates
6. **ALL nodes must have a 'label'**
7. **ALL relationships must have 'start_label', 'end_label', and 'type'**
8. Include all node properties from claim_json

EXISTING SCHEMA:
{json.dumps(existing_schema, indent=2)}

CLAIM JSON:
{json.dumps(claim_json, indent=2)}

Output strict JSON with "nodes" and "relationships". Return ONLY JSON.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    # Parse JSON safely
    match = re.search(r"\{[\s\S]*\}", response.content)
    if not match:
        raise ValueError("LLM did not return valid JSON")
    graph_json = json.loads(match.group(0))

    # Validate nodes
    for node in graph_json.get("nodes", []):
        if "label" not in node:
            st.warning(f"Node missing 'label', assigning 'Unknown': {node}")
            node["label"] = "Unknown"

    # Validate relationships
    for rel in graph_json.get("relationships", []):
        for key in ["start_label", "end_label", "type"]:
            if key not in rel:
                st.warning(f"Relationship missing '{key}', skipping: {rel}")
                rel[key] = "Unknown"

    return graph_json


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.title("📄 Medical Bill → Neo4j Extraction System")
st.write("Upload a medical bill (PDF or Image) and the system will extract and store structured data.")

uploaded_file = st.file_uploader("Upload PDF, JPG, PNG", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    st.info("⏳ Processing your file...")

    # Step 1 — OCR
    if file_type == "pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
    else:
        raw_text = extract_text_from_image(uploaded_file)

    st.subheader("📘 Extracted Text (OCR)")
    st.text_area("Raw OCR Output:", raw_text, height=250)

    # Step 2 — LLM Structuring (Dynamic JSON)
    st.info("🔍 Extracting structured information using GPT...")
    claim_data = extract_claim_data_with_gpt(raw_text)

    st.subheader("🧾 Structured Claim Data")
    st.json(claim_data)

    # Generate Dynamic Graph 
    existing_schema = get_existing_neo4j_schema()
    graph_schema = generate_graph_schema_llm(claim_data, existing_schema)

    st.subheader("📊 Generated Graph Schema")
    st.json(graph_schema)

    # Insert Dynamic Graph
    insert_dynamic_graph(graph_schema)
    st.success("✅ Dynamic claim graph inserted into Neo4j!")
