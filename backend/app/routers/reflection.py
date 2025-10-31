from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.journal_entry import JournalEntry

router = APIRouter()

@router.post("/submit-reflection")
async def submit_reflection(request: Request, db: Session = Depends(get_db)):
    """
    Submit reflection text for a specific journal entry.
    """
    data = await request.json()
    entry_id = data.get("entry_id")
    reflection_text = data.get("reflection_text", "")

    if not entry_id:
        return {"error": "entry_id is required"}
    if not reflection_text:
        return {"error": "reflection_text is required"}

    # Fetch the existing journal entry
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        return {"error": f"No journal entry found with id {entry_id}"}

    # Save reflection (you can add a new column for it)
    entry.journal_text += f"\n\nReflection: {reflection_text}"
    db.commit()

    return {"message": "Reflection added successfully"}
