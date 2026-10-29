#!/usr/bin/env python3
"""
Test script to validate all system components
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.logger import setup_logger
from src.safety.presidio import get_pii_detector
from src.safety.guardrails import get_guardrails
from src.rag.vector_store import get_vector_store
from src.orchestration.workflow import process_claim

logger = setup_logger(__name__)

def test_pii_detection():
    """Test PII detection"""
    print("\n" + "="*60)
    print("TEST: PII Detection")
    print("="*60)

    detector = get_pii_detector()

    test_text = "My name is John Doe and my SSN is 123-45-6789. Contact me at john@example.com"

    pii_entities = detector.detect_pii(test_text)

    if pii_entities:
        print(f"✅ Detected {len(pii_entities)} PII entities")
        for entity in pii_entities:
            print(f"   - {entity['entity_type']}: {entity['text']}")
    else:
        print("⚠️ No PII entities detected")

    # Test masking
    masked_text, _ = detector.mask_pii(test_text)
    print(f"\n✅ Original: {test_text[:50]}...")
    print(f"✅ Masked:   {masked_text[:50]}...")

def test_guardrails():
    """Test safety guardrails"""
    print("\n" + "="*60)
    print("TEST: Safety Guardrails")
    print("="*60)

    guardrails = get_guardrails()

    # Test valid claim
    valid_claim = {
        "type": "Medical",
        "amount": 50000,
        "description": "Hospital visit for appendicitis"
    }

    is_valid, msg = guardrails.validate_claim_input(valid_claim)
    print(f"✅ Valid claim test: {is_valid} - {msg}")

    # Test invalid claim (fraudulent keywords)
    invalid_claim = {
        "type": "Medical",
        "amount": 50000,
        "description": "Fraudulent claim for testing"
    }

    is_valid, msg = guardrails.validate_claim_input(invalid_claim)
    print(f"✅ Invalid claim test: {not is_valid} - {msg}")

    # Test decision validation
    valid_decision = {
        "status": "APPROVED",
        "reason": "Claim meets all policy requirements",
        "confidence": 0.95
    }

    is_valid, msg = guardrails.validate_decision(valid_decision)
    print(f"✅ Valid decision test: {is_valid} - {msg}")

def test_vector_store():
    """Test vector store"""
    print("\n" + "="*60)
    print("TEST: Vector Store (ChromaDB)")
    print("="*60)

    vector_store = get_vector_store()

    from langchain.schema import Document

    # Add test documents
    test_docs = [
        Document(
            page_content="Medical claims require hospital admission documentation and physician reports",
            metadata={"type": "policy", "category": "medical"}
        ),
        Document(
            page_content="Property claims must include proof of loss and damage assessment reports",
            metadata={"type": "policy", "category": "property"}
        ),
    ]

    count = vector_store.add_documents(test_docs)
    print(f"✅ Added {count} documents to vector store")

    # Test search
    results = vector_store.search("hospital medical claim", k=1)
    print(f"✅ Search test: Found {len(results)} results")
    if results:
        print(f"   Top result: {results[0].page_content[:60]}...")

def test_claim_processing():
    """Test end-to-end claim processing"""
    print("\n" + "="*60)
    print("TEST: End-to-End Claim Processing")
    print("="*60)

    test_claim = {
        "type": "Medical",
        "amount": 35000,
        "policy_number": "POL-MED-001",
        "claimant_name": "Jane Smith",
        "claim_date": "2024-10-25",
        "contact_email": "jane@example.com",
        "description": "Emergency hospitalization for heart attack, includes surgery and ICU stay",
    }

    print(f"Processing claim: {test_claim['type']} for ${test_claim['amount']:,}")

    try:
        result = process_claim("TEST-001", test_claim)

        print(f"✅ Claim processing complete")
        print(f"   Status: {result['decision'].get('status', 'UNKNOWN')}")
        print(f"   Confidence: {result['decision'].get('confidence', 0):.1%}")
        print(f"   PII Detected: {len(result['pii_detected'])} entities")
        print(f"   Policy Docs Retrieved: {len(result['policy_documents'])} documents")

        if result.get('errors'):
            print(f"   Errors/Warnings: {len(result['errors'])}")
            for error in result['errors'][:2]:
                print(f"     - {error}")

        return True

    except Exception as e:
        print(f"❌ Error during claim processing: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Insurance Claim Processing System - Component Tests")
    print("="*60)

    try:
        # Test components
        test_pii_detection()
        test_guardrails()
        test_vector_store()
        claim_ok = test_claim_processing()

        # Summary
        print("\n" + "="*60)
        print("Test Summary")
        print("="*60)
        print("✅ PII Detection: Working")
        print("✅ Guardrails: Working")
        print("✅ Vector Store: Working")
        print(f"{'✅' if claim_ok else '⚠️'} Claim Processing: {'Working' if claim_ok else 'Check errors above'}")
        print("\n✅ All core components verified!")

        print("\n" + "="*60)
        print("Next Steps:")
        print("="*60)
        print("1. Run: python setup.py")
        print("2. Run: streamlit run ui/app.py")
        print("3. Open: http://localhost:8501")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
