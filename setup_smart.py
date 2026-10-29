#!/usr/bin/env python
"""
Smart Setup Script
Installs dependencies only if needed, preventing unnecessary re-runs
"""

import os
import sys
import subprocess
from pathlib import Path
from verify_requirements import RequirementsVerifier


def check_python_version():
    """Verify Python version is 3.9+"""
    if sys.version_info < (3, 9):
        print(f"❌ Python 3.9+ required, but you have {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def setup_environment():
    """Setup environment variables"""
    env_example = Path(".env.example")
    env_file = Path(".env")

    if not env_file.exists() and env_example.exists():
        print("\n📝 Creating .env from .env.example...")
        with open(env_example, 'r') as f:
            env_content = f.read()
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env created (update with your API keys)")
    elif env_file.exists():
        print("✅ .env already exists")
    else:
        print("⚠️  No .env or .env.example found")


def install_requirements():
    """Install requirements using smart verification"""
    print("\n" + "=" * 50)
    print("📦 INSTALLING DEPENDENCIES")
    print("=" * 50)

    verifier = RequirementsVerifier("requirements.txt")

    # Check if all requirements are satisfied
    if verifier.verify_requirements():
        print("\n✅ All dependencies already installed!")
        return True
    else:
        print("\n🔧 Installing missing dependencies...")
        return verifier.install_missing()


def setup_database():
    """Setup ChromaDB and load sample data"""
    print("\n" + "=" * 50)
    print("📚 SETTING UP DATABASE")
    print("=" * 50)

    try:
        from src.rag.vector_store import VectorStore
        from pathlib import Path
        import json

        print("🔍 Initializing vector store...")
        vs = VectorStore()

        # Load sample policies
        policies_file = Path("data/sample_policies.json")
        if policies_file.exists():
            print("📄 Loading sample policies...")
            with open(policies_file, 'r') as f:
                policies = json.load(f)

            for policy in policies:
                vs.add_document(
                    doc_id=policy.get('id', 'unknown'),
                    content=str(policy),
                    metadata={"type": "policy"}
                )

            print(f"✅ Loaded {len(policies)} sample policies")
        else:
            print("⚠️  No sample policies found at data/sample_policies.json")

        return True
    except Exception as e:
        print(f"⚠️  Could not setup database: {e}")
        print("   (This is optional - the system will work without pre-loaded data)")
        return True


def verify_installation():
    """Verify all components are working"""
    print("\n" + "=" * 50)
    print("✅ VERIFICATION")
    print("=" * 50)

    checks = []

    # Check key imports
    try:
        import streamlit
        checks.append(("Streamlit", True))
    except ImportError:
        checks.append(("Streamlit", False))

    try:
        import langchain
        checks.append(("LangChain", True))
    except ImportError:
        checks.append(("LangChain", False))

    try:
        import chromadb
        checks.append(("ChromaDB", True))
    except ImportError:
        checks.append(("ChromaDB", False))

    try:
        from presidio_analyzer import AnalyzerEngine
        checks.append(("Presidio", True))
    except ImportError:
        checks.append(("Presidio", False))

    try:
        from sentence_transformers import SentenceTransformer
        checks.append(("Sentence Transformers", True))
    except ImportError:
        checks.append(("Sentence Transformers", False))

    print("\n📋 Component Status:")
    print("-" * 50)
    all_passed = True
    for component, status in checks:
        symbol = "✅" if status else "❌"
        print(f"{symbol} {component}")
        if not status:
            all_passed = False

    print("-" * 50)

    if all_passed:
        print("\n✅ All components verified successfully!")
        return True
    else:
        print("\n⚠️  Some components failed verification")
        return False


def main():
    print("\n" + "=" * 50)
    print("🚀 SMART SETUP - Insurance Claim Processing System")
    print("=" * 50)

    # Step 1: Check Python version
    print("\n📌 Step 1: Checking Python version...")
    if not check_python_version():
        return False

    # Step 2: Setup environment
    print("\n📌 Step 2: Setting up environment...")
    setup_environment()

    # Step 3: Install requirements (smart - only missing packages)
    print("\n📌 Step 3: Installing dependencies...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        return False

    # Step 4: Setup database
    print("\n📌 Step 4: Setting up database...")
    setup_database()

    # Step 5: Verify installation
    print("\n📌 Step 5: Verifying installation...")
    if not verify_installation():
        print("\n⚠️  Some components failed. Please check the errors above.")
        return False

    # Success!
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\n📚 Next steps:")
    print("   1. Configure .env with your API keys (if needed)")
    print("   2. Run: streamlit run ui/app.py")
    print("   3. Open: http://localhost:8501")
    print("\n" + "=" * 50)

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
