from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.spotify_service import get_tracks_by_mood
from services.db import get_db
from services.models import Post

router = APIRouter()

@router.get("/music/recommend")
async def recommend_music(
    post_id: int = Query(..., description="ID of the post to fetch mood from"),
    session: AsyncSession = Depends(get_db)
):
    # Fetch the post
    post = await session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    mood = post.normalized_mood
    try:
        tracks = get_tracks_by_mood(mood)
        return {
            "post_id": post_id,
            "raw_mood": post.raw_mood,
            "normalized_mood": mood,
            "songs": tracks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spotify error: {str(e)}")