from fastapi import APIRouter
from pydantic import BaseModel
from app.services.text_sentiment import analyze_text_sentiment

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/analyze-text")
async def analyze_text(input_data: TextInput):
    """
    Analyze the sentiment or emotion of a given text input.
    """
    text = input_data.text.strip()
    if not text:
        return {"error": "Text input cannot be empty."}

    result = analyze_text_sentiment(text)
    return {"text": text, "analysis": result}
