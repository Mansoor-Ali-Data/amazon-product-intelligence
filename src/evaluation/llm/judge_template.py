"""
Judge prompt template for LLM-as-a-Judge evaluation.

This prompt instructs the LLM to evaluate a generated answer
using a strict Retrieval-Augmented Generation (RAG) evaluation
rubric.

The judge must evaluate the answer conservatively and return
ONLY valid JSON.
"""

from __future__ import annotations

from string import Template


JUDGE_TEMPLATE = Template(
    """
You are an expert evaluator for Retrieval-Augmented Generation (RAG) systems.

Your task is NOT to answer the user's question.

Your task is ONLY to evaluate the quality of the generated answer using the
retrieved context and the reference answer.

Be objective, conservative, and strict.

────────────────────────────────────────
Evaluation Policy
────────────────────────────────────────

• Evaluate ONLY using the retrieved context and the reference answer.

• Do NOT use your own knowledge.

• Do NOT reward fluent writing.

• Do NOT reward plausible answers.

• Every factual statement in the generated answer must be explicitly
supported by the retrieved context.

• If the retrieved context does not contain enough information to answer
the question, the generated answer should receive a LOW correctness score.

• If the generated answer contains unsupported claims,
penalize Groundedness.

• If information required by the reference answer is missing,
penalize Answer Correctness.

• If the generated answer fails to answer the user's question,
penalize Answer Relevance.

• When uncertain, assign the LOWER score.

────────────────────────────────────────
Evaluation Metrics
────────────────────────────────────────

Score every metric between 0.0 and 1.0.

Groundedness
- Measures whether every factual claim in the generated answer
  is supported by the retrieved context.

Answer Relevance
- Measures whether the generated answer directly answers the
  user's question.

Semantic Similarity
- Measures how closely the generated answer matches the
  reference answer in meaning.

Answer Correctness
- Measures the factual correctness of the generated answer
  compared to the reference answer.

Confidence
- Estimate how confident you are in your own evaluation.

────────────────────────────────────────
User Question
────────────────────────────────────────

$user_query

────────────────────────────────────────
Retrieved Context
────────────────────────────────────────

$retrieved_context

────────────────────────────────────────
Reference Answer
────────────────────────────────────────

$ground_truth_answer

────────────────────────────────────────
Generated Answer
────────────────────────────────────────

$generated_answer

────────────────────────────────────────
Output Format
────────────────────────────────────────

Return ONLY valid JSON.

{
    "groundedness": 0.0,
    "answer_relevance": 0.0,
    "semantic_similarity": 0.0,
    "answer_correctness": 0.0,
    "confidence": 0.0,
    "evaluation_reason": "Briefly explain the evaluation and justify the assigned scores."
}

Do not include markdown.

Do not include explanations outside the JSON.

Do not include any additional fields.
""".strip()
)