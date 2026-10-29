# 🏥 Insurance Claim Processing System

A sophisticated multi-agent AI system for intelligent insurance claim assessment using **LangGraph**, **ChromaDB**, **Azure OpenAI**, and **Streamlit**.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit UI (Frontend)                   │
├─────────────────────────────────────────────────────────────┤
│                  Claim Processing Workflow                   │
│  ┌─────────────┬──────────────┬──────────────┬────────────┐ │
│  │   Intake    │ Retrieval    │ Validation   │ Decision   │ │
│  │   Agent     │ Agent        │ Agent        │ Agent      │ │
│  └─────────────┴──────────────┴──────────────┴────────────┘ │
├─────────────────────────────────────────────────────────────┤
│              Safety & Data Protection Layer                  │
│  ┌──────────────────────┬──────────────────────────────────┐ │
│  │  Presidio PII        │  NeMo Guardrails Safety          │ │
│  │  Detection/Masking   │  Validation & Control            │ │
│  └──────────────────────┴──────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                     Intelligence Layer                       │
│  ┌──────────────┬─────────────┬──────────────┬────────────┐  │
│  │  LLM Inference│  Embeddings │ Vector Search│ Reranking  │  │
│  │  (GPT-3.5T)  │  (ADA-003)   │  (ChromaDB)  │ (Cross-E)  │  │
│  └──────────────┴─────────────┴──────────────┴────────────┘  │
├─────────────────────────────────────────────────────────────┤
│              Evaluation & Observability                      │
│  ┌──────────────┬──────────────────────────────────────────┐ │
│  │  RAGAS       │  Python Logging (JSON format)            │ │
│  │  Evaluation  │  Comprehensive audit trails              │ │
│  └──────────────┴──────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestration** | LangGraph | Stateful multi-agent pipeline |
| **LLM Inference** | Azure OpenAI (GPT-3.5 Turbo) | Claim analysis & decision |
| **Embeddings** | Azure text-embedding-3-large | Semantic search |
| **Vector DB** | ChromaDB | Policy & document storage |
| **Search** | BM25 + Semantic + Cross-Encoder | Hybrid retrieval |
| **Data Protection** | Microsoft Presidio | PII detection & masking |
| **Safety Layer** | NeMo Guardrails | LLM validation & control |
| **Evaluation** | RAGAS | RAG pipeline metrics |
| **Observability** | Python Logging | Audit trails |
| **UI** | Streamlit | Interactive deployment |

## 📁 Project Structure

```
insurance-claim-processor/
├── config/
│   └── settings.py                 # Configuration management
├── src/
│   ├── llm/
│   │   ├── client.py               # LLM & embedding clients
│   │   └── __init__.py
│   ├── rag/
│   │   ├── vector_store.py         # ChromaDB integration
│   │   ├── retriever.py            # Hybrid search
│   │   ├── reranker.py             # Cross-encoder reranking
│   │   └── __init__.py
│   ├── agents/
│   │   └── (orchestrated by workflow.py)
│   ├── orchestration/
│   │   └── workflow.py             # LangGraph multi-agent workflow
│   ├── safety/
│   │   ├── presidio.py             # PII detection/masking
│   │   ├── guardrails.py           # Safety validation
│   │   └── __init__.py
│   ├── evaluation/
│   │   └── ragas_eval.py           # RAGAS evaluation
│   ├── logger.py                   # JSON logging
│   └── __init__.py
├── ui/
│   └── app.py                      # Streamlit application
├── data/
│   ├── sample_policies.json        # Policy database
│   ├── chroma_db/                  # Vector store (persistent)
│   └── uploads/                    # User uploads
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
├── setup.py                        # Initialization script
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- pip
- (Optional) Azure subscription for OpenAI or OpenAI API key

### 2. Installation

```bash
# Clone or download the project
cd insurance-claim-processor

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
# For testing without keys, most features will work
```

### 3. Configuration

Edit `.env` file:

```env
# Azure OpenAI (preferred)
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo

# OR OpenAI (fallback)
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-3.5-turbo

# Application
LOG_LEVEL=INFO
DEBUG=False
```

### 4. Initialize System

```bash
# Setup knowledge base and verify connections
python setup.py

# Output:
# ✅ Knowledge base initialized with X documents
# ✅ LLM connection verified
```

### 5. Run Application

```bash
# Start Streamlit UI
streamlit run ui/app.py

# UI will be available at: http://localhost:8501
```

## 📊 System Features

### 🔄 Multi-Agent Workflow

1. **Intake Agent**: Validates claim, detects & masks PII
2. **Retrieval Agent**: Searches relevant policy documents (hybrid search)
3. **Validation Agent**: Validates claim against policies using LLM
4. **Decision Agent**: Makes final APPROVED/REJECTED/REVIEW decision

### 🛡️ Safety & Compliance

- **PII Detection**: Automatic detection of sensitive data (SSN, phone, email, etc.)
- **PII Masking**: Replaces sensitive data with placeholders
- **Guardrails**: Validates claim inputs and LLM outputs
- **Audit Logging**: JSON-formatted audit trail of all decisions

### 🔍 Intelligent Search

- **Semantic Search**: Vector similarity using embeddings
- **BM25 Search**: Traditional keyword-based search
- **Cross-Encoder Reranking**: Intelligent ranking of results
- **Hybrid Retrieval**: Combines semantic + BM25 for best results

### 📈 Evaluation & Metrics

- **RAGAS Metrics**: Context relevancy, faithfulness
- **Decision Confidence**: Confidence scores for each decision
- **Performance Tracking**: Monitor claim processing metrics

### 🎨 User Interface

- **Claim Submission**: Form for entering claim details
- **Real-time Processing**: Multi-agent pipeline visualization
- **Claims History**: View all processed claims
- **Decision Analytics**: Statistics and insights
- **Knowledge Base Management**: Add policies and test PII detection

## 📝 Usage Examples

### Process a Claim Programmatically

```python
from src.orchestration.workflow import process_claim

