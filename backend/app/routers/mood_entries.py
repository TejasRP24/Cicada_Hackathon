from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import MoodEntryBase, MoodEntryCreate, ReflectionCreate
from app.crud import crud
from ..database import get_db

router = APIRouter()

@router.post("/create", response_model=MoodEntryBase)
async def create_entry(
    entry: MoodEntryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new mood entry.
    If mood is stressful, it will be eligible for 24-hour reflection prompt.
    """
    db_entry = crud.create_mood_entry(db, entry)
    return db_entry


@router.post("/{entry_id}/reflect")
async def submit_reflection(
    entry_id: int,
    reflection: ReflectionCreate,
    db: Session = Depends(get_db)
):
    """
    Submit reflection on a past mood entry.
    Returns mood change and confirmation message.
    """
    db_entry = crud.get_mood_entry(db, entry_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    if db_entry.reflection_response:
        return {
            "status": "already_reflected",
            "message": "Reflection already submitted for this entry"
        }
    
    crud.save_reflection(db, db_entry, reflection.reflection_text)
    mood_change = reflection.current_mood_score - db_entry.mood_score
    
    return {
        "status": "reflection_recorded",
        "mood_change": mood_change,
        "original_mood": db_entry.mood_score,
        "current_mood": reflection.current_mood_score,
        "message": "Reflection saved successfully! Great job reflecting on your emotions."
    }


@router.get("/{entry_id}", response_model=MoodEntryBase)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """Retrieve a mood entry by ID with all its details"""
    entry = crud.get_mood_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.get("/user/{user_id}")
def get_user_entries(user_id: int, db: Session = Depends(get_db)):
    """Get all entries for a specific user"""
    entries = db.query(crud.models.MoodEntry).filter(
        crud.models.MoodEntry.user_id == user_id
    ).order_by(crud.models.MoodEntry.created_at.desc()).all()
    
    return {
        "user_id": user_id,
        "total_entries": len(entries),
        "entries": entries
    }
