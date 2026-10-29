"""
LangChain Compatibility Layer
Handles different import paths across LangChain versions
"""

def get_recursive_text_splitter():
    """Get RecursiveCharacterTextSplitter with fallback for different versions"""
    try:
        # Try newer structure first
        from langchain.text_splitters import RecursiveCharacterTextSplitter
        return RecursiveCharacterTextSplitter
    except ImportError:
        try:
            # Try old structure
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            return RecursiveCharacterTextSplitter
        except ImportError:
            # Try langchain-community
            try:
                from langchain_community.text_splitters import RecursiveCharacterTextSplitter
                return RecursiveCharacterTextSplitter
            except ImportError:
                raise ImportError(
                    "Could not import RecursiveCharacterTextSplitter from any location. "
                    "Please ensure langchain is installed: pip install --upgrade langchain"
                )


def get_chroma():
    """Get Chroma with fallback for different versions"""
    try:
        # Try community first (newer structure)
        from langchain_community.vectorstores import Chroma
        return Chroma
    except ImportError:
        try:
            # Try old structure
            from langchain.vectorstores import Chroma
            return Chroma
        except ImportError:
            raise ImportError(
                "Could not import Chroma from any location. "
                "Please ensure langchain-community is installed: pip install --upgrade langchain-community"
            )


def get_bm25_retriever():
    """Get BM25Retriever with fallback for different versions"""
    try:
        # Try community first (newer structure)
        from langchain_community.retrievers import BM25Retriever
        return BM25Retriever
    except ImportError:
        try:
            # Try old structure
            from langchain.retrievers import BM25Retriever
            return BM25Retriever
        except ImportError:
            raise ImportError(
                "Could not import BM25Retriever from any location. "
                "Please ensure langchain-community is installed: pip install --upgrade langchain-community"
            )


def get_document():
    """Get Document schema"""
    try:
        from langchain.schema import Document
        return Document
    except ImportError:
        try:
            from langchain_core.documents import Document
            return Document
        except ImportError:
            raise ImportError("Could not import Document from any location")


# Export convenience variables
RecursiveCharacterTextSplitter = get_recursive_text_splitter()
Chroma = get_chroma()
BM25Retriever = get_bm25_retriever()
Document = get_document()
