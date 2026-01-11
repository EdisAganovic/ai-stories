"""
FastAPI pozadinska aplikacija za Generator priča za djecu.

Ova aplikacija omogućava korisnicima da otpreme dječje crteže i generiraju priče na bosanskom jeziku
koristeći Google Gemini API.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import sys
import io
from typing import Optional

from google import genai
from PIL import Image
import base64
import json
import webbrowser
import threading
import time
from pydantic import BaseModel

# Učitavanje varijabli okruženja iz .env datoteke
from dotenv import load_dotenv
load_dotenv()

# Globalna inicijalizacija Gemini klijenta
# NAPOMENA: Klijent se sada inicijalizira po zahtjevu korisnika (BYOK)
client = None

# --- KONFIGURACIJA ---
def get_exe_dir():
    """Vraća direktorij gdje se nalazi izvršna datoteka (exe)."""
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")

CONFIG_FILE = os.path.join(get_exe_dir(), "config.json")

class Settings(BaseModel):
    api_key: Optional[str] = None
    custom_prompt: Optional[str] = None
    gemini_model: str = "gemini-flash-latest"
    temperature: float = 1.0

def load_settings() -> Settings:
    """Učitava postavke iz config.json datoteke."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Settings(**data)
        except Exception as e:
            print(f"Greška prilikom učitavanja konfiguracije: {e}")
    return Settings()

def save_settings(settings: Settings):
    """Sprema postavke u config.json datoteku."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(settings.model_dump_json())
    except Exception as e:
        print(f"Greška prilikom spremanja konfiguracije: {e}")



def get_prompt_variables(child_name: str, style: str, length: str, image_description: str) -> dict:
    """Prepare variables for the story prompt."""
    # Map English style names to Bosnian equivalents for use in the prompt
    style_mapping = {
        "fairy tale": "basna",
        "sci-fi": "naučna fantastika",
        "adventure": "pustolovina",
        "mystery": "misterija",
        "comedy": "komedija",
        "everyday life": "svakodnevni život"
    }
    
    bosnian_style = style_mapping.get(style, style)
    
    # Length description is already in Bosnian
    length_description = "5 paragrafa" if length == "short" else "10 paragrafa"

    return {
        "child_name": child_name,
        "style": bosnian_style,
        "length": length_description,
        "image_description": image_description
    }

DEFAULT_PROMPT_TEMPLATE = """Napiši maštovitu i zanimljivu priču na bosanskom jeziku za dijete po imenu {child_name} na osnovu priloženog crteža: {image_description}.

Priča treba biti u stilu {style} i sadržavati otprilike {length}.
Pobrini se da priča bude primjerena uzrastu djeteta, zabavna i da uključuje elemente koji se mogu vidjeti na crtežu.
Glavni lik priče treba biti {child_name} ili priča treba povezati crtež sa avanturom koju {child_name} doživljava.

Započni priču sa: "Jednom davno, {child_name} je otkrio/la..."
Za stil basne možeš započeti sa: "Priča se događa u jednom dalekom carstvu gdje živi..."
Završi priču sa: "...i tako se završila izuzetna avantura koju je doživio/la {child_name}!"

Učini priču kreativnom, pozitivnom i primjerenom za djecu. Sav tekst mora biti na bosanskom jeziku."""


app = FastAPI(title="API za Generator priča za djecu")

# --- KONFIGURACIJA PUTEVA ZA PYINSTALLER ---
def get_resource_path(relative_path):
    """Vraća apsolutni put do resursa, radi za razvoj i za PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

static_dir = get_resource_path("static")
templates_dir = get_resource_path("templates")

# Provjera postojanja direktorija resursa
if not os.path.exists(static_dir):
    print(f"WARNING: Static direktorij nije pronađen na: {static_dir}")
