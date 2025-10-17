import asyncio
import base64
import io
import json
from PIL import Image
from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import AnalysisRequest, AnalysisResponse
from fastapi.responses import StreamingResponse
from logger import GLOBAL_LOGGER as log
# from client.local import LocalClient
from client.openai import OpenAIClient
from utils.output_streams import event_stream

router = APIRouter()
# client = LocalClient()
client = OpenAIClient()

@router.post("/analyze")
async def analyze(request: AnalysisRequest):
    """
    Analyze an image using the specified backend.
    
    Supports FastVLM backend.
    """
    try:
        # Decode the base64 image
        try:
            video_data = base64.b64decode(request.video)
            video = Image.open(io.BytesIO(video_data))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

        if request.stream:
            log.info("Calling LLM Client with streaming...")
            stream = client.invoke(video, request.prompt, stream=True)
            
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
            log.info("Calling FastVLM service with non-streaming...")
            analysis = client.invoke(video, request.prompt)
            return {
                "analysis": analysis,
            }
        
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Error processing analysis request")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/file", response_model=AnalysisResponse)
async def analyze_image_file(
    file: UploadFile = File(...),
    prompt: str = "Analyze this screen capture and describe what you see in detail.",
):
    """
    Alternative endpoint that accepts an image file upload instead of base64.
    """
    try:
        # Read and validate the uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Convert to base64 for the standard analysis flow
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        log.info("Image converted to base64")
        
        # Use the standard analysis endpoint
        analysis_request = AnalysisRequest(
            video=img_str,
            prompt=prompt,
        )
        log.info("Analysis request created")
        return await analyze(analysis_request)
        
    except Exception as e:
        log.error(str(e))
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
