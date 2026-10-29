# 🧪 Testing Guide - Insurance Claim Processing System

Complete testing procedures for verifying the system works correctly.

---

## 📋 Quick Start Testing

### Test 1: System Startup
```bash
# Verify all components start without errors
python setup_smart.py

# Output should show:
# ✅ All requirements are satisfied!
# ✅ Knowledge base initialized
# ✅ All components verified successfully!
# ✅ SETUP COMPLETED SUCCESSFULLY!
```

**Expected**: No errors, all checks pass ✅

---

### Test 2: Application Launch
```bash
streamlit run ui/app.py
```

**Expected**: 
- App opens in browser at `http://localhost:8501`
- All pages load without errors
- No SSL warnings in console

---

### Test 3: Web Interface Check

Navigate to each page:

#### ✅ Page 1: Process Claim
- Form displays correctly
- Input fields work
- Submit button responds

#### ✅ Page 2: View Results
- Shows previous claims
- Results display properly
- Status shows correctly

#### ✅ Page 3: System Status
- Shows component health
- Displays metrics
- Updates in real-time

#### ✅ Page 4: Knowledge Base
- Shows loaded policies
- Search works
- Results display

---

## 🎯 Functional Testing

### Test Scenario 1: Valid Claim (Should APPROVE/REVIEW)

**Input:**
```
Claim Type: Medical
Amount: $1,500
Description: Doctor visit and lab tests
Claimant SSN: MASKED (if entered)
```

**Expected Output:**
```
Status: APPROVED or REVIEW
Confidence: 85-100%
Reason: Valid claim within policy limits
```

**✅ What to verify:**
- Claim processes without errors
- PII is masked in logs
- Decision is logical
- Confidence score displayed

---

### Test Scenario 2: Invalid Claim (Should REJECT)

**Input:**
```
Claim Type: Medical
Amount: $500,000 (exceeds limits)
Description: Cosmetic surgery
```

**Expected Output:**
```
Status: REJECTED
Confidence: 95-100%
Reason: Exceeds maximum claim amount or not covered
```

**✅ What to verify:**
- System correctly identifies invalid claims
- Reason is clear and logical
- Confidence is high

---

### Test Scenario 3: Ambiguous Claim (Should REVIEW)

**Input:**
```
Claim Type: Auto
Amount: $25,000
Description: Pre-existing damage claim
```

**Expected Output:**
```
Status: REVIEW
Confidence: 60-80%
Reason: Requires manual review for pre-existing conditions
```

**✅ What to verify:**
- System correctly flags ambiguous cases
- Escalates to REVIEW status
- Confidence is moderate

---

## 🛡️ Security Testing

### Test 1: PII Detection and Masking

**Input claim with PII:**
```
Name: John Doe
SSN: 123-45-6789
Email: john@example.com
Phone: 555-123-4567
Credit Card: 4532-1111-2222-3333
```

**Expected:**
- ✅ PII detected before processing
- ✅ PII masked in logs
- ✅ PII not stored in results
- ✅ Claims processed safely

**Verification:**
```bash
# Check logs
tail -f logs/app.log | grep -i "pii\|mask\|detected"

# Should show:
# [INFO] PII detected: SSN, Email, Phone
# [INFO] PII masked successfully
```

---

### Test 2: Input Validation

**Try injecting malicious input:**
```
Amount: 1000 OR 1=1
Description: <script>alert('test')</script>
```

**Expected:**
- ✅ Input rejected
- ✅ Error message shown
- ✅ System remains stable
- ✅ No code execution

---

## 📊 Performance Testing

### Test 1: Response Time

**Measure claim processing time:**

```bash
# Time a single claim processing
time python -c "
from src.orchestration.workflow import build_workflow
import time

workflow = build_workflow()
start = time.time()
result = workflow.invoke({'claim_text': 'Test claim'})
duration = time.time() - start

print(f'Processing time: {duration:.2f} seconds')
"
```

**Expected:** 2-5 seconds per claim

---

### Test 2: Multiple Claims (Throughput)

```bash
# Process 10 claims and measure
python test_throughput.py
```

**Expected:** All 10 claims processed successfully

---

## 🔍 Integration Testing

### Test 1: Vector Store Integration

```python
from src.rag.vector_store import get_vector_store

# Initialize
vs = get_vector_store()

# Search test
results = vs.search("medical coverage limits", k=3)

# Expected: Returns relevant policy documents
print(f"Found {len(results)} relevant documents")
```

**Expected:** ✅ Returns 3 relevant policy documents

---

### Test 2: Retrieval Pipeline

```python
from src.rag.retriever import get_hybrid_retriever

# Create retriever
retriever = get_hybrid_retriever()

# Search
results = retriever.retrieve("What is covered under medical?")

# Expected: Returns policy information
print(f"Retrieved {len(results)} documents")
```

**Expected:** ✅ Returns relevant policies

---

### Test 3: End-to-End Workflow

```python
from src.orchestration.workflow import build_workflow
from langchain.schema import Document

# Build workflow
workflow = build_workflow()

# Test claim
claim = {
    "claim_id": "TEST-001",
    "claim_text": "Medical claim for $2000 doctor visit",
    "documents": []
}

# Process
result = workflow.invoke(claim)

# Verify
assert "decision" in result
assert result["decision"] in ["APPROVED", "REJECTED", "REVIEW"]
print(f"✅ Workflow test passed: {result['decision']}")
```

