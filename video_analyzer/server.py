import uvicorn
from video_analyzer.main import app

if __name__ == "__main__":
    uvicorn.run(
        "video_analyzer.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["video_analyzer"],
        reload_excludes=["*.pyc", "*.pyo", "*~"],
        log_level="info"
    )
