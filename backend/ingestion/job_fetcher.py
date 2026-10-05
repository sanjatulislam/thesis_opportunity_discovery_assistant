import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from helpers.constants import (
    JOBTECH_URL,
    JOBTECH_REQUEST_HEADER,
    JOBTECH_REQUEST_TIMEOUT,
    JOBTECH_REQUEST_LIMIT
)

import requests

def get_jobs(query: str) -> list[dict]:
    try:
        response = requests.get(
            JOBTECH_URL,
            params={"q": query, "limit": JOBTECH_REQUEST_LIMIT},
            headers=JOBTECH_REQUEST_HEADER,
            timeout=JOBTECH_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json().get("hits", [])

    except Exception as e:
        print(f"Request failed: {e}")
        return []

