from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.caption_route import router as caption_router
from routes import music_route
from services.db import engine, Base
from services.models import Post

app = FastAPI(
    title="InstaCapify - AI Instagram Caption Generator",
    description="Generate Instagram-style captions using Google Gemini and AI magic!",
    version="1.0.0"
)

# Register caption generation routes
app.include_router(caption_router, prefix="/api/caption")
app.include_router(music_route.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )