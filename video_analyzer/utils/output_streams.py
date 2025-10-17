import asyncio
import json

async def event_stream(stream):
    try:
        for text_chunk in stream:
            # Send each chunk as an SSE event
            # print(text_chunk, flush=True, end="")
            data = {
                "analysis": text_chunk,
            }
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(0)  # Allow other tasks to run
    except Exception as e:
        error_data = {
            "error": str(e),
        }
        yield f"data: {json.dumps(error_data)}\n\n"