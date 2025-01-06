import json
import logging
import os
from sqlalchemy.orm import Session
from pipeline.steps.nlu import extract_topic_terms
from pipeline.steps.academic_search import perform_academic_search
from pipeline.steps.ranking import rank_search_results
from pipeline.steps.summarization import summarize_results
from db.models import Hypothesis

DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")

logger = logging.getLogger(__name__)

async def start_validation_pipeline(hypothesis_id: str, db: Session):
    """
    Orchestrates the hypothesis validation pipeline.

    Args:
        hypothesis_id (str): The ID of the hypothesis.
        db (Session): The database session.

    Returns:
        None
    """
    # Step 1: Fetch the hypothesis
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == hypothesis_id).first()
    if not hypothesis:
        raise ValueError(f"Hypothesis with ID {hypothesis_id} not found.")

    try:

        # Step 2: Natural Language Understanding (NLU)
        nlu_result = await extract_topic_terms(str(hypothesis.content))
        hypothesis.status = "Processing" # type: ignore
        hypothesis.extracted_topics = nlu_result["topics"]
        hypothesis.extracted_terms = nlu_result["keywords"]
        hypothesis.extracted_entities = nlu_result["named_entities"]
        hypothesis.query_type = nlu_result["query_type"]

        db.commit()

        # Step 3: TODO: Check if the query is plausible / filter out harmful queries
        if hypothesis.query_type != "research-based":
            hypothesis.status = "Skipped"  # Mark as skipped for unsupported types
            db.commit()
            return f"Skipped: Query type '{hypothesis.query_type}' not handled."

        # Step 4: Academic Search
        search_results = await perform_academic_search(
            hypothesis, 
            excludeFulltext=True
        )
        if DEBUG_MODE:
            output_file = "../debug/search_results.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure the directory exists
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(search_results, f, ensure_ascii=False, indent=4)

        # Store or cache search results in the database (implementation omitted)

        # Step 5: Similarity ranking
        ranked_results = await rank_search_results(
            hypothesis.content,
            search_results,
            top_n=10
        )
        if DEBUG_MODE:
            output_file = "../debug/ranked_results.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure the directory exists
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(ranked_results, f, ensure_ascii=False, indent=4)


        # Step 6: Summarization (placeholder for now)
        summary = await summarize_results(search_results)
        # Store summary in the database or update hypothesis
        hypothesis.status = "Completed" # type: ignore
        db.commit()

        return summary
    except (ValueError, TypeError, RuntimeError) as e:
        # Handle errors and mark hypothesis as failed
        logger.error("Error during pipeline execution for hypothesis %s: %s", hypothesis_id, e)
        hypothesis.status = "Failed" # type: ignore
        db.commit()
