from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from src.logger import setup_logger
from typing import List, Tuple

logger = setup_logger(__name__)

class PIIDetectionMasking:
    def __init__(self):
        """Initialize Presidio for PII detection and masking"""
        logger.info("Initializing Presidio PII detection and anonymization")
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def detect_pii(self, text: str) -> List[dict]:
        """Detect PII entities in text"""
        results = self.analyzer.analyze(text=text, language="en")

        pii_entities = []
        for result in results:
            pii_entities.append({
                "entity_type": result.entity_type,
                "start": result.start,
                "end": result.end,
                "text": text[result.start:result.end],
                "score": result.score,
            })

        if pii_entities:
            logger.warning(f"Detected {len(pii_entities)} PII entities")

        return pii_entities

    def mask_pii(self, text: str) -> Tuple[str, List[dict]]:
        """Mask PII entities in text"""
        # First detect
        pii_entities = self.detect_pii(text)

        # Define masking operators
        operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE>"}),
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "<CREDIT_CARD>"}),
            "SSN": OperatorConfig("replace", {"new_value": "<SSN>"}),
            "DATE_TIME": OperatorConfig("replace", {"new_value": "<DATE>"}),
            "URL": OperatorConfig("replace", {"new_value": "<URL>"}),
        }

        # Anonymize
        anonymized_text = self.anonymizer.anonymize(
            text=text,
            analyzer_results=self.analyzer.analyze(text=text, language="en"),
            operators=operators
        )

        logger.info(f"Masked {len(pii_entities)} PII entities")
        return anonymized_text.text, pii_entities

    def is_pii_detected(self, text: str, threshold: float = 0.5) -> bool:
        """Check if PII is detected above threshold"""
        pii_entities = self.detect_pii(text)
        return any(entity["score"] >= threshold for entity in pii_entities)

# Singleton instance
_pii_detector = None

def get_pii_detector() -> PIIDetectionMasking:
    global _pii_detector
    if _pii_detector is None:
        _pii_detector = PIIDetectionMasking()
    return _pii_detector
