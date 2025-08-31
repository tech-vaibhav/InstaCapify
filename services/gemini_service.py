import os
import json
import re
import traceback
from google import genai
from google.genai import types
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()
# Initialize Gemini client with API key
api_key = os.getenv("GEMINI_API_KEY")
print("🔑 Loaded API Key:", api_key)
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

client = genai.Client(api_key=api_key)

# Function to generate a caption using image and prompt
async def generate_caption(prompt: str, image_bytes: bytes, mime_type: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {"role": "user", "parts": [{"text": prompt}]},
                {
                    "role": "user",
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_bytes
                            }
                        }
                    ]
                }
            ],
            config=types.GenerateContentConfig(
                # Optional: you can configure temperature, etc.
                temperature=0.7,
                thinking_config=types.ThinkingConfig(thinking_budget=0)  # Optional
            )
        )
        
        print("=== RAW GEMINI RESPONSE ===")
        print(response.text)
        
        clean_text = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.MULTILINE).strip()
        
        return json.loads(clean_text)
        # Try parsing Gemini response as JSON
        
    except json.JSONDecodeError as e:
        print("❌ JSON parse failed:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Gemini returned an invalid JSON response: {e}"
        )
    except Exception as e:
        print("❌ Gemini API error occurred:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")