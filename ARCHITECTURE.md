# 🏗️ Architecture Documentation

## System Overview

The Insurance Claim Processing System is a sophisticated multi-agent AI pipeline designed for intelligent claim assessment. It orchestrates multiple specialized agents through LangGraph, combining RAG (Retrieval-Augmented Generation), safety controls, and LLM inference.

```
┌─────────────────────────────────────────────────────┐
│         User Interface (Streamlit)                  │
│  - Claim submission form                            │
│  - Real-time processing visualization               │
│  - Claims history and analytics                     │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│    Claim Processing Orchestration (LangGraph)       │
│                                                      │
│  State: ClaimState (TypedDict)                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ • claim_id                                   │   │
│  │ • claim_data                                 │   │
│  │ • masked_claim (PII removed)                 │   │
│  │ • policy_documents (retrieved)               │   │
│  │ • validation_result                          │   │
│  │ • decision                                   │   │
│  │ • messages (agent trail)                     │   │
│  │ • errors                                     │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┬────────────┐
        │          │          │            │
        ▼          ▼          ▼            ▼
    ┌────────┐┌────────┐┌────────┐┌──────────┐
    │ Intake ││Retrieval││Validation││Decision │
    │ Agent  ││ Agent  ││ Agent   ││ Agent   │
    └───┬────┘└───┬────┘└───┬────┘└──┬──────┘
        │         │         │        │
        └─────────▼─────────▼────────┘
                  │
        ┌─────────▼──────────┐
        │  Safety Layer      │
        ├────────────────────┤
        │ • Presidio PII     │
        │ • NeMo Guardrails  │
        │ • Input/Output Val │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────────────────┐
        │  Intelligence Layer             │
        ├─────────────────────────────────┤
        │ • LLM: Azure OpenAI GPT-3.5T   │
        │ • Embeddings: text-embedding-3 │
        │ • Search: Hybrid (Semantic+BM25)
        │ • Reranking: Cross-Encoder     │
        │ • Storage: ChromaDB            │
        └─────────┬──────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  Observability     │
        ├────────────────────┤
        │ • JSON Logging     │
        │ • RAGAS Evaluation │
        │ • Audit Trail      │
        └────────────────────┘
```

## Component Architecture

### 1. Multi-Agent Orchestration (LangGraph)

**File**: `src/orchestration/workflow.py`

#### Agents:

##### Intake Agent
```python
intake_agent(state: ClaimState) -> ClaimState
```
- **Purpose**: Validate and prepare claim data
- **Operations**:
  - Detect PII with Presidio
  - Mask sensitive information
  - Validate claim input with guardrails
  - Check amount, type, required fields
- **Output**: 
  - `masked_claim`: Claim with PII replaced
  - `pii_detected`: List of detected entities
  - `intake_valid`: Boolean validation result

##### Retrieval Agent
```python
retrieval_agent(state: ClaimState) -> ClaimState
```
- **Purpose**: Find relevant policy documents
- **Operations**:
  - Use hybrid retriever (semantic + BM25)
  - Apply cross-encoder reranking
  - Limit results to top-k documents
- **Output**:
  - `policy_documents`: Retrieved document texts

##### Validation Agent
```python
validation_agent(state: ClaimState) -> ClaimState
```
- **Purpose**: Validate claim against policies
- **Operations**:
  - Call LLM with claim + policy context
  - Check policy compliance
  - Verify required fields
  - Assess claim reasonableness
- **Output**:
  - `validation_result`: JSON with validation details

##### Decision Agent
```python
decision_agent(state: ClaimState) -> ClaimState
```
- **Purpose**: Make final claim decision
- **Operations**:
  - Analyze validation results
  - Generate decision rationale
  - Assign confidence score
  - Determine next steps
  - Validate decision with guardrails
- **Output**:
  - `decision`: APPROVED/REJECTED/REVIEW with reason

#### Workflow Graph:

```
Intake → Retrieval → Validation → Decision → END
  ↓
  └─→ Guardrails Validation
      └─→ Safety Layer Checks
```

### 2. RAG (Retrieval-Augmented Generation)

**Files**:
- `src/rag/vector_store.py` - ChromaDB integration
- `src/rag/retriever.py` - Hybrid search
- `src/rag/reranker.py` - Cross-encoder reranking