if not os.path.exists(templates_dir):
    print(f"WARNING: Templates direktorij nije pronađen na: {templates_dir}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Prikazuje glavnu stranicu web interfejsa."""
    return templates.TemplateResponse("index.html", {"request": request})

# Povezivanje statičkih datoteka
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Postavljanje šablona (templates)
templates = Jinja2Templates(directory=templates_dir)


async def generate_story_with_gemini_api(
    image_data: bytes, 
    child_name: str, 
    style: str, 
    length: str,
    api_key: Optional[str] = None,
    custom_prompt: Optional[str] = None,
    gemini_model: str = "gemini-flash-latest",
    temperature: float = 1.0
) -> tuple[str, dict]:
    """Generira priču koristeći Google Gemini API i vraća tekst i metapodatke o korištenju."""
    try:
        # Determine which client to use
        current_client = None
        if api_key and api_key.strip():
            current_client = genai.Client(api_key=api_key)
        else:
            current_client = client

        if not current_client:
            raise ValueError("API ključ je obavezan. Molimo unesite svoj Google Gemini API ključ u postavkama.")

        # Prepare variables
        variables = get_prompt_variables(child_name, style, length, "priloženog crteža")

        # Determine prompt
        if custom_prompt and custom_prompt.strip():
            try:
                # Use safe formatting or just format. 
                # Using standard format, but we should be careful if user puts extra braces.
                # For simplicity, we assume user knows what they are doing with {keys}.
                prompt = custom_prompt.format(**variables)
            except KeyError as e:
                # Fallback or error? Let's error clearly.
                raise ValueError(f"Greška u formatu šablona: Nedostaje varijabla {e}")
            except Exception as e:
                raise ValueError(f"Greška prilikom formatiranja šablona: {e}")
        else:
            prompt = DEFAULT_PROMPT_TEMPLATE.format(**variables)
        
        # Učitavanje slike iz bajtova
        image_file = io.BytesIO(image_data)
        img = Image.open(image_file)
        
        # Generiranje sadržaja pomoću novog API-ja
        # Koristimo run_in_executor jer je genai poziv sinhron
        from fastapi.concurrency import run_in_threadpool
        
        response = await run_in_threadpool(
            current_client.models.generate_content,
            model=gemini_model,
            contents=[prompt, img],
            config={'temperature': temperature}
        )
        
        # Ekstrakcija metapodataka o tokenima
        usage_metadata = {
            "prompt_token_count": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
            "candidates_token_count": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
            "total_token_count": response.usage_metadata.total_token_count if response.usage_metadata else 0
        }
        
        return response.text, usage_metadata

    except Exception as e:
        # Proslijeđuje izuzetak da se obradi na višem nivou
        raise e


@app.post("/generate-story/")
async def generate_story(
    image: UploadFile = File(...),
    child_name: str = Form(...),
    style: str = Form(...),
    length: str = Form(...),
    api_key: Optional[str] = Form(None),
    custom_prompt: Optional[str] = Form(None),
    gemini_model: Optional[str] = Form(None),
    temperature: Optional[float] = Form(None)
):
    """Generira priču na osnovu otpremljene slike i korisničkih postavki."""
    # Validacija ulaznih podataka
    if not child_name.strip():
        raise HTTPException(status_code=400, detail="Ime djeteta ne može biti prazno.")

    valid_styles = ["fairy tale", "sci-fi", "adventure", "mystery", "comedy", "everyday life"]
    if style not in valid_styles:
        raise HTTPException(status_code=400, detail="Nevažeći stil priče.")

    if length not in ["short", "long"]:
        raise HTTPException(status_code=400, detail="Nevažeća dužina priče.")

    # Validacija tipa datoteke
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
        raise HTTPException(status_code=400, detail="Nepodržan format slike.")

    # Definisanje MIME tipova
    mime_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp'
    }

    mime_type = mime_type_map.get(file_extension)
    if not mime_type:
        raise HTTPException(status_code=400, detail="Nepodržan format slike.")

    try:
        # Čitanje sadržaja slikovne datoteke
        image_content = await image.read()

        # Generiranje priče pomoću API funkcije
        story, usage = await generate_story_with_gemini_api(
            image_content, 
            child_name, 
            style, 
            length, 
            api_key=api_key, 
            custom_prompt=custom_prompt,
            gemini_model=gemini_model or "gemini-flash-latest",
            temperature=temperature if temperature is not None else 1.0
        )

        # Encode image to base64 for frontend display
        image_base64 = base64.b64encode(image_content).decode('utf-8')

        return {
            "story": story,
            "image_base64": image_base64,
            "mime_type": mime_type,
            "usage": usage
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška prilikom generiranja priče: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Endpoint za provjeru statusa aplikacije (health check)."""
    return {"status": "ok"}

    return {"status": "ok"}


@app.get("/api/settings", response_model=Settings)
async def get_settings():
    """Vraća trenutne postavke."""
    return load_settings()


@app.post("/api/settings")
async def update_settings(settings: Settings):
    """Ažurira postavke."""
    save_settings(settings)
    return {"status": "success", "message": "Postavke spremljene"}


def open_browser():
    """Otvara web pretraživač nakon kratkog čekanja."""
    url = "http://localhost:8000"
    time.sleep(1.5)  # Čekamo da se server pokrene
    print(f"Otvaram pretraživač na: {url}")
    print(f"Ako se pretraživač ne otvori automatski, posjetite: {url}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Ne mogu automatski otvoriti pretraživač: {e}")


if __name__ == "__main__":
    import uvicorn
    
    # Pokreni otvaranje pretraživača u zasebnoj dretvi
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)