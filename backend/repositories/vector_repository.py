import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from helpers.constants import (
    EMBEDDING_DIMENSION,  
    AUDIT_COLUMN_CREATED_AT, 
    AUDIT_COLUMN_UPDATED_AT)
from helpers.utils import get_datetime_local
from repositories.database import Database
from common.embedding_model import EmbeddingService
from dto.vector_record import VectorRecord

from langchain_postgres import PGVectorStore
from langchain_postgres.v2.engine import Column


class VectorRepository():
    table_name: str
    id_column_name: str
    id_column_def: Column
    content_column: str
    metadata_columns: list[Column]


    def __init__(self, db: Database, embedding_service: EmbeddingService):
        self.db = db
        self.embedding_service = embedding_service
        self.engine = db.engine
        self._store: PGVectorStore | None = None


    @property
    def all_metadata_columns(self) -> list[Column]:
        return [
            *self.metadata_columns,
            Column(AUDIT_COLUMN_CREATED_AT, "TIMESTAMP"),
            Column(AUDIT_COLUMN_UPDATED_AT, "TIMESTAMP", nullable=True),
        ]


    @property
    def store(self) -> PGVectorStore:
        if self._store is None:
            self._store = PGVectorStore.create_sync(
                engine=self.engine,
                table_name=self.table_name,
                embedding_service=self.embedding_service.model,
                id_column=self.id_column_name,
                content_column=self.content_column,
                embedding_column="embedding",
                metadata_columns=[
                    c.name for c in self.all_metadata_columns
                ],
            )
        return self._store


    def setup(self, overwrite_existing: bool = False):
        self.db.execute(
            "CREATE EXTENSION IF NOT EXISTS vector;"
        )

        if self.table_exists() and not overwrite_existing:
            print(f"Table '{self.table_name}' already exists - skipping creation.")
            return

        self.engine.init_vectorstore_table(
            table_name=self.table_name,
            vector_size=EMBEDDING_DIMENSION,
            id_column=self.id_column_def,
            content_column=self.content_column,
            embedding_column="embedding",
            metadata_columns=self.all_metadata_columns,
            overwrite_existing=overwrite_existing,
        )
        print(f"Table '{self.table_name}' ready.")


    def table_exists(self) -> bool:
            row = self.db.fetch_one(
                "SELECT to_regclass(%s) AS table_name;", 
                (self.table_name,)
            )
            return row is not None and row["table_name"] is not None

    def save_all(self, items: list[VectorRecord]) -> list[str]:
        if not items:
            return []

        batch_metadatas = []

        ids = [item.id for item in items]
        contents = [item.content for item in items]

        for item in items:
            audit = {
                AUDIT_COLUMN_CREATED_AT: get_datetime_local(), 
                AUDIT_COLUMN_UPDATED_AT: None
            }
            
            batch_metadatas.append({**item.metadata, **audit})

        return self.store.add_texts(
            texts=contents,
            metadatas=batch_metadatas,
            ids=ids
        )