#### Vector Store (ChromaDB)
```python
class VectorStore:
    - add_documents(docs) → chunks & embeds
    - search(query) → semantic similarity
    - get_retriever() → LangChain interface
```

#### Hybrid Retriever
```python
class HybridRetriever:
    - Semantic search (embeddings)
    - BM25 search (keywords)
    - Combine results by weight
    - Rerank with cross-encoder
```

#### Cross-Encoder Reranker
```python
class CrossEncoderReranker:
    - Score document-query pairs
    - Rank by relevance
    - Return top-k results
```

### 3. LLM & Embeddings

**File**: `src/llm/client.py`

#### LLM Client
- **Primary**: Azure OpenAI (GPT-3.5 Turbo)
- **Fallback**: OpenAI API
- **Config**: Via environment variables

#### Embedding Model
- **Primary**: Azure text-embedding-3-large
- **Fallback**: sentence-transformers (all-MiniLM-L6-v2)

### 4. Safety & Data Protection

#### Presidio PII Detection

**File**: `src/safety/presidio.py`

```python
class PIIDetectionMasking:
    - detect_pii(text) → entities with confidence
    - mask_pii(text) → anonymized text + entities
    - is_pii_detected(text, threshold)
```

**Detects**:
- PERSON names
- EMAIL_ADDRESS
- PHONE_NUMBER
- CREDIT_CARD
- SSN
- DATE_TIME
- URL

#### NeMo Guardrails

**File**: `src/safety/guardrails.py`

```python
class SafetyGuardrails:
    - validate_claim_input(claim)
    - validate_llm_output(output)
    - validate_decision(decision)
```

**Checks**:
- Amount thresholds
- Blocked keywords (fraud, illegal, etc.)
- SQL injection patterns
- Decision consistency
- Confidence requirements

### 5. Observability & Logging

**File**: `src/logger.py`

#### JSON Logger
```json
{
  "timestamp": "2024-10-29T10:30:45.123456",
  "level": "INFO",
  "logger": "insurance-claim-processor",
  "message": "Claim processing complete",
  "module": "workflow",
  "function": "process_claim",
  "line": 42
}
```

#### RAGAS Evaluation

**File**: `src/evaluation/ragas_eval.py`

```python
class RAGASEvaluator:
    - evaluate_retrieval(queries, docs, answers)
    - evaluate_generation(questions, texts, contexts)
    - Metrics: faithfulness, context_relevancy
```

### 6. User Interface

**File**: `ui/app.py`

#### Pages:
1. **Process Claim** - Claim submission & real-time processing
2. **View Results** - Claims history & details
3. **System Status** - Component health & statistics
4. **Knowledge Base** - Policy management & PII testing

## Data Flow

### Claim Processing Flow

```
User Submission
    ↓
┌───────────────────────────────────────┐
│ INTAKE PHASE                          │
├───────────────────────────────────────┤
│ 1. Validate input with guardrails    │
│ 2. Detect PII with Presidio           │
│ 3. Mask sensitive data                │
│ 4. Check claim feasibility            │
└───────────┬───────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ RETRIEVAL PHASE                       │
├───────────────────────────────────────┤
│ 1. Generate search query              │
│ 2. Semantic search (embeddings)      │
│ 3. BM25 search (keywords)            │
│ 4. Merge & deduplicate               │
│ 5. Rerank with cross-encoder         │
│ 6. Return top-k documents            │
└───────────┬───────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ VALIDATION PHASE                      │
├───────────────────────────────────────┤
│ 1. Prepare LLM prompt                 │
│ 2. Add claim + policies + context     │
│ 3. Call LLM for validation            │
│ 4. Parse structured response          │
│ 5. Check policy compliance            │
└───────────┬───────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ DECISION PHASE                        │
├───────────────────────────────────────┤
│ 1. Analyze validation results         │
│ 2. Call LLM for decision making       │
│ 3. Generate decision rationale        │
│ 4. Assign confidence score            │
│ 5. Validate with guardrails           │
│ 6. Return decision + next steps       │
└───────────┬───────────────────────────┘
            ↓
Final Decision (APPROVED/REJECTED/REVIEW)
    ↓
Audit Log & User Notification
```

## State Management

### ClaimState TypedDict

