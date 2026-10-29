from typing import List
from langchain.schema import Document
from sentence_transformers import CrossEncoder
from src.logger import setup_logger

logger = setup_logger(__name__)

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/qnli-distilroberta-base"):
        """Initialize cross-encoder for reranking"""
        logger.info(f"Loading cross-encoder model: {model_name}")
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: List[Document], k: int = 3) -> List[Document]:
        """Rerank documents using cross-encoder"""
        if not documents:
            return []

        # Prepare document texts
        doc_texts = [doc.page_content for doc in documents]

        # Score pairs
        scores = self.model.predict([(query, doc_text) for doc_text in doc_texts])

        # Sort by score
        doc_score_pairs = list(zip(documents, scores))
        doc_score_pairs.sort(key=lambda x: x[1], reverse=True)

        # Return top k
        reranked = [doc for doc, _ in doc_score_pairs[:k]]
        logger.info(f"Reranked to top {len(reranked)} documents")

        return reranked
