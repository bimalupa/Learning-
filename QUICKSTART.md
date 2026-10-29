# 🚀 Quick Start Guide

Get the Insurance Claim Processing System running in 5 minutes!

## Option 1: Using OpenAI (Fastest)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure OpenAI
```bash
cp .env.example .env

# Edit .env and add your OpenAI key
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-3.5-turbo
```

### Step 3: Initialize System
```bash
python setup.py

# Output: ✅ Knowledge base initialized with X documents
```

### Step 4: Run Tests (Optional)
```bash
python test_system.py

# Validates all components are working
```

### Step 5: Start Application
```bash
streamlit run ui/app.py

# Opens: http://localhost:8501
```

---

## Option 2: Using Azure OpenAI

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Azure
```bash
cp .env.example .env

# Edit .env with Azure credentials:
# AZURE_OPENAI_API_KEY=your-key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
# AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

### Step 3-5: Same as Option 1

---

## Testing Without API Keys

Most features work without keys for demonstration:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize (creates sample policies)
python setup.py

# 3. Run tests (uses mock LLM)
python test_system.py

# 4. Start UI
streamlit run ui/app.py
```

Note: LLM features will fail gracefully with an error message.

---

## 📊 Using the Streamlit UI

### Process a Claim
1. Open http://localhost:8501
2. Go to "Process Claim" tab
3. Fill in the form:
   - Select claim type (Medical, Property, Auto, etc.)
   - Enter amount, policy number, claimant info
   - Write claim description
4. Click "Process Claim"
5. View decision and details

### View Results
- Go to "View Results" tab
- See all processed claims in a table
- Click on a claim to view full details
- Export as JSON

### Manage Knowledge Base
- Go to "Knowledge Base" tab
- Add custom policy documents
- Test PII detection on sample text

### Monitor System
- Go to "System Status" tab
- View component status
- See decision statistics
- Monitor claim metrics

---

## 🔧 Troubleshooting

### Error: "No LLM API key configured"
**Solution:** Add API key to `.env` file and restart

### Error: "Module not found"
**Solution:** Run `pip install -r requirements.txt` in project root

### Vector store not initializing
**Solution:** Run `python setup.py` to initialize

### Streamlit port already in use
**Solution:** Use different port:
```bash
streamlit run ui/app.py --server.port 8502
```

### Memory issues with ChromaDB
**Solution:** Clear and reinitialize:
```bash
rm -rf data/chroma_db
python setup.py
```

---

## 📖 Key Features Demo

### 1. Multi-Agent Processing
- Intake Agent: Validates claim
- Retrieval Agent: Finds policies
- Validation Agent: Checks compliance
- Decision Agent: Makes decision

### 2. PII Protection
Claims are automatically scanned for:
- Names, SSN, phone numbers
- Email addresses, credit cards
- Dates of birth
All masked before processing ✅

### 3. Intelligent Search
- Semantic search via embeddings
- Keyword search (BM25)
- Cross-encoder reranking
- Hybrid approach for best results

### 4. Safety Guardrails
- Input validation
- Output verification
- Decision consistency checks
- Fraud detection keywords

---

## 🎯 Example Workflows

### Medical Claim
```
Type: Medical
Amount: $50,000
Description: Emergency hospital visit for appendicitis
Policy: POL-MED-001

↓ Processing...

Decision: APPROVED
Confidence: 95%
Reason: Matches policy coverage, valid documentation
```

### Property Claim
```
Type: Property
Amount: $100,000
Description: Fire damage to home
Policy: POL-PROP-001

↓ Processing...

Decision: REVIEW
Confidence: 65%
Reason: Requires inspection, amount verification needed
```

### Auto Claim
```
Type: Auto
Amount: $25,000
Description: Collision damage from accident
Policy: POL-AUTO-001

↓ Processing...

Decision: APPROVED
Confidence: 88%
Reason: Clear accident report, policy covers collision
```

---

## 📊 Performance Metrics

Typical processing time per claim:
- Intake validation: ~100ms
- Document retrieval: ~500ms
- Policy validation: ~2000ms
- Decision generation: ~1500ms
- **Total: ~4 seconds**

---

## 🔐 Security Features

✅ **PII Detection & Masking**
- Automatic detection of sensitive data
- Replaced with placeholders in processing
- Original data never logged

✅ **Audit Trail**
- All decisions logged with JSON formatting
- Includes confidence scores
- Full claim processing history

✅ **Input Validation**
- Claim amount limits
- Type validation
- Fraud keyword detection

✅ **Output Validation**
- LLM output checking
- Decision consistency
- Confidence thresholds

---

## 💡 Next Steps

1. **Process Real Claims**: Use your actual insurance data
2. **Add More Policies**: Upload your policy documents
3. **Customize Decision Logic**: Modify guardrails and agents
4. **Deploy**: Use Docker or cloud platforms
5. **Integrate**: Connect to existing systems via API

---

## 📞 Need Help?

1. Check README.md for detailed documentation
2. Review test_system.py for component examples
3. Check .env.example for configuration options
4. Look at logs for error details

---

**Ready? Start with:**
```bash
pip install -r requirements.txt
python setup.py
streamlit run ui/app.py
```

Enjoy! 🎉
