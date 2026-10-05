import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ingestion.job_fetcher import get_jobs
from models.job_ad import JobAd

from typing import Optional

def build_search_queries(job_fields: dict[str, list[str]], 
                         employment_types: list[str]) -> list[str]:
    fields = []
    for field, synonyms in job_fields.items():
        fields.append(field)
        fields.extend(synonyms)

    queries = []
    for field in fields:
        for emp_type in employment_types:
            queries.append(f"{field} {emp_type}")

    return queries


def normalize(ad: dict) -> Optional[JobAd]:
    if ad and ad.get("id"):
        return JobAd(
            id = ad.get("id") or "",
            title = ad.get("headline") or "",
            employer = (ad.get("employer") or {}).get("name") or "",
            cities = [
                addr["municipality"]
                for addr in ad.get("workplace_addresses") or []
                if addr.get("municipality")
            ],
            application_deadline = ad.get("application_deadline"),
            publication_date = ad.get("publication_date"),
            description = (ad.get("description") or {}).get("text") or "",
            url = ad.get("webpage_url") or ""
        )

    return None


def fetch_jobs(queries: list[str]) -> list[JobAd]:
    all_ads: dict[str, JobAd] = {}

    for query in queries:
        hits = get_jobs(query)
        print(f"{query}: total {len(hits)} job ads")

        for ad in hits:
            ad_id: Optional[str] = ad.get("id")
            if ad_id and ad_id not in all_ads:
                all_ads[ad_id] = normalize(ad)

    print(f"{len(all_ads)} unique ads")
    
    return list(all_ads.values())









