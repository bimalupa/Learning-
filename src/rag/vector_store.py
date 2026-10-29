import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain.text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings
from src.logger import setup_logger
from src.llm.client import get_embedding_model
import os

logger = setup_logger(__name__)

class VectorStore:
    def __init__(self):
        self.embeddings = get_embedding_model()
        os.makedirs(settings.chroma_db_path, exist_ok=True)

        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=settings.chroma_db_path,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

        self.vector_store = Chroma(
            client=self.client,
            collection_name=settings.chroma_collection_name,
            embedding_function=self.embeddings,
        )

        logger.info(f"Vector store initialized at {settings.chroma_db_path}")

    def add_documents(self, documents: list, metadata: dict = None):
        """Add documents to vector store"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

        split_docs = text_splitter.split_documents(documents)
        logger.info(f"Adding {len(split_docs)} document chunks to vector store")

        self.vector_store.add_documents(split_docs)
        return len(split_docs)

    def search(self, query: str, k: int = 5):
        """Search vector store by semantic similarity"""
        logger.info(f"Searching vector store with query: {query[:100]}")
        results = self.vector_store.similarity_search(query, k=k)
        return results

    def search_with_scores(self, query: str, k: int = 5):
        """Search with similarity scores"""
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results

    def get_retriever(self, k: int = 5):
        """Get a retriever interface"""
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    def reset(self):
        """Clear all documents from vector store"""
        logger.warning("Resetting vector store")
        self.client.delete_collection(name=settings.chroma_collection_name)
        self.vector_store = Chroma(
            client=self.client,
            collection_name=settings.chroma_collection_name,
            embedding_function=self.embeddings,
        )

# Singleton instance
_vector_store = None

def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
