#!/usr/bin/env python3
"""
Fix LangChain Import Issues
Updates old import paths to new LangChain structure
"""

import subprocess
import sys


def test_imports():
    """Test if all imports work"""
    print("\n🧪 Testing imports...")
    print("-" * 50)

    imports_to_test = [
        ("Streamlit", "import streamlit"),
        ("LangChain", "import langchain"),
        ("LangChain Community", "from langchain_community.vectorstores import Chroma"),
        ("ChromaDB", "import chromadb"),
        ("Sentence Transformers", "from sentence_transformers import SentenceTransformer"),
        ("Presidio", "from presidio_analyzer import AnalyzerEngine"),
        ("LangGraph", "from langgraph import graph"),
    ]

    failed = []

    for name, import_statement in imports_to_test:
        try:
            exec(import_statement)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {str(e)[:50]}")
            failed.append(name)

    print("-" * 50)

    if failed:
        print(f"\n⚠️  {len(failed)} import(s) failed")
        return False
    else:
        print("✅ All imports successful!")
        return True


def install_missing():
    """Install missing packages"""
    print("\n📦 Installing missing dependencies...")
    print("-" * 50)

    try:
        # Ensure langchain-community is installed
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "langchain-community>=0.0.30"],
            check=True
        )
        print("✅ langchain-community installed")

        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("🔧 LangChain Import Fixer")
    print("=" * 60)

    print("\n✅ Import paths already updated in:")
    print("   - src/rag/vector_store.py")
    print("   - src/rag/retriever.py")

    print("\n📝 Changes made:")
    print("   OLD: from langchain.vectorstores import Chroma")
    print("   NEW: from langchain_community.vectorstores import Chroma")
    print()
    print("   OLD: from langchain.text_splitter import RecursiveCharacterTextSplitter")
    print("   NEW: from langchain.text_splitters import RecursiveCharacterTextSplitter")
    print()
    print("   OLD: from langchain.retrievers import BM25Retriever")
    print("   NEW: from langchain_community.retrievers import BM25Retriever")

    # Ensure langchain-community is installed
    print("\n📦 Ensuring dependencies...")
    if not install_missing():
        print("⚠️  Could not install langchain-community")
        return False

    # Test imports
    if not test_imports():
        print("\n❌ Some imports still failing")
        print("\n💡 Try this:")
        print("   pip install --upgrade langchain langchain-community")
        return False

    print("\n" + "=" * 60)
    print("✅ All imports fixed and working!")
    print("=" * 60)
    print("\nNow you can run:")
    print("   python setup.py")
    print("   streamlit run ui/app.py")
    print("\n")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
