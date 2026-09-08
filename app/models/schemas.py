import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


# SQLAlchemy ORM Model for pgvector table
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    # text-embedding-3-small uses 1536 dimensions
    embedding = mapped_column(Vector(1536), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


# Pydantic Schemas for API requests & responses
class ChunkMetadata(BaseModel):
    document_name: str
    page_number: int
    chunk_index: int
    content: str


class IngestionResponse(BaseModel):
    document_name: str
    total_pages: int
    total_chunks: int
    status: str = Field(default="indexed")
