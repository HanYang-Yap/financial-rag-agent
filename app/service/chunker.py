from io import BytesIO

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.models.schemas import ChunkMetadata


class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def extract_chunks_from_pdf(
        self, file_bytes: bytes, filename: str
    ) -> tuple[int, list[ChunkMetadata]]:
        """
        Parses PDF bytes, keeps track of page numbers, and splits
        text into manageable chunks tagged with page metadata.
        """
        pdf_stream = BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)
        total_pages = len(reader.pages)
        chunks: list[ChunkMetadata] = []
        global_chunk_idx = 0

        for page_idx, page in enumerate(reader.pages):
            page_number = page_idx + 1
            text = page.extract_text() or ""
            text = text.strip()

            if not text:
                continue

            page_splits = self.splitter.split_text(text)
            for split_text in page_splits:
                chunks.append(
                    ChunkMetadata(
                        document_name=filename,
                        page_number=page_number,
                        chunk_index=global_chunk_idx,
                        content=split_text,
                    )
                )
                global_chunk_idx += 1

        return total_pages, chunks
