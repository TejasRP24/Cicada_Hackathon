from transformers import pipeline

# Load once at startup (avoids reloading every request)
emotion_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=False
)

def analyze_text_sentiment(text: str):
    """Analyze emotion from text input and return mood label + score."""
    result = emotion_analyzer(text)[0]
    mood_label = result["label"]
    mood_score = round(result["score"], 3)
    
    return {
        "mood_label": mood_label,
        "mood_score": mood_score,
        "journal_text": text
    }
