import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ingestion.job_fetcher import get_jobs
from dto.job_ad import JobAd
from helpers.utils import parse_datetime_isoformat, get_datetime_local, clean_text
from ingestion.job_employment_checker import is_thesis_ad

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

def is_job_application_open(application_deadline) -> bool:
    if not application_deadline:
        return False
    
    return parse_datetime_isoformat(application_deadline) >= get_datetime_local()

def normalize(ad: dict) -> Optional[JobAd]:
    if ad and ad.get("id"):
        return JobAd(
            id = ad.get("id") or "",
            title = clean_text(ad.get("headline") or ""),
            employer = clean_text((ad.get("employer") or {}).get("name") or ""),
            cities = [
                addr["municipality"]
                for addr in ad.get("workplace_addresses") or []
                if addr.get("municipality")
            ],
            application_deadline = ad.get("application_deadline"),
            publication_date = ad.get("publication_date"),
            description = clean_text((ad.get("description") or {}).get("text") or ""),
            url = ad.get("webpage_url") or ""
        )

    return None


def is_valid_ad(ad: dict) -> bool:
    deadline = ad.get("application_deadline")
    title = clean_text(ad.get("headline") or "")
    desc = clean_text((ad.get("description") or {}).get("text") or "")
    
    if not desc or not is_job_application_open(deadline):
        return False

    if not is_thesis_ad(title=title, desc=desc):
        print(f"Non thesis: {title}, url: {ad.get('webpage_url')}")
        return False

    return True


def fetch_jobs(queries: list[str], existing_job_ids: list[str]) -> list[JobAd]:
    all_ads: list[JobAd] = []
    new_job_ids: set[str] = set()

    for query in queries:
        hits = get_jobs(query)
        print(f"{query}: total {len(hits)} job ads")

        for ad in hits:
            ad_id = ad.get("id")
            if not ad_id or (ad_id in new_job_ids) or (ad_id in existing_job_ids):
                continue
            
            new_job_ids.add(ad_id)

            if is_valid_ad(ad):
                normalized_ad = normalize(ad)

                if normalized_ad:
                    all_ads.append(normalized_ad)

    print(f"{len(new_job_ids)} ads checked, {len(all_ads)} kept")

    return all_ads








