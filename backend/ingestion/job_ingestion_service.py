import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from helpers.constants import (
    JOB_FIELDS,
    EMPLOYMENT_TYPES
)
from models.job import Job
from dto.job_ad import JobAd
from helpers.utils import list_to_str, parse_datetime_isoformat
from ingestion.job_search_service import build_search_queries, fetch_jobs
from common.app_container import container

def embedding_text(ad: JobAd) -> str:
    return (
        f"{ad.title}\n"
        f"Company: {ad.employer}\n"
        f"Location: {list_to_str(ad.cities, "; ")}\n\n"
        f"{ad.description}"
    )


def get_existing_ids() -> list[str]:
    return container.job_repository.get_existing_job_ids()


def to_job(job_ad: JobAd) -> Job:
    return Job(
        id=job_ad.id,
        title=job_ad.title,
        company=job_ad.employer,
        url=job_ad.url,
        posted_at=parse_datetime_isoformat(job_ad.publication_date),
        application_deadline_at=parse_datetime_isoformat(job_ad.application_deadline),
        locations=list_to_str(job_ad.cities, "; "),
        description=job_ad.description,
        is_deleted=False,
        embedding_text=embedding_text(job_ad)
    )


def execute_job_ingestion():
    queries = build_search_queries(JOB_FIELDS, EMPLOYMENT_TYPES)
    existing_job_ids = get_existing_ids()

    job_ads: list[JobAd] = fetch_jobs(queries=queries, existing_job_ids=existing_job_ids)
    print(f"Found {len(job_ads)} jobs")

    if len(job_ads) > 0:
        jobs: list[Job] = [to_job(job_ad) for job_ad in job_ads]
        job_ids = container.job_repository.save_jobs(jobs=jobs)

        print(f"Saved: {len(job_ids)} new jobs, job_ids: {', '.join(job_ids)}")