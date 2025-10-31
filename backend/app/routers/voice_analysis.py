from fastapi import APIRouter, UploadFile, Depends
import tempfile
import librosa
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.services.audio_features import extract_audio_features_from_array
from app.services.transcribe_audio import transcribe_audio
from app.services.text_sentiment import analyze_text_sentiment
from app.services.tone_analysis import analyze_tone_from_array
from app.services.fusion_engine import fuse_emotions
from app.services.ai_responder import generate_ai_response
from app.services.mood_utils import emotion_to_score
from app.database.database import get_db
from app.models.journal_entry import JournalEntry
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/analyze-voice")
async def analyze_voice(file: UploadFile, db: Session = Depends(get_db)):
    # Save uploaded audio file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Load audio
    y, sr = librosa.load(tmp_path, sr=16000)

    # Extract tone + text emotion
    tone_emotion = analyze_tone_from_array(y, sr)
    text = transcribe_audio(tmp_path)
    text_emotion = analyze_text_sentiment(text)
    print("Text Emotion:", text_emotion)
    print("Tone Emotion:", tone_emotion)

    # Fuse final emotion
    fused = fuse_emotions(text_emotion, tone_emotion)
    final_emotion = fused["fused_emotion"]

    # Convert to numeric mood score (1–10)
    today_score = emotion_to_score(final_emotion)

    # Fetch yesterday’s mood (if exists)
    yesterday = datetime.utcnow() - timedelta(days=1)
    yesterday_entry = (
        db.query(JournalEntry)
        .filter(
            JournalEntry.date >= yesterday.replace(hour=0, minute=0, second=0),
            JournalEntry.date <= yesterday.replace(hour=23, minute=59, second=59)
        )
        .order_by(desc(JournalEntry.date))
        .first()
    )

    if yesterday_entry:
        mirror_score = today_score - yesterday_entry.mood_score
    else:
        mirror_score = 0  # No previous data to compare

    # Generate supportive AI response
    ai_message = generate_ai_response(text, final_emotion)

    # Save current entry in DB (id & date auto-handled)
    new_entry = JournalEntry(
        mood_score=today_score,
        journal_text=text,
        final_emotion=final_emotion
    )
    db.add(new_entry)
    db.commit()

    return {
        "final_emotion": final_emotion,
        "mood_score": today_score,
        "mirror_moment_change": mirror_score,
        "message": (
            "You seem to be feeling a bit better today. Keep up your positive energy!"
            if mirror_score > 0 else
            "Your mood seems slightly lower than yesterday. Take it slow, and remember that emotions fluctuate naturally."
            if mirror_score < 0 else
            "Your mood feels similar to yesterday — consistency is good! Stay mindful."
        ),
        "response_message": ai_message
    }