claim_data = {
    "type": "Medical",
    "amount": 50000,
    "policy_number": "POL-MED-123",
    "claimant_name": "John Doe",
    "description": "Emergency hospital visit for appendicitis",
}

result = process_claim("CLAIM-001", claim_data)

print(f"Decision: {result['decision']['status']}")
print(f"Confidence: {result['decision']['confidence']:.1%}")
print(f"Reason: {result['decision']['reason']}")
```

### Add Policy Documents

```python
from src.rag.vector_store import get_vector_store
from langchain.schema import Document

vector_store = get_vector_store()

doc = Document(
    page_content="Coverage details for medical procedures...",
    metadata={"type": "policy", "category": "medical"}
)

vector_store.add_documents([doc])
```

### Test PII Detection

```python
from src.safety.presidio import get_pii_detector

detector = get_pii_detector()

text = "My name is Jane Smith and my email is jane@example.com"
entities = detector.detect_pii(text)

for entity in entities:
    print(f"{entity['entity_type']}: {entity['text']}")
```

## 🔌 API Integrations

### Azure OpenAI Configuration

```env
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

### OpenAI Fallback

If Azure is not available, the system automatically falls back to OpenAI:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```

## 📊 Decision Workflow

```
Input Claim
    ↓
[Intake Agent] → Validate & Mask PII
    ↓
[Retrieval Agent] → Find Relevant Policies
    ↓
[Validation Agent] → Check Policy Compliance
    ↓
[Decision Agent] → Generate Decision
    ↓
Output: APPROVED | REJECTED | REVIEW
```

## 🛠️ Customization

### Add Custom Guardrails

Edit `src/safety/guardrails.py`:

```python
def validate_claim_input(self, claim_data: dict):
    # Add your custom validation logic
    if claim_data.get("amount") > YOUR_THRESHOLD:
        return False, "Custom validation failed"
    return True, "Passed"
```

### Modify Workflow Agents

Edit `src/orchestration/workflow.py`:

```python
def custom_agent(state: ClaimState) -> ClaimState:
    # Your custom agent logic
    return state
```

### Update Policy Database

Edit `data/sample_policies.json` or add documents via Streamlit UI.

## 📊 Monitoring & Logging

All operations are logged in JSON format for easy parsing:

```json
{
  "timestamp": "2024-10-29T10:30:45.123456",
  "level": "INFO",
  "logger": "insurance-claim-processor",
  "message": "Claim intake complete. Valid: True",
  "module": "workflow",
  "function": "intake_agent",
  "line": 42
}
```

View logs:
```bash
# Follow real-time logs
tail -f logs/app.log | jq .

# Filter by agent
grep "intake_agent" logs/app.log
```

## 🧪 Testing

Run example claims:

```bash
python -c "
from src.orchestration.workflow import process_claim

# Test medical claim
result = process_claim('TEST-001', {
    'type': 'Medical',
    'amount': 25000,
    'policy_number': 'POL-MED-001',
    'claimant_name': 'Test User',
    'description': 'Hospital visit for surgery'
})

print('Status:', result['decision']['status'])
print('Confidence:', result['decision']['confidence'])
"
```

## 🚨 Troubleshooting

### LLM Connection Issues

```
❌ Error: No LLM API key configured
```

**Solution**: Add API keys to `.env`:
```bash
cp .env.example .env
# Edit .env with your keys
```

### Vector Store Not Found

```
❌ Error: ChromaDB path not found
```

**Solution**: Run setup:
```bash
python setup.py
```

### Out of Memory

**Solution**: Clear ChromaDB cache:
```bash
rm -rf data/chroma_db
python setup.py
```

## 📈 Performance Tuning

### Optimize Retrieval

```python
retriever = get_hybrid_retriever(alpha=0.7)  # Increase semantic weight
results = retriever.retrieve(query, k=10)    # Get more results
```

### Reduce LLM Calls

Set `max_tokens` in `src/llm/client.py`:
```python
max_tokens=1000  # Reduce from 2000
```

### Faster Embeddings

Use lightweight model:
```python
# In src/llm/client.py
return HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## 🔐 Security Considerations

- ✅ PII automatically detected and masked
- ✅ All sensitive data logged as placeholders
- ✅ Input validation with guardrails
- ✅ API keys managed via environment variables
- ⚠️ Store `.env` securely, don't commit to git

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

To extend the system:

1. Add new agents to `src/orchestration/workflow.py`
2. Implement safety checks in `src/safety/guardrails.py`
3. Add evaluation metrics to `src/evaluation/ragas_eval.py`
4. Update UI in `ui/app.py`

## 📞 Support

For issues or questions:
1. Check logs in JSON format
2. Review error messages in Streamlit UI
3. Test components individually
4. Verify API key configuration

---

**Built with ❤️ using LangGraph, ChromaDB & Streamlit**
