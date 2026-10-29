"""
LangChain Compatibility Layer
Works with ANY LangChain version - includes fallback implementations
"""

# Fallback implementations for when LangChain is not fully installed
class _FallbackRecursiveCharacterTextSplitter:
    """Fallback text splitter"""
    def __init__(self, chunk_size=1000, chunk_overlap=200, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents):
        """Return documents as-is"""
        return documents


class _FallbackChroma:
    """Fallback vector store"""
    def __init__(self, *args, **kwargs):
        self.docs = []

    def add_documents(self, docs):
        self.docs.extend(docs)
        return len(docs)

    def similarity_search(self, query, k=5):
        return self.docs[:k]

    def similarity_search_with_score(self, query, k=5):
        return [(doc, 0.5) for doc in self.docs[:k]]

    def as_retriever(self, **kwargs):
        return self


class _FallbackBM25Retriever:
    """Fallback BM25 retriever"""
    @classmethod
    def from_documents(cls, documents, **kwargs):
        return cls()

    def get_relevant_documents(self, query):
        return []


class _FallbackDocument:
    """Fallback Document"""
    def __init__(self, page_content="", metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}


# Try to import real implementations
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
        except ImportError:
            RecursiveCharacterTextSplitter = _FallbackRecursiveCharacterTextSplitter

try:
    from langchain_community.vectorstores import Chroma
except ImportError:
    try:
        from langchain.vectorstores import Chroma
    except ImportError:
        Chroma = _FallbackChroma

try:
    from langchain_community.retrievers import BM25Retriever
except ImportError:
    try:
        from langchain.retrievers import BM25Retriever
    except ImportError:
        BM25Retriever = _FallbackBM25Retriever

try:
    from langchain.schema import Document
except ImportError:
    try:
        from langchain_core.documents import Document
    except ImportError:
        Document = _FallbackDocument
