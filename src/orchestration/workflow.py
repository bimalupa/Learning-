from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Any, Optional
from src.logger import setup_logger
from src.llm.client import get_llm
from src.safety.presidio import get_pii_detector
from src.safety.guardrails import get_guardrails
from src.rag.retriever import get_hybrid_retriever
import json

logger = setup_logger(__name__)

class ClaimState(TypedDict):
    """State structure for claim processing workflow"""
    claim_id: str
    claim_data: dict
    masked_claim: Optional[str]
    pii_detected: list
    intake_valid: bool
    policy_documents: List[str]
    validation_result: dict
    decision: dict
    errors: List[str]
    messages: List[dict]

def intake_agent(state: ClaimState) -> ClaimState:
    """Agent 1: Claim Intake - Validates and masks PII"""
    logger.info(f"Processing claim intake for {state['claim_id']}")

    try:
        # Detect and mask PII
        pii_detector = get_pii_detector()
        claim_text = json.dumps(state["claim_data"])
        masked_text, pii_entities = pii_detector.mask_pii(claim_text)

        state["masked_claim"] = masked_text
        state["pii_detected"] = pii_entities

        # Validate input with guardrails
        guardrails = get_guardrails()
        is_valid, message = guardrails.validate_claim_input(state["claim_data"])

        state["intake_valid"] = is_valid
        if not is_valid:
            state["errors"].append(f"Intake validation failed: {message}")
            logger.warning(f"Claim intake validation failed: {message}")

        state["messages"].append({
            "role": "intake_agent",
            "content": f"Claim intake complete. Valid: {is_valid}. PII masked: {len(pii_entities)} entities"
        })

    except Exception as e:
        state["errors"].append(f"Intake agent error: {str(e)}")
        logger.error(f"Error in intake agent: {str(e)}")

    return state

def retrieval_agent(state: ClaimState) -> ClaimState:
    """Agent 2: Document Retrieval - Retrieves relevant policy documents"""
    logger.info(f"Retrieving policy documents for claim {state['claim_id']}")

    try:
        if not state["intake_valid"]:
            logger.warning("Skipping retrieval for invalid claim")
            return state

        # Use hybrid retriever
        retriever = get_hybrid_retriever()
        query = f"{state['claim_data'].get('type', '')} {state['claim_data'].get('description', '')}"

        documents = retriever.retrieve(query)
        state["policy_documents"] = [doc.page_content for doc in documents]

        state["messages"].append({
            "role": "retrieval_agent",
            "content": f"Retrieved {len(state['policy_documents'])} relevant policy documents"
        })

    except Exception as e:
        state["errors"].append(f"Retrieval agent error: {str(e)}")
        logger.error(f"Error in retrieval agent: {str(e)}")

    return state

def validation_agent(state: ClaimState) -> ClaimState:
    """Agent 3: Claim Validation - Validates claim against policies"""
    logger.info(f"Validating claim {state['claim_id']}")

    try:
        if not state["intake_valid"]:
            state["validation_result"] = {"status": "INVALID_INTAKE", "confidence": 0}
            return state

        llm = get_llm()

        # Prepare validation prompt
        policy_context = "\n".join(state["policy_documents"][:3]) if state["policy_documents"] else "No policies found"

        prompt = f"""
        Validate the following insurance claim against the policy documents.

        Claim Type: {state['claim_data'].get('type', 'Unknown')}
        Amount: ${state['claim_data'].get('amount', 0)}
        Description: {state['claim_data'].get('description', '')}

        Relevant Policies:
        {policy_context}

        Provide validation result with:
        1. Is claim valid according to policies?
        2. Are all required fields present?
        3. Does amount seem reasonable?
        4. What is your confidence level (0-1)?

        Format your response as JSON with keys: is_valid, missing_fields, is_reasonable, confidence
        """

        response = llm.invoke(prompt)

        # Parse response
        try:
            validation_json = json.loads(response.content)
            state["validation_result"] = validation_json
        except:
            state["validation_result"] = {
                "is_valid": True,
                "missing_fields": [],
                "is_reasonable": True,
                "confidence": 0.7
            }

        state["messages"].append({
            "role": "validation_agent",
            "content": f"Claim validation complete. Valid: {state['validation_result'].get('is_valid', False)}"
        })

    except Exception as e:
        state["errors"].append(f"Validation agent error: {str(e)}")
        logger.error(f"Error in validation agent: {str(e)}")

    return state

