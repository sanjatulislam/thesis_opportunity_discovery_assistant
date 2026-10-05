JOBTECH_URL = "https://jobsearch.api.jobtechdev.se/search"
JOBTECH_REQUEST_TIMEOUT = 30.0 
JOBTECH_REQUEST_RETRIES = 3
JOBTECH_REQUEST_HEADER = { "accept": "application/json" }
JOBTECH_REQUEST_LIMIT = 50
JOBTECH_REQUEST_SORTING = "relevance"

EMPLOYMENT_TYPES = ["master thesis", "examensarbete", "exjobb", "degree project"]
JOB_FIELDS = {
    "Artificial Intelligence": ["AI"],
    "Machine Learning": ["ML", "Deep Learning", "Computer Vision", "Reinforcement Learning"],
    "Large Language Model": ["LLM", "RAG"],
    "Agentic AI": ["AI agent"]
}

THESIS_EMPLOYMENT_TYPE_KEYWORDS = ["thesis", "examensarbete", "exjobb", "degree project"]

QWEN_MODEL="qwen/qwen3.8-27b"
QWEN_SKIP_REASONING="none"
LLM_DEFAULT_TEMP=0
MAX_OUTPUT_TOKEN=900

EMBEDDING_MODEL="jinaai/jina-embeddings-v5-text-nano"
EMBEDDING_DIMENSION=768
EMBEDDING_MODEL_REVISION="8a7f00a"

MAX_RESULTS_RETRIVAL=20
MAX_RESULTS_RERANKED=10
RERANKING_MODEL="rerank-v3.5"
