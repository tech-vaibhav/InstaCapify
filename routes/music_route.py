from fastapi import APIRouter, HTTPException, Query
from services.spotify_service import get_tracks_by_mood

router = APIRouter()

@router.get("/music/recommend")
def recommend_music(mood: str = Query(..., example="chill")):
    try:
        tracks = get_tracks_by_mood(mood)
        return {"mood": mood, "songs": tracks}
    except Exception as e:
        return {"error": str(e)}