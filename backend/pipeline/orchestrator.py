import asyncio
import json
import logging
import time
import os
import traceback
from sqlalchemy.orm import Session
from messaging.redis import AsyncRedisClient
from pipeline.steps.nlu import extract_topic_terms
from pipeline.steps.academic_search import perform_academic_search
from pipeline.steps.ranking import rank_search_results
from pipeline.steps.summarization import summarize_abstracts
from pipeline.steps.evaluation import evaluate_hypothesis
from db.models import Hypothesis, ValidationResult
from core import utils

DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")

logger = logging.getLogger(__name__)
redis_client = AsyncRedisClient()

async def start_validation_pipeline(hypothesis_id: str, db: Session):
    """
    Orchestrates the hypothesis validation pipeline.

    Args:
        hypothesis_id (str): The ID of the hypothesis.
        db (Session): The database session.

    Returns:
        None
    """
    comment = ""

    # Step 1: Fetch the hypothesis
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == hypothesis_id).first()

    if not hypothesis:
        raise ValueError(f"Hypothesis with ID {hypothesis_id} not found.")

    # Raise status
    hypothesis.status = "Processing"
    db.commit()

    try:
        steps = [
            ("ExtractingTopics", "Extracting query", extract_topic_terms),
            ("PerformingAcademicSearch", "Search CORE database", perform_academic_search),
            ("RankingSearchResults", "Similarity ranking", rank_search_results),
            ("SummarizingResults", "Summerization", summarize_abstracts),
            ("EvaluatingHypothesis", "Evaluating hypothesis", evaluate_hypothesis),
        ]

        for step, title, step_function in steps:
            # Publish status before executing the step
            await redis_client.publish(
                "pipeline_updates",
                json.dumps({
                    "id": hypothesis_id, 
                    "step": step, 
                    "title": title, 
                    "time": time.time()
                })
            )
            await asyncio.sleep(0)  # Yield control to the event loop

            # Execute the step
            if step == "ExtractingTopics":
                result = await step_function(hypothesis.content)
                hypothesis.extracted_topics = result["topics"]
                hypothesis.extracted_terms = result["keywords"]
                hypothesis.extracted_entities = result["named_entities"]
                hypothesis.query_type = result["query_type"]
                db.commit()
                comment = f"Extracted topics: {hypothesis.extracted_topics}"
                
                # Check if query type is supported
                if hypothesis.query_type != "research-based":
                    await redis_client.publish(
                        "pipeline_updates",
                        json.dumps({
                            "id": hypothesis_id,
                            "step": step,
                            "title": title,
                            "error": f"Skipped: Query type '{hypothesis.query_type}' not handled.",
                            "time": time.time()
                        })
                    )
                    hypothesis.status = "Skipped"
                    db.commit()
                    return f"Skipped: Query type '{hypothesis.query_type}' not handled."

            elif step == "PerformingAcademicSearch":
                result = await step_function(hypothesis, db, exclude_fulltext=False)
                comment = f": {len(result)} results"

            elif step == "RankingSearchResults":
                result = await step_function(hypothesis.content, result, top_n=10)
                similarities = [item["similarity"] for item in result]
                highest = round(max(similarities), 2)
                lowest = round(min(similarities), 2)
                comment = f"scores between {lowest} and {highest}." # pylint: disable=C0301

                if DEBUG_MODE:
                    output_file = "../debug/ranked_results.json"
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=4)

            elif step == "SummarizingResults":
                max_results = 6
                threshold = 0.2
                result = [
                    item for item in result if item.get("similarity", 0) > threshold
                ][:max_results]

                if not result:
                    hypothesis.status = "InsufficientSources"
                    db.commit()
                    return "No valid results above the threshold were found."

                result = await step_function(result, db)
                comment = " successful."

            elif step == "EvaluatingHypothesis":
                result = await step_function(result, hypothesis)

                validation_result = ValidationResult(
                    id=utils.generate_id('V'),
                    hypothesis_id=hypothesis.id,
                    classification=result.get("classification"),
                    motivation=result.get("motivation"),
                    sources=result.get("sources", [])
                )
                db.add(validation_result)
                db.commit()
                db.refresh(validation_result)

                comment=" successful."

            # Publish result after executing the step
            await redis_client.publish(
                "pipeline_updates",
                json.dumps({
                    "id": hypothesis_id, 
                    "step": step, 
                    "title": title,
                    "comment": comment, 
                    "time": time.time()
                })
            )
            await asyncio.sleep(0)  # Yield control to the event loop

        # Mark pipeline as completed
        hypothesis.status = "Completed"
        db.commit()

    except (asyncio.TimeoutError, ValueError, TypeError, RuntimeError) as e:
        # Handle errors and mark hypothesis as failed
        error_type = type(e).__name__
    
        # Log the error with its type
        logger.error("Error in step %s for hypothesis %s [%s]: %s", step, hypothesis_id, error_type, e)
        hypothesis.status = "Failed"
        db.commit()
        await redis_client.publish(
            "pipeline_updates",
            json.dumps({
                "id": hypothesis_id,
                "step": step,
                "title": title,
                "error": f"An error occured: {str(error_type)}",
                "time": time.time()
            })
        )
        return
    
    except Exception as e: # pylint: disable=W0718
        error_type = type(e).__name__
        error_traceback = traceback.format_exc()
        
        # Log the error with its type and traceback
        logger.error(
            "Error in step %s for hypothesis %s [%s]: %s\nTraceback:\n%s",
            step,
            hypothesis_id,
            error_type,
            e,
            error_traceback
        )
        hypothesis.status = "Failed"
        db.commit()
        await redis_client.publish(
            "pipeline_updates",
            json.dumps({
                "id": hypothesis_id,
                "step": step,
                "title": title,
                "error": f"An error occured: {str(error_type)}",
                "time": time.time()
            })
        )
        return
    
    finally:
        # Ensure status is updated appropriately
        if hypothesis.status not in ["Completed", "Failed", "Skipped"]:
            hypothesis.status = "Failed"
            db.commit()

