from langchain_openai import AzureChatOpenAI, ChatOpenAI
from config.settings import settings
from src.logger import setup_logger

logger = setup_logger(__name__)

def get_llm():
    """Initialize LLM client - Azure OpenAI or fallback to OpenAI"""

    if settings.azure_openai_api_key and settings.azure_openai_endpoint:
        logger.info("Initializing Azure OpenAI LLM")
        return AzureChatOpenAI(
            azure_deployment=settings.azure_openai_deployment_name,
            api_version=settings.azure_openai_api_version,
            temperature=0.7,
            max_tokens=2000,
        )
    elif settings.openai_api_key:
        logger.info("Initializing OpenAI LLM (fallback)")
        return ChatOpenAI(
            model=settings.openai_model,
            temperature=0.7,
            max_tokens=2000,
            api_key=settings.openai_api_key,
        )
    else:
        raise ValueError("No LLM API key configured. Set AZURE_OPENAI_API_KEY or OPENAI_API_KEY")

def get_embedding_model():
    """Initialize embedding model"""
    try:
        if settings.azure_openai_api_key and settings.azure_openai_endpoint:
            logger.info("Initializing Azure embeddings model")
            from langchain_openai import AzureOpenAIEmbeddings
            return AzureOpenAIEmbeddings(
                azure_deployment=settings.azure_openai_embedding_deployment,
                api_version=settings.azure_openai_api_version,
            )
    except Exception as e:
        logger.warning(f"Azure embeddings failed: {e}, using sentence-transformers")

    logger.info("Using sentence-transformers for embeddings")
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
