from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MoodEntryCreate(BaseModel):
    user_id: int
    mood_label: str
    mood_score: float
    journal_text: str

class MoodEntryBase(BaseModel):
    id: int
    user_id: int
    mood_label: str
    mood_score: float
    journal_text: str
    created_at: datetime
    reflection_response: Optional[str] = None
    reflected_at: Optional[datetime] = None

    class Config:
        from_attributes = True  
        
class ReflectionCreate(BaseModel):
    reflection_text: str
    current_mood_score: float
