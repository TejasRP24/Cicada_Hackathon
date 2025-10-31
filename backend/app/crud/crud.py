from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from app import models, schemas


def create_mood_entry(db: Session, entry: schemas.MoodEntryCreate) -> models.MoodEntry:
    db_entry = models.MoodEntry(
        user_id=entry.user_id,
        mood_label=entry.mood_label,
        mood_score=entry.mood_score,
        journal_text=entry.journal_text
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_entries_24hrs_old(db: Session):
    now = datetime.utcnow()
    twenty_four_hrs_ago = now - timedelta(hours=24)

    stressful_moods = ["stressed", "anxious", "overwhelmed", "upset", "nervous", "sad", "angry"]

    entries = (
        db.query(models.MoodEntry)
        .filter(
            and_(
                models.MoodEntry.created_at >= twenty_four_hrs_ago - timedelta(minutes=5),
                models.MoodEntry.created_at <= twenty_four_hrs_ago + timedelta(minutes=5),
                models.MoodEntry.reflection_response.is_(None),
                models.MoodEntry.mood_label.in_(stressful_moods)
            )
        )
        .all()
    )

    return entries