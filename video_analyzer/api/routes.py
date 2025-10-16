import asyncio
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from screen_analysis.logger import GLOBAL_LOGGER as log
from utils.output_streams import event_stream

router = APIRouter()

@router.post("/analyze")
async def analyze_image(request: AnalysisRequest):
    """
    Analyze an image using the specified backend.
    
    Supports FastVLM backend.
    """
    try:
        # Decode the base64 image
        try:
            image_data = base64.b64decode(request.image)
            image = Image.open(io.BytesIO(image_data))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

        if request.stream:
            log.info("Calling FastVLM service with streaming...")
            stream = fast_vlm_service.analyze_image(image, request.prompt, stream=True)
            
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
            analysis = fast_vlm_service.analyze_image(image, request.prompt)
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
        
        # Use the standard analysis endpoint
        analysis_request = AnalysisRequest(
            image=img_str,
            prompt=prompt,
        )
        
        return await analyze_image(analysis_request)
        
    except Exception as e:
        logger.exception("Error processing file upload")
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
