from langchain_openai import OpenAIEmbeddings

from app.core.config import get_settings

settings = get_settings()


class EmbeddingService:
    def __init__(self):
        self.client = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY,
        )

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate 1536-dimensional embeddings for a batch of text chunks."""
        if not texts:
            return []
        return await self.client.aembed_documents(texts)

    async def generate_query_embedding(self, query: str) -> list[float]:
        """Generate embedding for a single search query."""
        return await self.client.aembed_query(query)
