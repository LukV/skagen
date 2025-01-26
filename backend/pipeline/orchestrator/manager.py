import asyncio
import logging
import os
from sqlalchemy.orm import Session
from pipeline.utils.helpers import publish_update, handle_pipeline_error
from pipeline.steps.common.nlu import extract_topic_terms
from pipeline.orchestrator.academic_pipeline import start_academic_pipeline
from pipeline.orchestrator.factual_pipeline import start_factual_pipeline
from pipeline.orchestrator.definitional_pipeline import start_definitional_pipeline
from pipeline.orchestrator.abstract_pipeline import start_abstract_pipeline
from db.models import Hypothesis

DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")
logger = logging.getLogger(__name__)

async def start_validation_pipeline(hypothesis_id: str, db: Session):
    """
    Routes to the appropriate pipeline based on the hypothesis query_type.
    """
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == hypothesis_id).first()

    if not hypothesis:
        raise ValueError(f"Hypothesis with ID {hypothesis_id} not found.")

    # Raise status
    hypothesis.status = "Processing"
    db.commit()

    try:
        step = "ExtractingTopics"
        title = "Extracting query"

        # Publish status before step
        await publish_update(hypothesis, step, title)

        # Execute the step
        result = await extract_topic_terms(hypothesis.content)
        hypothesis.extracted_topics = result["topics"]
        hypothesis.extracted_terms = result["keywords"]
        hypothesis.extracted_entities = result["named_entities"]
        hypothesis.query_type = result["query_type"]
        db.commit()

        comment = f"Extracted topics: {hypothesis.extracted_topics}"

        # Publish success
        await publish_update(hypothesis, step, title, comment=comment)

        # Check if query type is supported
        if hypothesis.query_type == "factual":
            await start_factual_pipeline(hypothesis, db)
        elif hypothesis.query_type == "definitional":
            await start_definitional_pipeline(hypothesis, db)
        elif hypothesis.query_type == "research-based":
            await start_academic_pipeline(hypothesis, db)
        elif hypothesis.query_type == "abstract":
            await start_abstract_pipeline(hypothesis, db)
        else:
            skip_msg = f"Skipped: Query type '{hypothesis.query_type}' not handled."
            logger.info(skip_msg)
            hypothesis.status = "Skipped"
            db.commit()

            await publish_update(hypothesis, step, title, error=skip_msg)
            return skip_msg


        # If we arrive here, it means extraction was done and, if relevant,
        # academic pipeline also completed successfully. Mark completed.
        # NOTE: If the academic pipeline sets a different status (e.g. "Failed"),
        # we do not overwrite it. So we check here first.
        if hypothesis.status not in ["Completed", "Failed", "Skipped"]:
            hypothesis.status = "Completed"
            db.commit()

        # Publish status before step
        await publish_update(hypothesis, "Finished", "Finished processing")

    except (asyncio.TimeoutError, ValueError, TypeError, RuntimeError) as e:
        await handle_pipeline_error(e, step, title, hypothesis, db, include_traceback=False)
        return

    except Exception as e: # pylint: disable=broad-except
        # Unknown errors
        await handle_pipeline_error(e, step, title, hypothesis, db, include_traceback=True)
        return

    finally:
        # Ensure final status isn't left in "Processing" if something got missed
        if hypothesis.status not in ["Completed", "Failed", "Skipped"]:
            hypothesis.status = "Failed"
            db.commit()
