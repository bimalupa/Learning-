#!/usr/bin/env python3
"""
Fix: Workflow state structure mismatch
The workflow expects claim_data dict but tests provide individual fields
"""

import sys
import json

print("\n" + "=" * 70)
print("🔧 FIXING WORKFLOW STATE MISMATCH")
print("=" * 70)

print("\n📋 Issue:")
print("   ❌ Workflow expects: state['claim_data'] = {...}")
print("   ❌ Tests provide: state['claim_text'] = 'Medical claim...'")

print("\n🔍 Solution:")
print("   ✅ Convert test input to workflow format")

print("\n📝 Test code fix:")
print("""
Before:
    claim_state = {
        "claim_id": "TEST-001",
        "claim_text": "Medical claim for $500",
        "documents": [],
        ...
    }

After:
    claim_state = {
        "claim_id": "TEST-001",
        "claim_data": {
            "claim_text": "Medical claim for $500",
            "documents": []
        },
        "masked_claim": None,
        "pii_detected": [],
        "intake_valid": False,
        "policy_documents": [],
        "validation_result": {},
        "decision": {},
        "errors": [],
        "messages": []
    }
""")

print("\n" + "=" * 70)
print("✅ SOLUTION PROVIDED")
print("=" * 70)

print("\n💡 Next steps:")
print("   1. Update test state structure (as shown above)")
print("   2. OR update workflow to accept 'claim_text' field")
print("   3. Run tests again")

print()
