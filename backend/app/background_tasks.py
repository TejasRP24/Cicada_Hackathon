import asyncio
from .database import SessionLocal
from app.crud.crud import get_entries_24hrs_old

async def notify_user(user_id: int, entry_id: int, original_mood: str, original_text: str):
    """
    Send notification to user about reflection prompt.
    Replace this with actual notification system (push, email, WebSocket, etc.)
    """
    print(f"\n{'='*70}")
    print(f"NOTIFICATION FOR USER {user_id}")
    print(f"{'='*70}")
    print(f"Entry ID: {entry_id}")
    print(f"Original Mood: {original_mood}")
    print(f"Original Entry: {original_text[:100]}...")
    print(f"Message: Time to reflect on your mood entry from 24 hours ago!")
    print(f"{'='*70}\n")

async def check_and_prompt_24hr_reflections():
    """
    Periodic task that checks for entries created 24 hours ago
    and sends reflection prompts for those entries.
    Runs every hour by default.
    """
    print("Background task started: Checking for 24-hour-old entries...")
    
    while True:
        await asyncio.sleep(3600)  # Check every hour (3600 seconds)
        
        db = SessionLocal()
        try:
            entries = get_entries_24hrs_old(db)
            
            if entries:
                print(f"\nFound {len(entries)} entry/entries due for reflection!")
                for entry in entries:
                    await notify_user(
                        entry.user_id,
                        entry.id,
                        entry.mood_label,
                        entry.journal_text
                    )
            else:
                print("No entries due for reflection at this time.")
        except Exception as e:
            print(f"Error in background task: {e}")
        finally:
            db.close()
