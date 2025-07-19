import os
import json
import traceback
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from services.gemini_service import generate_caption

router = APIRouter()

@router.post("/generate-caption")
async def generate_caption_endpoint(
    mood: str = Form(...),
    style: str = Form(...),
    country: str = Form(...),
    language: str = Form(...),
    image: UploadFile = File(...)
):
    print("📩 Caption endpoint hit")

    # Load and format prompt
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/caption_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_template = file.read()
            print("📄 Prompt loaded")
    except Exception as e:
        print("❌ Failed to read prompt file:", e)
        raise HTTPException(status_code=500, detail="Prompt template not found")

    prompt = prompt_template.format(
        mood=mood,
        style=style,
        Country=country,
        language=language
    )
    print("🧠 Final prompt:\n", prompt)

    image_bytes = await image.read()
    mime_type = image.content_type

    try:
        response = await generate_caption(prompt, image_bytes, mime_type)
        return {"captions": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
