import asyncio
from sqlalchemy.orm import Session
from core import utils
from pipeline.utils.helpers import publish_update, handle_pipeline_error
from pipeline.steps.factual.wikisearch import factual_search_step
from pipeline.steps.factual.evaluation import evaluate_factual_claim
from db.models import Hypothesis, ValidationResult

async def start_factual_pipeline(hypothesis: Hypothesis, db: Session):
    """
    Orchestrates the factual hypothesis validation pipeline.
    """
    result = []
    comment = ""

    try:
        steps = [
            ("SearchingFact", "Search Wikipedia", factual_search_step),
            ("EvaluatingFact", "Evaluate factual claim", evaluate_factual_claim),
        ]

        for step, title, step_function in steps:
            # Publish status before step
            await publish_update(hypothesis, step, title)

            # Execute the step
            if step == "SearchingFact":
                result = await step_function(hypothesis)
                comment = f"Step '{title}' completed successfully."
            elif step == "EvaluatingFact":
                result = await step_function(hypothesis, result)
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
