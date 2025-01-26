import asyncio
import logging
from sqlalchemy.orm import Session
from pipeline.utils.helpers import publish_update, handle_pipeline_error
from db.models import Hypothesis

logger = logging.getLogger(__name__)

async def start_definitional_pipeline(hypothesis: Hypothesis, db: Session):
    """
    Orchestrates the definitional hypothesis validation pipeline.
    """
    result = []
    comment = ""

    try:
        steps = [
            ("SearchingFact", "Perform web search", perform_web_search),
            ("EvaluatingFact", "Evaluate definitional claim", evaluate_definitional_claim),
        ]

        for step, title, step_function in steps:
            # Publish status before step
            await publish_update(hypothesis, step, title)

            # Execute the step
            result = await step_function(hypothesis, db)
            comment = f"Step '{title}' completed successfully."

            # Publish completion for this step
            await publish_update(hypothesis, step, title, comment=comment)

        # Mark pipeline as completed
        hypothesis.status = "Completed"
        db.commit()

    except (asyncio.TimeoutError, ValueError, TypeError, RuntimeError) as e:
        await handle_pipeline_error(e, step, title, hypothesis, db, include_traceback=False)
        return

    except Exception as e:  # pylint: disable=broad-except
        await handle_pipeline_error(e, step, title, hypothesis, db, include_traceback=True)
        return

    finally:
        if hypothesis.status not in ["Completed", "Failed", "Skipped"]:
            hypothesis.status = "Failed"
            db.commit()


async def perform_web_search(hypothesis: Hypothesis, db: Session):
    """
    Example step: Perform a definitional search.
    Replace this with actual implementation.
    """
    # Mock implementation: Replace with definitional search logic
    logger.info(f"Performing web search for: {hypothesis.content}")
    return [{"fact": "Example fact"}]


async def evaluate_definitional_claim(hypothesis: Hypothesis, db: Session):
    """
    Example step: Evaluate the definitional claim.
    Replace this with actual implementation.
    """
    # Mock implementation: Replace with definitional evaluation logic
    logger.info(f"Evaluating definitional claim for: {hypothesis.content}")
    return {"classification": "Verified", "details": "The claim is definitional."}