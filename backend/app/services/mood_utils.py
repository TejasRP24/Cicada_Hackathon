def emotion_to_score(emotion: str) -> int:
    """
    Maps final emotion to a 1–10 mood score.
    Higher = more positive emotional state.
    """
    emotion_map = {
        "joy": 9,
        "happiness": 9,
        "love": 8,
        "calm": 7,
        "neutral": 5,
        "sadness": 3,
        "fear": 4,
        "anger": 2,
        "anxiety": 4,
        "stress": 3,
        "frustration": 2,
        "depression": 1
    }
    return emotion_map.get(emotion.lower(), 5)
