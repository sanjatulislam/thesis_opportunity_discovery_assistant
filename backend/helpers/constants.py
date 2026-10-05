JOBTECH_URL = "https://jobsearch.api.jobtechdev.se/search"
JOBTECH_REQUEST_TIMEOUT = 30.0 
JOBTECH_REQUEST_RETRIES = 3
JOBTECH_REQUEST_HEADER = { "accept": "application/json" }
JOBTECH_REQUEST_LIMIT = 20

EMPLOYMENT_TYPES = ["master thesis", "examensarbete", "exjobb"]
JOB_FIELDS = {
    "Artificial Intelligence": ["AI"],
    "Machine Learning": ["ML"],
    "Large Language Model": ["LLM", "RAG"],
    "Agentic AI": ["AI agent"]
}