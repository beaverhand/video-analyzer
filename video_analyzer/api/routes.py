import base64
import io
from PIL import Image
from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import AnalysisRequest, AnalysisResponse
from fastapi.responses import StreamingResponse
from logger import GLOBAL_LOGGER as log
from client.openai import OpenAIClient
from utils.output_streams import event_stream
from utils.video import get_video_frames

router = APIRouter()
client = OpenAIClient()

@router.post("/analyze")
async def analyze(request: AnalysisRequest):
    """
    Analyze using the specified backend.
    
    Supports Qwen backend.
    """
    try:
        # Decode the base64 image
        try:
            video_path = request.video
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

        if request.stream:
            log.info("Calling LLM Client with streaming...")
            stream = client.invoke(video_path, request.prompt, stream=True)
            
            return StreamingResponse(
                event_stream(stream),
                media_type="text/event-stream",
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no'  # Disable buffering in nginx if used
                }
            )

        else:        
            log.info("Calling Qwen service with non-streaming...")
            analysis = client.invoke(video_path, request.prompt)
            return {
                "analysis": analysis,
            }
        
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Error processing analysis request")
        raise HTTPException(status_code=500, detail=str(e))