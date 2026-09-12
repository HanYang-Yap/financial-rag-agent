from sqlalchemy import text

from app.db.session import Base, engine


async def init_vector_db():
    """Enable pgvector extension and create all tables."""
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await conn.run_sync(Base.metadata.create_all)
