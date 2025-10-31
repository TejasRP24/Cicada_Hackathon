def fuse_emotions(text_emotion, tone_emotion):
    """
    Fuse text and tone emotions intelligently, handling unknown categories safely.
    """
    text_emotion_name = text_emotion.get("emotion") if isinstance(text_emotion, dict) else text_emotion
    tone_emotion_name = tone_emotion.get("emotion") if isinstance(tone_emotion, dict) else tone_emotion

    # Define normalized priority list
    priority = ["anger", "fear", "sadness", "arousal", "dominance", "neutral", "joy"]

    # If emotion not in list, fallback to neutral
    if text_emotion_name not in priority:
        text_emotion_name = "neutral"
    if tone_emotion_name not in priority:
        tone_emotion_name = "neutral"

    # If both same → return directly
    if text_emotion_name == tone_emotion_name:
        fused_emotion = text_emotion_name
    else:
        # Choose emotion with higher intensity or lower index priority
        fused_emotion = (
            text_emotion_name
            if priority.index(text_emotion_name) < priority.index(tone_emotion_name)
            else tone_emotion_name
        )

    return {"fused_emotion": fused_emotion}
