from fastapi import FastAPI
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base
from app import models
from app.routers import voice_analysis, mood_entries,text_analysis,reflection,chat
from app.background_tasks import check_and_prompt_24hr_reflections

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Mental Wellness Mirror",
    description=(
        "A GenAI-powered emotional reflection platform that helps users "
        "analyze journal entries or voice logs, track emotional changes, "
        "and build resilience through mindful reflection."
    ),
    version="1.0.0"
)

# Enable CORS for development (adjust allowed_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(text_analysis.router, prefix="/analyze", tags=["Text Analysis"])
app.include_router(voice_analysis.router, prefix="/analyze", tags=["Voice Analysis"])
app.include_router(reflection.router, prefix="/reflect", tags=["Reflections"])
app.include_router(mood_entries.router, prefix="/mood", tags=["Mood Entries"])
app.include_router(chat.router, prefix="/chat", tags=["Chat Reflection"])

# Background reflection task
@app.on_event("startup")
async def startup_event():
    """Start background task for reflection reminders"""
    asyncio.create_task(check_and_prompt_24hr_reflections())

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Mental Wellness Mirror API 🌱",
        "description": "Empower users to reflect, analyze, and improve their emotional well-being.",
        "available_endpoints": {
            "Login/Register": "/auth",
            "Analyze Voice Emotion": "POST /analyze/analyze-voice",
            "Create Mood Entry": "POST /mood/create",
            "Reflect on Entry": "POST /mood/{entry_id}/reflect",
            "View Mood Entry": "GET /mood/{entry_id}",
            "View User Entries": "GET /mood/user/{user_id}"
        }
    }
