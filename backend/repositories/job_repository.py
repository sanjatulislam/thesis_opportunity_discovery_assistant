import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from repositories.vector_repository import VectorRepository
from dto.vector_record import VectorRecord

from langchain_postgres.v2.engine import Column

from models.job import Job
from helpers.constants import (
    JOBS_TABLE,
    JOBS_TABLE_ID,
    JOBS_TABLE_URL,
    JOBS_TABLE_POSTED_AT,
    JOBS_TABLE_APPLICATION_DEADLINE_AT,
    JOBS_TABLE_TITLE,
    JOBS_TABLE_COMPANY,
    JOBS_TABLE_LOCATIONS,
    JOBS_TABLE_DESCRIPTION,
    JOBS_TABLE_EMBEDDING_TEXT,
    JOBS_TABLE_IS_DELETED
)

class JobRepository(VectorRepository):
    table_name = JOBS_TABLE
    id_column_name = JOBS_TABLE_ID
    id_column_def = Column(JOBS_TABLE_ID, "TEXT")
    content_column = JOBS_TABLE_EMBEDDING_TEXT

    metadata_columns = [
        Column(name=JOBS_TABLE_URL, data_type="TEXT"),
        Column(name=JOBS_TABLE_TITLE, data_type="TEXT"),
        Column(name=JOBS_TABLE_COMPANY, data_type="TEXT"),
        Column(name=JOBS_TABLE_LOCATIONS, data_type="TEXT"),
        Column(name=JOBS_TABLE_POSTED_AT, data_type="TIMESTAMPTZ"),
        Column(name=JOBS_TABLE_APPLICATION_DEADLINE_AT, data_type="TIMESTAMPTZ"),
        Column(name=JOBS_TABLE_DESCRIPTION, data_type="TEXT"),
        Column(name=JOBS_TABLE_IS_DELETED, data_type="BOOLEAN"),
    ]


    def get_existing_job_ids(self) -> list[str]:
        query = f"""SELECT {self.id_column_name} 
                    FROM {self.table_name}"""
        
        rows = self.db.fetch_all(query,)
        
        existing_ids = [row[self.id_column_name] for row in rows]

        return list(existing_ids)


    def save_jobs(self, jobs: list[Job]) -> list[str]:
        batch_items: list[VectorRecord] = []
        
        for job in jobs:
            vec_rec = VectorRecord(
                 id=job.id,
                 content=job.embedding_text,
                 metadata={
                    JOBS_TABLE_URL: job.url,
                    JOBS_TABLE_POSTED_AT: job.posted_at,
                    JOBS_TABLE_APPLICATION_DEADLINE_AT: job.application_deadline_at,
                    JOBS_TABLE_TITLE: job.title,
                    JOBS_TABLE_COMPANY: job.company,
                    JOBS_TABLE_LOCATIONS: job.locations,
                    JOBS_TABLE_DESCRIPTION: job.description,
                    JOBS_TABLE_IS_DELETED: job.is_deleted,
                }
            )
              
            batch_items.append(vec_rec)

        return self.save_all(batch_items)