```python
{
    "claim_id": str,                  # Unique claim identifier
    "claim_data": dict,               # Original claim data
    "masked_claim": str,              # PII-masked claim
    "pii_detected": list,             # Detected PII entities
    "intake_valid": bool,             # Intake validation result
    "policy_documents": list,         # Retrieved policy texts
    "validation_result": dict,        # LLM validation output
    "decision": dict,                 # Final decision
    "errors": list,                   # Errors/warnings
    "messages": list,                 # Agent messages trail
}
```

## Configuration Management

**File**: `config/settings.py`

```python
Settings:
├── Azure OpenAI
│   ├── api_key
│   ├── endpoint
│   ├── deployment_name
│   └── embedding_deployment
├── Vector Store
│   ├── chroma_db_path
│   └── collection_name
├── Application
│   ├── log_level
│   └── debug
└── NeMo Guardrails
    └── enabled
```

## Performance Considerations

### Latency Breakdown

| Phase | Time | Operations |
|-------|------|-----------|
| Intake | ~100ms | Validation + PII detection |
| Retrieval | ~500ms | Hybrid search + reranking |
| Validation | ~2000ms | LLM call + parsing |
| Decision | ~1500ms | LLM call + validation |
| **Total** | **~4s** | Complete processing |

### Optimization Strategies

1. **Caching**
   - Cache embeddings for common queries
   - Store frequent policy documents
   - Reuse LLM responses

2. **Batch Processing**
   - Process multiple claims in parallel
   - Batch embedding computations
   - Bulk database operations

3. **Resource Management**
   - Limit ChromaDB search results
   - Reduce LLM max_tokens
   - Use lighter embedding model

## Security Architecture

### Data Flow Security

```
User Input
    ↓
[Input Validation]
    ↓
[PII Detection]
    ↓
[Presidio Masking]
    ↓
[Processing with Masked Data]
    ↓
[Output Validation]
    ↓
[Guardrails Check]
    ↓
Safe Decision Output
```

### PII Protection

- **Detection**: Presidio analyzer finds 10+ entity types
- **Masking**: Replace with `<ENTITY_TYPE>` placeholders
- **Logging**: Never log unmasked sensitive data
- **Audit**: All PII handling logged and tracked

## Scalability

### Horizontal Scaling

```
Load Balancer
    ├─→ Instance 1 (Streamlit)
    ├─→ Instance 2 (Streamlit)
    └─→ Instance 3 (Streamlit)
         ↓
    Shared ChromaDB (persistent)
    Shared Logs (central logging)
```

### Vertical Scaling

1. Increase `RAGAS_BATCH_SIZE`
2. Parallel agent execution
3. Async LLM calls
4. Connection pooling

## Extension Points

### Add Custom Agent

```python
def custom_agent(state: ClaimState) -> ClaimState:
    # Your logic
    state["custom_field"] = value
    return state

workflow.add_node("custom", custom_agent)
workflow.add_edge("validation", "custom")
workflow.add_edge("custom", "decision")
```

### Add Custom Guardrail

```python
def validate_custom(self, claim_data):
    # Your validation
    if condition:
        return False, "Reason"
    return True, "Passed"
```

### Add Custom Retriever

```python
class CustomRetriever:
    def retrieve(self, query):
        # Your search implementation
        return documents
```

## Deployment

### Docker Deployment

```bash
docker-compose up -d
# Runs on http://localhost:8501
```

### Cloud Deployment

#### Azure Container Instances
```bash
az container create \
  --resource-group mygroup \
  --name insurance-processor \
  --image myregistry.azurecr.io/insurance:latest \
  --environment-variables AZURE_OPENAI_API_KEY=...
```

#### AWS ECS
```bash
aws ecs run-task \
  --cluster insurance \
  --task-definition insurance-processor \
  --launch-type FARGATE
```

---

## Summary

The architecture combines:
- **Orchestration**: LangGraph for multi-agent coordination
- **Intelligence**: LLM + embeddings for reasoning
- **Search**: Hybrid retrieval with reranking
- **Safety**: Multi-layer protection with Presidio + guardrails
- **Observability**: Comprehensive logging and evaluation
- **Scalability**: Modular design for easy extension

This creates a robust, transparent, and secure claim processing system suitable for production insurance operations.
