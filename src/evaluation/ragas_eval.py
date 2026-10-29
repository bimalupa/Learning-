from ragas import evaluate
from ragas.metrics import faithfulness, context_relevancy
from datasets import Dataset
from src.logger import setup_logger
from typing import List, Dict
import json

logger = setup_logger(__name__)

class RAGASEvaluator:
    """RAGAS-based evaluation for RAG pipeline performance"""

    def __init__(self):
        self.metrics = [faithfulness, context_relevancy]
        logger.info("RAGAS evaluator initialized")

    def evaluate_retrieval(self, queries: List[str], retrieved_docs: List[List[str]],
                          ground_truth: List[str]) -> Dict:
        """
        Evaluate retrieval quality using RAGAS metrics

        Args:
            queries: List of query strings
            retrieved_docs: List of lists of retrieved document texts
            ground_truth: List of ground truth answers

        Returns:
            Dictionary with RAGAS metrics
        """

        try:
            # Prepare dataset
            dataset_dict = {
                "question": queries,
                "contexts": retrieved_docs,
                "ground_truth": ground_truth,
            }

            dataset = Dataset.from_dict(dataset_dict)

            logger.info(f"Evaluating retrieval with {len(queries)} queries")

            # Run evaluation
            results = evaluate(
                dataset,
                metrics=[context_relevancy]
            )

            evaluation_results = {
                "total_queries": len(queries),
                "context_relevancy": float(results["context_relevancy"]),
                "status": "success"
            }

            logger.info(f"Evaluation complete. Context relevancy: {evaluation_results['context_relevancy']}")
            return evaluation_results

        except Exception as e:
            logger.error(f"RAGAS evaluation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "total_queries": len(queries)
            }

    def evaluate_generation(self, questions: List[str], generated_texts: List[str],
                           contexts: List[List[str]], ground_truths: List[str]) -> Dict:
        """Evaluate generated text quality"""

        try:
            dataset_dict = {
                "question": questions,
                "answer": generated_texts,
                "contexts": contexts,
                "ground_truth": ground_truths,
            }

            dataset = Dataset.from_dict(dataset_dict)

            logger.info(f"Evaluating generation with {len(questions)} samples")

            results = evaluate(
                dataset,
                metrics=[faithfulness, context_relevancy]
            )

            evaluation_results = {
                "total_samples": len(questions),
                "faithfulness": float(results["faithfulness"]),
                "context_relevancy": float(results["context_relevancy"]),
                "status": "success"
            }

            logger.info(f"Generation evaluation complete. Faithfulness: {evaluation_results['faithfulness']}")
            return evaluation_results

        except Exception as e:
            logger.error(f"Generation evaluation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "total_samples": len(questions)
            }

    def log_evaluation_results(self, results: Dict, eval_type: str = "unknown"):
        """Log evaluation results"""
        logger.info(f"{eval_type} Evaluation Results:")
        logger.info(json.dumps(results, indent=2))

def get_evaluator() -> RAGASEvaluator:
    """Factory for evaluator"""
    return RAGASEvaluator()