def decision_agent(state: ClaimState) -> ClaimState:
    """Agent 4: Decision Making - Makes final claim decision"""
    logger.info(f"Making decision for claim {state['claim_id']}")

    try:
        if not state["intake_valid"]:
            state["decision"] = {
                "status": "REJECTED",
                "reason": "Failed intake validation",
                "confidence": 1.0
            }
            return state

        llm = get_llm()
        validation = state.get("validation_result", {})

        prompt = f"""
        Based on the following validation results, make a final claim decision.

        Validation Result: {json.dumps(validation)}
        Claim Amount: ${state['claim_data'].get('amount', 0)}
        Claim Type: {state['claim_data'].get('type', '')}

        Provide decision with:
        1. Status: APPROVED, REJECTED, or REVIEW (for borderline cases)
        2. Detailed reason for decision
        3. Confidence level (0-1)
        4. Any required next steps

        Format your response as JSON with keys: status, reason, confidence, next_steps
        """

        response = llm.invoke(prompt)

        try:
            decision_json = json.loads(response.content)
            state["decision"] = decision_json
        except:
            state["decision"] = {
                "status": "REVIEW" if validation.get("confidence", 0.5) < 0.7 else "APPROVED",
                "reason": "Unable to parse detailed decision",
                "confidence": 0.5,
                "next_steps": ["Manual review required"]
            }

        # Validate decision with guardrails
        guardrails = get_guardrails()
        is_valid, msg = guardrails.validate_decision(state["decision"])

        if not is_valid:
            state["decision"]["status"] = "REVIEW"
            state["errors"].append(f"Decision validation: {msg}")
            logger.warning(f"Decision validation failed: {msg}")

        state["messages"].append({
            "role": "decision_agent",
            "content": f"Decision: {state['decision'].get('status', 'UNKNOWN')}"
        })

    except Exception as e:
        state["errors"].append(f"Decision agent error: {str(e)}")
        logger.error(f"Error in decision agent: {str(e)}")
        state["decision"] = {
            "status": "REVIEW",
            "reason": f"System error: {str(e)}",
            "confidence": 0.0
        }

    return state

def build_workflow():
    """Build LangGraph workflow"""
    logger.info("Building claim processing workflow")

    workflow = StateGraph(ClaimState)

    # Add nodes
    workflow.add_node("intake", intake_agent)
    workflow.add_node("retrieval", retrieval_agent)
    workflow.add_node("validation", validation_agent)
    workflow.add_node("decision", decision_agent)

    # Add edges
    workflow.set_entry_point("intake")
    workflow.add_edge("intake", "retrieval")
    workflow.add_edge("retrieval", "validation")
    workflow.add_edge("validation", "decision")
    workflow.add_edge("decision", END)

    return workflow.compile()

# Global workflow
_workflow = None

def get_workflow():
    global _workflow
    if _workflow is None:
        _workflow = build_workflow()
    return _workflow

def process_claim(claim_id: str, claim_data: dict):
    """Process a claim through the workflow"""
    logger.info(f"Starting claim processing for {claim_id}")

    initial_state: ClaimState = {
        "claim_id": claim_id,
        "claim_data": claim_data,
        "masked_claim": None,
        "pii_detected": [],
        "intake_valid": False,
        "policy_documents": [],
        "validation_result": {},
        "decision": {},
        "errors": [],
        "messages": [],
    }

    workflow = get_workflow()
    final_state = workflow.invoke(initial_state)

    logger.info(f"Claim processing complete for {claim_id}. Decision: {final_state['decision']}")
    return final_state
