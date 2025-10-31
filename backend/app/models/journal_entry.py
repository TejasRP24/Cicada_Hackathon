from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Index, ForeignKey
from datetime import datetime
from app.database.database import Base

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    mood_score = Column(Float) 
    journal_text = Column(Text)
    final_emotion = Column(String(50))
    reflection_text = Column(Text, nullable=True)

class MoodEntry(Base):
    __tablename__ = 'mood_entries'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    mood_label = Column(String(50), nullable=False)
    mood_score = Column(Float, nullable=False)
    journal_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    reflection_response = Column(Text, nullable=True)
    reflected_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index('idx_user_created', 'user_id', 'created_at'),
    )

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"))
    sender = Column(String(50))  # "user" or "ai"
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)