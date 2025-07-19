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
    try:
        # Read the uploaded image file as bytes
        image_bytes = await image.read()
        mime_type = image.content_type  # e.g., "image/jpeg"

        # Load and format the prompt from file
        with open("prompts/caption_prompt.txt", "r", encoding="utf-8") as file:
            template = file.read()

        prompt = template.format(
            mood=mood,
            style=style,
            Country=country,
            language=language
        )

        # Call the Gemini service
        captions = await generate_caption(prompt, image_bytes, mime_type)

        return JSONResponse(content=captions)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))