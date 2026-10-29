from typing import List
from langchain.schema import Document
from langchain.retrievers import BM25Retriever
from src.rag.vector_store import get_vector_store
from src.logger import setup_logger
from src.rag.reranker import CrossEncoderReranker

logger = setup_logger(__name__)

class HybridRetriever:
    def __init__(self, alpha: float = 0.5, k: int = 5, rerank_k: int = 3):
        """
        Hybrid retriever combining semantic and BM25 search
        alpha: weight for semantic search (0.0-1.0), rest goes to BM25
        """
        self.vector_store = get_vector_store()
        self.alpha = alpha
        self.k = k
        self.rerank_k = rerank_k
        self.reranker = CrossEncoderReranker()
        self.bm25_retriever = None

    def set_bm25_documents(self, documents: List[Document]):
        """Initialize BM25 retriever with documents"""
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        logger.info(f"BM25 retriever initialized with {len(documents)} documents")

    def retrieve(self, query: str) -> List[Document]:
        """Hybrid search: semantic + BM25 with reranking"""
        if not self.bm25_retriever:
            logger.warning("BM25 retriever not initialized, using semantic only")
            semantic_results = self.vector_store.search(query, k=self.k)
            return semantic_results

        # Semantic search
        semantic_results = self.vector_store.search_with_scores(query, k=self.k)

        # BM25 search
        bm25_results = self.bm25_retriever.get_relevant_documents(query)[:self.k]

        # Normalize and combine
        combined = self._combine_results(semantic_results, bm25_results)

        # Rerank using cross-encoder
        reranked = self.reranker.rerank(query, combined, k=self.rerank_k)

        logger.info(f"Retrieved {len(reranked)} documents after reranking")
        return reranked

    def _combine_results(self, semantic_results, bm25_results):
        """Combine semantic and BM25 results"""
        seen = set()
        combined = []

        # Add semantic results with weights
        for doc, score in semantic_results:
            doc_id = doc.page_content[:50]
            if doc_id not in seen:
                doc.metadata['semantic_score'] = score
                combined.append(doc)
                seen.add(doc_id)

        # Add BM25 results that aren't already in semantic
        for doc in bm25_results:
            doc_id = doc.page_content[:50]
            if doc_id not in seen:
                combined.append(doc)
                seen.add(doc_id)

        return combined

def get_hybrid_retriever(alpha: float = 0.5) -> HybridRetriever:
    """Factory function for hybrid retriever"""
    return HybridRetriever(alpha=alpha)
