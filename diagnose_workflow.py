#!/usr/bin/env python3
"""
Diagnose workflow issues
Check what the workflow actually returns
"""

import sys
import json
from pprint import pprint

print("\n" + "=" * 70)
print("🔍 DIAGNOSING WORKFLOW ISSUES")
print("=" * 70)

try:
    print("\n📋 Step 1: Testing imports...")
    from src.orchestration.workflow import build_workflow
    print("✅ Workflow imported")

    print("\n📋 Step 2: Building workflow...")
    workflow = build_workflow()
    print("✅ Workflow built")

    print("\n📋 Step 3: Creating test claim...")
    claim_state = {
        "claim_id": "DIAG-001",
        "claim_text": "Medical claim for $500 doctor visit",
        "documents": [],
        "validation_passed": True,
        "pii_detected": False,
        "decision": None
    }
    print("✅ Test claim created")

    print("\n📋 Step 4: Processing claim...")
    print("-" * 70)

    result = workflow.invoke(claim_state)

    print("\n📋 Step 5: Analyzing result...")
    print("-" * 70)

    print(f"\nResult type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")

    print("\n📊 Full Result:")
    pprint(result, width=70, depth=5)

    print("\n📋 Step 6: Checking for expected fields...")
    print("-" * 70)

    expected_fields = ["decision", "errors", "claim_id", "validation_passed"]
    for field in expected_fields:
        if field in result:
            print(f"✅ '{field}' found: {result[field]}")
        else:
            print(f"❌ '{field}' NOT found")

    # Try to get decision
    print("\n📋 Step 7: Extracting decision...")
    print("-" * 70)

    if "decision" in result:
        print(f"✅ Decision found: {result['decision']}")
    elif "errors" in result:
        print(f"⚠️  Errors found instead of decision:")
        print(f"   {result['errors']}")
    else:
        print("❌ No decision or errors found")
        print("   Available keys:", list(result.keys()))

    print("\n" + "=" * 70)
    print("✅ DIAGNOSIS COMPLETE")
    print("=" * 70)

    # Recommendations
    print("\n💡 Recommendations:")
    print("   1. If decision field exists: Tests are correct")
    print("   2. If only errors exist: Workflow has validation error")
    print("   3. Check workflow output structure vs test expectations")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

print()
