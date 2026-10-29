#!/usr/bin/env python3
"""
Quick fix for test errors
"""

import subprocess
import sys
from pathlib import Path

def fix_missing_directories():
    """Create missing directories"""
    print("\n📁 Creating missing directories...")

    dirs = ["logs", "data/chroma_db", "data/uploads"]

    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {d}")


def install_missing_packages():
    """Install missing packages"""
    print("\n📦 Installing missing packages...")

    packages = [
        "langchain-community>=0.0.30",
        "langchain-text-splitters",
    ]

    for pkg in packages:
        print(f"\n   Installing: {pkg}")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                check=True,
                capture_output=True
            )
            print(f"   ✅ Installed: {pkg}")
        except Exception as e:
            print(f"   ❌ Failed: {str(e)[:100]}")
            return False

    return True


def verify_imports():
    """Verify key imports work"""
    print("\n🧪 Verifying imports...")

    imports = [
        ("LangChain", "import langchain"),
        ("LangChain Community", "import langchain_community"),
        ("ChromaDB", "import chromadb"),
        ("Compatibility Layer", "from langchain_compat import Document"),
    ]

    for name, stmt in imports:
        try:
            exec(stmt)
            print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name}: {str(e)[:50]}")
            return False

    return True


def main():
    print("\n" + "=" * 60)
    print("🔧 FIXING TEST ERRORS")
    print("=" * 60)

    print("\nIssues found:")
    print("   ❌ Missing 'logs' directory")
    print("   ❌ Missing 'langchain_community' module")
    print("   ❌ Missing 'langchain_text_splitters' module")

    # Step 1: Create directories
    print("\n📋 STEP 1: Creating directories...")
    fix_missing_directories()

    # Step 2: Install packages
    print("\n📋 STEP 2: Installing packages...")
    if not install_missing_packages():
        print("\n⚠️  Package installation failed")
        return False

    # Step 3: Verify imports
    print("\n📋 STEP 3: Verifying imports...")
    if not verify_imports():
        print("\n⚠️  Import verification failed")
        print("\nTry manually:")
        print("   pip install --upgrade langchain-community langchain-text-splitters")
        return False

    # Success
    print("\n" + "=" * 60)
    print("✅ ALL FIXES APPLIED!")
    print("=" * 60)

    print("\n🎯 Next steps:")
    print("   1. python run_tests.py")
    print("   2. streamlit run ui/app.py")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
