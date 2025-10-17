from pydantic import BaseModel, Field
from typing import Optional

class AnalysisRequest(BaseModel):
    """Schema for analysis request body."""
    video: str = Field(..., description="url of video (base64 encoded)")
    prompt: str = Field("Analyze this screen record and describe what you see in detail.", 
                       description="Prompt/instructions for the analysis")
    video_type: str = Field("url", description="Type of video (url or frame_list)")
    stream: bool = Field(False, description="Whether to stream the response")
    # backend: str = Field(..., description="Backend to use for analysis")
    # model: Optional[str] = Field(None, description="Specific model to use with the backend")

class AnalysisResponse(BaseModel):
    """Schema for analysis response."""
    analysis: str = Field(..., description="The analysis result")
    # backend: str = Field(..., description="Backend used for analysis")
    # model: Optional[str] = Field(None, description="Model used for analysis")
    # processing_time: Optional[float] = Field(None, description="Time taken for analysis in seconds")
