from fastapi import FastAPI
from routes.caption_route import router as caption_router

app = FastAPI(
    title="InstaCapify - AI Instagram Caption Generator",
    description="Generate Instagram-style captions using Google Gemini and AI magic!",
    version="1.0.0"
)

# Register caption generation routes
app.include_router(caption_router, prefix="/api/caption")
