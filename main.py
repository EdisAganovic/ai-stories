"""
FastAPI backend za Generator priča za djecu

Ova aplikacija omogućava korisnicima da otpreme dječije crteže i generišu priče na bosanskom jeziku
koristeći OpenRouter API sa Polaris Alpha modelom.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import uuid
from typing import Optional
import base64
import openai

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from story_generator import validate_image_path, get_story_prompt

app = FastAPI(title="Children's Story Generator API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Create necessary directories if they don't exist
Path("uploads").mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main page for the web interface."""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


async def generate_story_with_gemini_api(image_data: bytes, mime_type: str, child_name: str, style: str, length: str) -> str:
    """Generate a story using the OpenRouter API (Polaris Alpha model) from in-memory image data."""
    try:
        # Configure OpenAI to use OpenRouter
        client = openai.AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )

        # Encode the image to base64 for the API call
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Create the prompt
        prompt = get_story_prompt(child_name, style, length, "the provided drawing")
        
        # Call the OpenRouter API with vision capabilities
        response = await client.chat.completions.create(
            model="openrouter/polaris-alpha",  # Using Polaris Alpha model through OpenRouter
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        
        return response.choices[0].message.content

    except Exception as e:
        raise e


@app.post("/generate-story/")
async def generate_story(
    image: UploadFile = File(...),
    child_name: str = Form(...),
    style: str = Form(...),
    length: str = Form(...)
):
    """Generate a story based on an uploaded image and user preferences."""
    # Validate inputs
    if not child_name.strip():
        raise HTTPException(status_code=400, detail="Child's name cannot be empty")

    if style not in ["fairy tale", "sci-fi", "adventure", "mystery", "comedy", "everyday life"]:
        raise HTTPException(status_code=400, detail="Invalid story style")

    if length not in ["short", "long"]:
        raise HTTPException(status_code=400, detail="Invalid story length")

    # Validate file type
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    # Define MIME types
    mime_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp'
    }

    mime_type = mime_type_map.get(file_extension)
    if not mime_type:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    try:
        # Read the image file content
        image_content = await image.read()

        # Generate the story using the API-compatible function
        story = await generate_story_with_gemini_api(image_content, mime_type, child_name, style, length)

        return {"story": story}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)