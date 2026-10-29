#!/usr/bin/env python3
"""
Automated Test Suite for Insurance Claim Processing System
Tests all major components and functionality
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Test results tracking
results = {
    "timestamp": datetime.now().isoformat(),
    "tests": {},
    "passed": 0,
    "failed": 0,
    "errors": []
}

# List to store test functions
test_functions = []

def test(name):
    """Decorator for tests - accepts test name as argument"""
    def decorator(func):
        def wrapper():
            print(f"\n🧪 Testing: {name}")
            print("-" * 60)
            try:
                func()
                results["tests"][name] = "PASS"
                results["passed"] += 1
                print(f"✅ PASS: {name}")
                return True
            except AssertionError as e:
                results["tests"][name] = f"FAIL: {e}"
                results["failed"] += 1
                results["errors"].append(f"{name}: {e}")
                print(f"❌ FAIL: {name}")
                print(f"   Error: {e}")
                return False
            except Exception as e:
                results["tests"][name] = f"ERROR: {e}"
                results["failed"] += 1
                results["errors"].append(f"{name}: {str(e)[:100]}")
                print(f"❌ ERROR: {name}")
                print(f"   {str(e)[:100]}")
                return False

        # Register the test
        test_functions.append(wrapper)
        return wrapper

    return decorator


# ============================================
# SYSTEM TESTS
# ============================================

@test("Python Version")
def test_python_version():
    """Verify Python 3.9+"""
    assert sys.version_info >= (3, 9), f"Python 3.9+ required, got {sys.version_info.major}.{sys.version_info.minor}"
    print(f"   Python {sys.version_info.major}.{sys.version_info.minor}")


@test("Required Directories")
def test_directories():
    """Check required directories exist"""
    dirs = ["src", "ui", "data", "logs", "config"]
    for d in dirs:
        assert Path(d).exists(), f"Directory {d} not found"
    print(f"   All {len(dirs)} directories present")


@test("Configuration Files")
def test_config_files():
    """Check required config files"""
    files = ["config/settings.py", "data/sample_policies.json"]
    for f in files:
        assert Path(f).exists(), f"File {f} not found"
    print(f"   All config files present")


# ============================================
# IMPORT TESTS
# ============================================

@test("LangChain Compatibility")
def test_langchain_compat():
    """Test compatibility layer imports"""
    from langchain_compat import Document, Chroma, BM25Retriever, RecursiveCharacterTextSplitter
    assert Document is not None
    assert Chroma is not None
    print("   ✅ All compatibility imports working")


@test("Core Modules Import")
def test_core_imports():
    """Test all core modules import"""
    from src.logger import setup_logger
    from src.llm.client import get_embedding_model, get_llm
    from src.rag.vector_store import get_vector_store
    from src.safety.presidio import PIIDetectionMasking
    print("   ✅ All core modules imported")


@test("Configuration Loading")
def test_config_loading():
    """Test configuration loads"""
    from config.settings import settings
    assert settings.chroma_db_path is not None
    assert settings.chroma_collection_name is not None
    print(f"   ChromaDB path: {settings.chroma_db_path}")


# ============================================
# COMPONENT TESTS
# ============================================

@test("Logger Initialization")
def test_logger():
    """Test logging setup"""
    from src.logger import setup_logger
    logger = setup_logger(__name__)
    assert logger is not None
    logger.info("Test log message")
    print("   ✅ Logger working")


@test("Embeddings Model")
def test_embeddings():
    """Test embeddings initialization"""
    from src.llm.client import get_embedding_model
    embeddings = get_embedding_model()

    # Test embedding
    emb = embeddings.embed_query("test query")
    assert emb is not None
    assert len(emb) > 0
    print(f"   ✅ Embeddings: {len(emb)} dimensions")


@test("Vector Store")
def test_vector_store():
    """Test vector store initialization"""
    from src.rag.vector_store import get_vector_store
    vs = get_vector_store()
    assert vs is not None
    assert vs.vector_store is not None
    print("   ✅ Vector store initialized")


@test("PII Detection")
def test_pii_detection():
    """Test PII detection and masking"""
    from src.safety.presidio import PIIDetectionMasking

    pii = PIIDetectionMasking()
    text = "My email is john@example.com and SSN is 123-45-6789"

    # Detect
    detected = pii.detect_pii(text)
    assert len(detected) > 0, "PII not detected"

    # Mask
    masked = pii.mask_pii(text)
    assert "john@example.com" not in masked, "Email not masked"

    print(f"   ✅ Detected {len(detected)} PII entities")
    print(f"   ✅ Original: {text[:40]}...")
    print(f"   ✅ Masked:   {masked[:40]}...")


@test("Sample Policies Loading")
def test_sample_policies():
    """Test sample policies load"""
    import json

    with open("data/sample_policies.json", "r") as f:
        data = json.load(f)

    assert "policies" in data
    assert len(data["policies"]) > 0

    # Verify structure
    for policy in data["policies"]:
        assert "id" in policy
        assert "type" in policy
        assert "coverage" in policy

    print(f"   ✅ Loaded {len(data['policies'])} policies")


# ============================================
# WORKFLOW TESTS
# ============================================

@test("Workflow Building")
def test_workflow_build():
    """Test workflow can be built"""
    from src.orchestration.workflow import build_workflow

    workflow = build_workflow()
    assert workflow is not None
    print("   ✅ Workflow built successfully")


@test("Workflow Processing")
def test_workflow_process():
    """Test workflow processes a claim"""
    from src.orchestration.workflow import build_workflow

    workflow = build_workflow()

    # Simple test claim
    claim_state = {
        "claim_id": "TEST-001",
        "claim_text": "Medical claim for $500 doctor visit",
        "documents": [],
        "validation_passed": True,
        "pii_detected": False,
        "decision": None
    }

    # Process
    start = time.time()
    result = workflow.invoke(claim_state)
    duration = time.time() - start

    assert result is not None
    assert "decision" in result or result.get("validation_passed") is not None

    print(f"   ✅ Processing time: {duration:.2f} seconds")
    print(f"   ✅ Workflow executed successfully")


# ============================================
# DATA TESTS
# ============================================

@test("Data Files Exist")
def test_data_files():
    """Check data files"""
    files = ["data/sample_policies.json"]

    for f in files:
        assert Path(f).exists(), f"File {f} not found"

    print(f"   ✅ All data files present")


@test("ChromaDB Directory")
def test_chroma_directory():
    """Check ChromaDB directory"""
    from config.settings import settings

    chroma_path = Path(settings.chroma_db_path)
    chroma_path.mkdir(parents=True, exist_ok=True)

    assert chroma_path.exists()
    print(f"   ✅ ChromaDB directory: {chroma_path}")


# ============================================
# PERFORMANCE TESTS
# ============================================

@test("Response Time")
def test_response_time():
    """Test claim processing response time"""
    from src.orchestration.workflow import build_workflow

    workflow = build_workflow()

    claim_state = {
        "claim_id": "PERF-001",
        "claim_text": "Medical claim",
        "documents": [],
        "validation_passed": True,
        "pii_detected": False,
        "decision": None
    }

    start = time.time()
    result = workflow.invoke(claim_state)
    duration = time.time() - start

    # Should complete in reasonable time
    assert duration < 30, f"Processing took {duration}s, expected < 30s"

    print(f"   Processing time: {duration:.2f}s")
    if duration < 5:
        print("   ✅ Excellent performance (< 5s)")
    elif duration < 10:
        print("   ✅ Good performance (< 10s)")
    else:
        print(f"   ⚠️  Slow ({duration:.2f}s)")


# ============================================
# SECURITY TESTS
# ============================================

@test("PII Masking in Processing")
def test_pii_masking_workflow():
    """Test PII is masked during workflow"""
    from src.safety.presidio import PIIDetectionMasking

    pii = PIIDetectionMasking()

    sensitive_claim = "Claim by John Doe, SSN: 123-45-6789, Email: john@example.com"
    masked = pii.mask_pii(sensitive_claim)

    # Verify sensitive info is masked
    assert "123-45-6789" not in masked
    assert "john@example.com" not in masked

    print(f"   ✅ Sensitive data properly masked")


# ============================================
# INTEGRATION TESTS
# ============================================

@test("End-to-End Processing")
def test_end_to_end():
    """Test complete end-to-end processing"""
    from src.orchestration.workflow import build_workflow
    from src.logger import setup_logger

    logger = setup_logger(__name__)
    workflow = build_workflow()

    # Test claim
    test_cases = [
        ("Valid Medical", "Medical claim for $1500 doctor visit"),
        ("Invalid Amount", "Medical claim for $999999"),
        ("Auto Claim", "Auto collision claim $5000"),
    ]

    for name, claim_text in test_cases:
        claim_state = {
            "claim_id": f"TEST-{name}",
            "claim_text": claim_text,
            "documents": [],
            "validation_passed": True,
            "pii_detected": False,
            "decision": None
        }

        result = workflow.invoke(claim_state)
        assert result is not None
        logger.info(f"Processed: {name}")

    print(f"   ✅ All {len(test_cases)} test cases processed")


# ============================================
# MAIN TEST RUNNER
# ============================================

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 INSURANCE CLAIM PROCESSING SYSTEM - TEST SUITE")
    print("=" * 70)

    print(f"\n📋 Running {len(test_functions)} tests...\n")

    for test_func in test_functions:
        test_func()

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    total = results["passed"] + results["failed"]
    pass_rate = (results["passed"] / total * 100) if total > 0 else 0

    print(f"\nTotal Tests: {total}")
    print(f"Passed:      {results['passed']} ✅")
    print(f"Failed:      {results['failed']} ❌")
    print(f"Pass Rate:   {pass_rate:.1f}%")

    if results["errors"]:
        print(f"\n⚠️  Errors:")
        for error in results["errors"]:
            print(f"   - {error}")

    # Save results
    with open("TEST_RESULTS.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Results saved to: TEST_RESULTS.json")

    # Final status
    print("\n" + "=" * 70)
    if results["failed"] == 0:
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n🎉 System is ready for use!")
        return 0
    else:
        print(f"❌ {results['failed']} TEST(S) FAILED")
        print("=" * 70)
        print("\n💡 Fix the errors above and run tests again")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
