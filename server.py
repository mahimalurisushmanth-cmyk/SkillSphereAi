from __future__ import annotations
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pathlib import Path
import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="SkillSphere AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"]
)

class AIRequest(BaseModel):
    message: str = Field(min_length=1, max_length=6000)
    career: str = "AI / ML Engineer"
    level: str = "Beginner"
    goal: str = "Build AI projects and prepare for internships"

@app.get("/api/health")
async def health():
    return {"ok": True, "service": "SkillSphere AI", "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))}

@app.post("/api/ai")
async def ask_ai(body: AIRequest):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not set on the server. Configure it and restart the backend.")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    prompt = f"""You are SkillSphere AI, a supportive AI learning and career mentor for students.
Student context:
- Target career: {body.career}
- Current level: {body.level}
- Goal: {body.goal}
Answer the student's question with clear, practical, appropriately scoped steps.
Do not claim to have checked live news or course freshness unless live source data was provided.
For changing technical details, encourage checking official documentation. Do not guarantee employment.
Student question: {body.message}"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                url,
                headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": prompt}]}],
                      "generationConfig": {"temperature": 0.5, "maxOutputTokens": 1200}}
            )
        if response.status_code >= 400:
            # Avoid returning provider payloads that might include operational details.
            raise HTTPException(status_code=502, detail=f"Gemini API returned HTTP {response.status_code}. Check model availability, API key restrictions, quota, and server logs.")
        payload = response.json()
        parts = payload.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        reply = "\n".join(p.get("text", "") for p in parts if p.get("text"))
        if not reply:
            raise HTTPException(status_code=502, detail="Gemini returned no text. Try a shorter prompt.")
        return {"reply": reply, "model": model, "provider": "Gemini API"}
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Gemini request timed out. Please retry.")
    except Exception:
        raise HTTPException(status_code=502, detail="Could not complete the Gemini request. Check backend logs and network access.")

@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "index.html")

# Serve only when this file is run as a module from the project backend folder.
app.mount("/assets", StaticFiles(directory=BASE_DIR), name="assets")
