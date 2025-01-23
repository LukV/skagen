import json
import logging
import time
import traceback
from sqlalchemy.orm import Session
from messaging.redis import AsyncRedisClient
from db.models import Hypothesis

logger = logging.getLogger(__name__)
redis_client = AsyncRedisClient()

async def publish_update(
    hypothesis: Hypothesis,
    step: str,
    title: str,
    comment: str = None,
    error: str = None
):
    """
    Helper to publish pipeline updates to Redis.
    """
    message = {
        "id": hypothesis.id,
        "step": step,
        "title": title,
        "time": time.time()
    }
    if comment:
        message["comment"] = comment
    if error:
        message["error"] = error

    await redis_client.publish("pipeline_updates", json.dumps(message))


async def handle_pipeline_error(
    e: Exception,
    step: str,
    title: str,
    hypothesis: Hypothesis,
    db: Session,
    include_traceback: bool = False
):
    """
    Centralized error handling:
      - logs the error
      - sets hypothesis.status = "Failed"
      - commits the DB session
      - publishes error to Redis
    """
    error_type = type(e).__name__
    error_traceback = traceback.format_exc() if include_traceback else ""

    logger.error(
        "Error in step %s for hypothesis %s [%s]: %s\nTraceback:\n%s",
        step,
        hypothesis.id,
        error_type,
        e,
        error_traceback
    )
    hypothesis.status = "Failed"
    db.commit()

    # Publish the error message
    await publish_update(
        hypothesis=hypothesis,
        step=step,
        title=title,
        error=f"An error occurred: {error_type}"
    )
