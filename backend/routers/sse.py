import asyncio
import json

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from db.database import get_db
from crud.hypothesises import get_hypothesis_by_id

router = APIRouter()

@router.get("/progress/{hypothesis_id}")
async def sse_progress(
    hypothesis_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Streams the current pipeline status as Server-Sent Events (SSE).
    The client will keep this connection open to get real-time updates.
    """

    # Check that hypothesis exists
    hypothesis = get_hypothesis_by_id(db, hypothesis_id)
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")

    async def event_generator():
        # Keep streaming until pipeline is done OR client disconnects
        while True:
            # 1. Check if client disconnected
            if await request.is_disconnected():
                print("Client disconnected")
                break

            # 2. Reload hypothesis from DB to get fresh status
            db.refresh(hypothesis)
            current_status = hypothesis.status  # e.g. "ExtractingTopicTerms", "Completed", etc.

            # 3. Yield an SSE message
            payload = {
                "status": current_status
            }
            yield f"data: {json.dumps(payload)}\n\n"

            # 4. If the pipeline is done or failed, exit
            if current_status in ("Completed", "Failed", "Skipped"):
                break

            # 5. Sleep a bit to avoid busy-looping
            await asyncio.sleep(1)

    # Return a streaming response with the above generator
    return StreamingResponse(event_generator(), media_type="text/event-stream")
