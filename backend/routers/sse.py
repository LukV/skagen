import asyncio
import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from messaging.redis import AsyncRedisClient

router = APIRouter()
redis_client = AsyncRedisClient()

@router.get("/progress/{hypothesis_id}")
async def sse_progress(
    hypothesis_id: str,
    request: Request,
):
    """
    Streams the current pipeline status as Server-Sent Events (SSE).
    """
    pubsub = redis_client.redis.pubsub()
    await pubsub.subscribe("pipeline_updates")

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break

                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message["type"] == "message":
                    data = json.loads(message["data"])
                    if data["id"] == hypothesis_id:
                        yield f"data: {json.dumps(data)}\n\n"

                        # Disconnect the client if the pipeline is completed
                        if data["step"] in ["Completed"]:
                            break

                await asyncio.sleep(0.1)
        finally:
            await redis_client.unsubscribe(pubsub, "pipeline_updates")

    return StreamingResponse(event_generator(), media_type="text/event-stream")
