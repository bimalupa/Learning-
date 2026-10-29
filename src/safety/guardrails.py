from src.logger import setup_logger
from typing import Tuple
import re

logger = setup_logger(__name__)

class SafetyGuardrails:
    """NeMo Guardrails-inspired safety validation layer"""

    def __init__(self):
        self.enabled = True
        # Define policy keywords to block
        self.blocked_keywords = [
            "fraudulent", "fraud", "fake", "stolen",
            "illegal", "malicious", "hack", "unauthorized"
        ]

        # Define harmful patterns
        self.harmful_patterns = [
            r"drop\s+table",
            r"delete\s+from",
            r"exec\s+\(",
            r"eval\s*\(",
        ]

    def validate_claim_input(self, claim_data: dict) -> Tuple[bool, str]:
        """Validate claim input for safety"""

        # Check claim amount is reasonable
        claim_amount = claim_data.get("amount", 0)
        if claim_amount > 10_000_000:  # Example threshold
            return False, "Claim amount exceeds maximum threshold"

        if claim_amount <= 0:
            return False, "Claim amount must be positive"

        # Check claim description for blocked content
        description = claim_data.get("description", "").lower()
        for keyword in self.blocked_keywords:
            if keyword in description:
                logger.warning(f"Blocked keyword '{keyword}' detected in claim")
                return False, f"Claim description contains inappropriate content: {keyword}"

        # Check for injection patterns
        for pattern in self.harmful_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                logger.warning(f"Harmful pattern detected: {pattern}")
                return False, "Claim description contains potentially harmful content"

        return True, "Claim input validated"

    def validate_llm_output(self, output: str) -> Tuple[bool, str]:
        """Validate LLM output for safety"""

        if not output or len(output) == 0:
            return False, "Empty LLM output"

        output_lower = output.lower()

        # Check for refusals or errors
        if any(phrase in output_lower for phrase in ["i cannot", "i cannot help", "this violates"]):
            logger.warning("LLM produced refusal output")
            return False, "LLM refused to process request"

        # Check for injection patterns
        for pattern in self.harmful_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                logger.warning(f"Harmful pattern in LLM output: {pattern}")
                return False, "LLM output contains harmful content"

        return True, "LLM output validated"

    def validate_decision(self, decision: dict) -> Tuple[bool, str]:
        """Validate claim decision for consistency"""

        status = decision.get("status", "").upper()
        reason = decision.get("reason", "").lower()

        # Status must be APPROVED, REJECTED, or REVIEW
        if status not in ["APPROVED", "REJECTED", "REVIEW"]:
            return False, f"Invalid decision status: {status}"

        # Must have a reason
        if not reason or len(reason) < 10:
            return False, "Decision must include a detailed reason"

        # APPROVED requires confidence
        if status == "APPROVED":
            confidence = decision.get("confidence", 0)
            if confidence < 0.6:
                return False, "APPROVED decisions require confidence >= 0.6"

        return True, "Decision validated"

# Singleton instance
_guardrails = None

def get_guardrails() -> SafetyGuardrails:
    global _guardrails
    if _guardrails is None:
        _guardrails = SafetyGuardrails()
    return _guardrails
