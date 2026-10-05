import os
import sys
from dotenv import load_dotenv
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from repositories.database import Database
from common.embedding_model import EmbeddingService
from repositories.job_repository import JobRepository


load_dotenv()

class AppContainer:
    def __init__(self):
        connection_str = os.getenv('DB_CONNECTION_STR')

        if not connection_str:
            raise RuntimeError("DB_CONNECTION_STR is not configured")

        self.db = Database(connection_str)
        self.embedding_service = EmbeddingService()

        self.job_repository = JobRepository(db=self.db, embedding_service=self.embedding_service)
        self.job_repository.setup()

    def close(self):
        self.db.close()



container = AppContainer()