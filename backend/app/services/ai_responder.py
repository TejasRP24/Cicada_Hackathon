import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_ai_response(user_text: str, emotion: str):
    try:
        # --------------- GEMINI PROMPT ---------------
        prompt = f"""
        You are a compassionate mental wellness assistant. 
        The user expressed a {emotion} emotion and said: "{user_text}"

        Respond in a gentle, human-like tone using 2–4 lines.
        Your goal is to comfort, validate emotions, and offer gentle positivity.
        Avoid sounding robotic, overly formal, or giving medical advice.
        Example:
        - If sadness → “I can sense this is weighing on you. Remember, it’s okay to slow down. You’ve already taken a strong step by expressing it 💙”
        - If anger → “It’s valid to feel frustrated when things go wrong. Try to take a moment to breathe—you deserve calm too.”
        - If joy → “That’s wonderful! Your happiness shines through. Keep celebrating those moments—they make life brighter 🌻”
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("AI response error:", e)

        # --------------- FALLBACK OFFLINE MESSAGES ---------------
        fallback = {
            "sadness": (
                "It sounds like you’re going through a tough moment. "
                "Take a pause, breathe deeply, and remind yourself that better days do come. "
                "You’re not alone in this journey 💙"
            ),
            "anger": (
                "Your feelings are completely valid. "
                "Try to give yourself a moment to release the tension—maybe step away or take a few deep breaths. "
                "You deserve calm and understanding too 🔆"
            ),
            "fear": (
                "It’s okay to feel uncertain or scared sometimes. "
                "What matters is that you’re still moving forward, one step at a time. "
                "You have the strength to get through this 🌿"
            ),
            "joy": (
                "That’s such a beautiful feeling! "
                "Hold on to this joy—it’s a reminder of all the good that surrounds you. "
                "Share it with someone today 🌞"
            ),
            "neutral": (
                "I’m here with you, listening and present. "
                "Whatever’s on your mind, it matters—and you matter too 🤍"
            ),
        }
        return fallback.get(emotion.lower(), "I'm here with you, whenever you need to talk 💙")
