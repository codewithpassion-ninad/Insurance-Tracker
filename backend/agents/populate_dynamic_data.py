import os
from neo4j import GraphDatabase
from llm_client import LLMClient
import httpx

api_key = os.getenv("LLM_API_KEY")
llm = LLMClient(api_key=api_key)

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# HTTP client for internal use
# tiktoken_cache_dir = "./tiktoken_cache"
# os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

# # validate
# assert os.path.exists(os.path.join(tiktoken_cache_dir,"9b5ad71b2ce5302211f9c61530b329a4922fc6a4"))

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


