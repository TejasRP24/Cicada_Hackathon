import random

def generate_ai_response(user_message: str, mood: str) -> str:
    """
    Simple placeholder logic. 
    You can later replace with Gemini or an LLM API call.
    """
    responses = {
        "stressed": [
            "It sounds like you're carrying some pressure. Have you tried short breaks?",
            "Stress can be tough — what usually helps you calm down?",
        ],
        "happy": [
            "That’s wonderful! What made you feel this way today?",
            "Great! Maybe you could share your positive experience with a friend?",
        ],
        "sad": [
            "I’m sorry you’re feeling low. Want to talk about what happened?",
            "That’s okay. It’s fine to have down days. How do you usually find comfort?",
        ],
        "default": [
            "Tell me more about what’s on your mind.",
            "I’m listening. How are you feeling right now?",
        ],
    }

    return random.choice(responses.get(mood.lower(), responses["default"]))
