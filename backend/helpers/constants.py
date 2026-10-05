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

AUDIT_COLUMN_CREATED_AT="created_at"
AUDIT_COLUMN_UPDATED_AT="updated_at"

AUDIT_COLUMNS_SQL = f"""created_at TIMESTAMPTZ NOT NULL, 
                        updated_at TIMESTAMPTZ"""


JOBS_TABLE="jobs"
JOBS_TABLE_ID = "id"
JOBS_TABLE_URL = "url"
JOBS_TABLE_POSTED_AT = "posted_at"
JOBS_TABLE_APPLICATION_DEADLINE_AT = "application_deadline_at"
JOBS_TABLE_TITLE = "title"
JOBS_TABLE_COMPANY = "company"
JOBS_TABLE_LOCATIONS = "locations"
JOBS_TABLE_DESCRIPTION = "description"
JOBS_TABLE_EMBEDDING_TEXT = "embedding_text"
JOBS_TABLE_IS_DELETED="is_deleted"