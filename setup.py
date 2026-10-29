#!/usr/bin/env python3
"""
Setup script for Insurance Claim Processing System
Initializes vector store with sample policies
"""

import json
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.rag.vector_store import get_vector_store
from src.llm.client import get_llm
from src.logger import setup_logger
from langchain.schema import Document

logger = setup_logger(__name__)

def load_sample_policies():
    """Load sample policies from JSON file"""
    policies_path = Path(__file__).parent / "data" / "sample_policies.json"

    with open(policies_path, 'r') as f:
        data = json.load(f)

    return data

def initialize_knowledge_base():
    """Initialize vector store with sample policies"""
    logger.info("Initializing knowledge base...")

    try:
        # Load policies
        data = load_sample_policies()

        # Get vector store
        vector_store = get_vector_store()

        # Add policies as documents
        documents = []

        for policy in data["policies"]:
            policy_text = f"""
            Policy ID: {policy['id']}
            Type: {policy['type']}
            Coverage: {policy['coverage']}
            Max Claim Amount: ${policy['max_claim_amount']:,}
            Deductible: ${policy['deductible']:,}

            Covered Services/Events:
            {json.dumps(policy.get('covered_services') or policy.get('covered_events') or policy.get('covered'), indent=2)}

            Exclusions:
            {json.dumps(policy.get('exclusions'), indent=2)}
            """

            documents.append(Document(
                page_content=policy_text,
                metadata={
                    "policy_id": policy["id"],
                    "type": policy["type"],
                    "source": "policy_database"
                }
            ))

        # Add guidelines
        guidelines_text = f"""
        Insurance Claims Processing Guidelines

        {json.dumps(data['processing_guidelines'], indent=2)}
        """

        documents.append(Document(
            page_content=guidelines_text,
            metadata={
                "type": "guidelines",
                "source": "processing_guidelines"
            }
        ))

        # Add to vector store
        num_docs = vector_store.add_documents(documents)
        logger.info(f"✅ Knowledge base initialized with {num_docs} documents")

        return True

    except Exception as e:
        logger.error(f"❌ Error initializing knowledge base: {str(e)}")
        return False

def verify_llm_connection():
    """Verify LLM connection works"""
    logger.info("Verifying LLM connection...")

    try:
        llm = get_llm()

        # Simple test
        response = llm.invoke("Say 'LLM connection successful'")
        logger.info(f"✅ LLM connection verified: {response.content[:50]}")
        return True

    except Exception as e:
        logger.warning(f"⚠️ LLM connection failed: {str(e)}")
        logger.warning("   You may need to configure Azure OpenAI or OpenAI API keys in .env")
        return False

def create_directories():
    """Create required directories"""
    directories = [
        "data/chroma_db",
        "data/uploads",
        "logs",
        "src/llm",
        "src/rag",
        "src/agents",
        "src/orchestration",
        "src/safety",
        "src/evaluation",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    logger.info("✅ Directories created")

def main():
    """Run setup"""
    print("\n" + "="*60)
    print("Insurance Claim Processing System - Setup")
    print("="*60 + "\n")

    # Create directories
    create_directories()

    # Initialize knowledge base
    kb_ready = initialize_knowledge_base()

    # Verify LLM
    llm_ready = verify_llm_connection()

    # Summary
    print("\n" + "="*60)
    print("Setup Summary")
    print("="*60)
    print(f"Knowledge Base: {'✅ Ready' if kb_ready else '⚠️ Check error above'}")
    print(f"LLM Connection: {'✅ Ready' if llm_ready else '⚠️ Configure API keys'}")
    print("\n" + "="*60)

    if not llm_ready:
        print("\n📝 Setup Notes:")
        print("1. Copy .env.example to .env")
        print("2. Add your Azure OpenAI or OpenAI API keys")
        print("3. Run: python setup.py")
        print("\n📖 Then start the app with:")
        print("   streamlit run ui/app.py")
    else:
        print("\n✅ Setup complete! Start the app with:")
        print("   streamlit run ui/app.py")

    print("\n")

if __name__ == "__main__":
    main()