**Expected:** ✅ Returns valid decision

---

## 📝 Log Testing

### Check Application Logs

```bash
# View recent logs
cat logs/app.log | tail -50

# Filter by level
grep "\[ERROR\]" logs/app.log    # Show errors
grep "\[WARNING\]" logs/app.log  # Show warnings
grep "\[INFO\]" logs/app.log     # Show info

# Search for specific events
grep "claim processing" logs/app.log
grep "PII detected" logs/app.log
```

**Expected:**
- ✅ Structured JSON logs
- ✅ Timestamp on each entry
- ✅ Clear error messages
- ✅ Audit trail of decisions

---

## 🧩 Component Testing

### Test 1: LLM Client
```bash
python -c "
from src.llm.client import get_llm

llm = get_llm()
response = llm.invoke('Say hello')
print('✅ LLM working:', response.content[:50])
"
```

**Expected:** ✅ LLM responds

---

### Test 2: Embeddings
```bash
python -c "
from src.llm.client import get_embedding_model

embeddings = get_embedding_model()
emb = embeddings.embed_query('test')
print(f'✅ Embeddings working: {len(emb)} dimensions')
"
```

**Expected:** ✅ Returns embedding vector

---

### Test 3: Presidio PII Detection
```bash
from src.safety.presidio import PIIDetectionMasking

pii = PIIDetectionMasking()
text = "My SSN is 123-45-6789 and email is john@example.com"
result = pii.detect_and_mask(text)

print(f"✅ PII masked: {result}")
```

**Expected:** ✅ PII entities detected and masked

---

## 📊 Data Testing

### Test 1: Sample Policies Load

```bash
python -c "
import json
from pathlib import Path

# Load policies
policies = json.load(open('data/sample_policies.json'))
print(f'✅ Loaded {len(policies[\"policies\"])} policies')

# Verify structure
for policy in policies['policies']:
    assert 'id' in policy
    assert 'type' in policy
    assert 'coverage' in policy
print('✅ All policies have required fields')
"
```

**Expected:** ✅ 5 policies loaded with correct structure

---

### Test 2: Database Persistence

```bash
# Check if ChromaDB persists data
ls -la data/chroma_db/

# Should show files like:
# chroma.db
# chroma.sqlite
```

**Expected:** ✅ Database files exist

---

## ✅ Final Verification Checklist

- [ ] Setup runs without errors
- [ ] App launches in browser
- [ ] All pages load
- [ ] Can submit claims
- [ ] Claims get processed
- [ ] Decisions are logical
- [ ] PII is masked
- [ ] No SSL errors
- [ ] Logs are created
- [ ] Response time < 5 sec
- [ ] Multiple claims work
- [ ] Results persist
- [ ] Can view history
- [ ] System doesn't crash

---

## 🚀 Running Full Test Suite

If you have a test file:

```bash
python test_system.py -v
```

Or run individual tests:

```bash
python -m pytest test_system.py::test_pii_detection -v
python -m pytest test_system.py::test_vector_store -v
python -m pytest test_system.py::test_workflow -v
```

---

## 📈 Test Results Template

Create a file `TEST_RESULTS.md`:

```markdown
# Test Results - [Date]

## System Health
- [ ] Setup successful
- [ ] All components start
- [ ] No import errors
- [ ] No SSL errors

## Functional Tests
- [ ] Valid claim → Correct decision
- [ ] Invalid claim → Rejected
- [ ] Ambiguous claim → Review
- [ ] Response time < 5 sec

## Security Tests
- [ ] PII detected
- [ ] PII masked
- [ ] No PII in logs
- [ ] Input validation works

## Integration Tests
- [ ] Vector store works
- [ ] Retriever works
- [ ] Workflow processes
- [ ] LLM responds

## Issues Found
- [ ] (None if all pass)

## Overall Status
✅ PASS / ❌ FAIL
```

---

## 🆘 Troubleshooting Tests

### If claim processing fails:
```bash
python -c "
from src.orchestration.workflow import build_workflow
try:
    workflow = build_workflow()
    print('✅ Workflow builds')
except Exception as e:
    print(f'❌ Workflow error: {e}')
"
```

### If PII detection fails:
```bash
python -c "
from src.safety.presidio import PIIDetectionMasking
try:
    pii = PIIDetectionMasking()
    print('✅ Presidio loads')
except Exception as e:
    print(f'❌ Presidio error: {e}')
"
```

### If vector store fails:
```bash
python -c "
from src.rag.vector_store import get_vector_store
try:
    vs = get_vector_store()
    print('✅ Vector store initializes')
except Exception as e:
    print(f'❌ Vector store error: {e}')
"
```

---

## 📞 Test Support

If you encounter issues:

1. **Check logs**: `tail -f logs/app.log`
2. **Run component tests**: See above
3. **Verify imports**: `python fix_imports.py`
4. **Check SSL**: `python fix_ssl_issue.py`
5. **Review requirements**: `pip list | grep langchain`

---

## 🎯 Next Steps After Testing

Once all tests pass:

1. ✅ Deploy to production
2. ✅ Monitor logs
3. ✅ Scale as needed
4. ✅ Add more policies
5. ✅ Customize rules

---

*Last Updated: 2024-10-29*
*Testing Guide v1.0*

**Happy Testing!** 🚀
