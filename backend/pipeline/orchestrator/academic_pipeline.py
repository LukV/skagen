import asyncio
import json
import logging
import os
from sqlalchemy.orm import Session
from pipeline.utils.helpers import publish_update, handle_pipeline_error
from pipeline.steps.academic.academic_search import perform_academic_search
from pipeline.steps.academic.ranking import rank_search_results
from pipeline.steps.academic.summarization import summarize_abstracts
from pipeline.steps.academic.evaluation import evaluate_hypothesis
from db.models import Hypothesis, ValidationResult
from core import utils

DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")
logger = logging.getLogger(__name__)

async def start_academic_pipeline(hypothesis: Hypothesis, db: Session):
    """
    Orchestrates the academic hypothesis validation pipeline.
    """
    result = []
    comment = ""

    try:
        steps = [
            ("PerformingAcademicSearch", "Search CORE database", perform_academic_search),
            ("RankingSearchResults", "Similarity Ranking", rank_search_results),
            ("SummarizingResults", "Summarization", summarize_abstracts),
            ("EvaluatingHypothesis", "Evaluating Hypothesis", evaluate_hypothesis),
        ]

        for step, title, step_function in steps:
            # Publish status before step
            await publish_update(hypothesis, step, title)

            # Execute the step
            if step == "PerformingAcademicSearch":
                result = await step_function(hypothesis, db, exclude_fulltext=False)
                comment = f"{len(result)} results found."

            elif step == "RankingSearchResults":
                result = await step_function(hypothesis.content, result, top_n=10)
                similarities = [item["similarity"] for item in result]
                highest = round(max(similarities), 2)
                lowest = round(min(similarities), 2)
                comment = f"Scores range {lowest} to {highest}"

                if DEBUG_MODE:
                    output_file = "../debug/ranked_results.json"
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=4)

            elif step == "SummarizingResults":
                max_results = 6
                threshold = 0.2
                # Filter out low-similarity items
                result = [
                    item for item in result if item.get("similarity", 0) > threshold
                ][:max_results]

                if not result:
                    hypothesis.status = "InsufficientSources"
                    db.commit()
                    return "No valid results above the threshold were found."

                result = await step_function(result, db)
                comment = "Summaries generated."

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

                comment = "Evaluation complete."

            # Publish completion for this step
            await publish_update(hypothesis, step, title, comment=comment)

        # Mark pipeline as completed
        hypothesis.status = "Completed"
        db.commit()

    except (asyncio.TimeoutError, ValueError, TypeError, RuntimeError) as e:
        await handle_pipeline_error(e, step, title, hypothesis, db, include_traceback=False)
        return

    except Exception as e: # pylint: disable=broad-except
        await handle_pipeline_error(e, step, title, hypothesis, db, include_traceback=True)
        return

    finally:
        if hypothesis.status not in ["Completed", "Failed", "Skipped", "InsufficientSources"]:
            hypothesis.status = "Failed"
            db.commit()
