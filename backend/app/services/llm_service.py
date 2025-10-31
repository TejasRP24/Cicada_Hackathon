from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.config import settings

def analyze_tone_with_gemini(features):
    model = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",
        google_api_key=settings.GOOGLE_API_KEY
    )

    prompt = PromptTemplate.from_template("""
    You are an emotion analysis expert. The following normalized acoustic features describe a human voice, where:
    - pitch_mean: 0 (very low pitch) → 1 (very high pitch)
    - energy: 0 (very quiet) → 1 (very loud)
    - tempo: 0 (very slow) → 1 (very fast)
    - mfcc_mean: 0 (muffled tone) → 1 (clear tone)

    Given:
    Pitch Mean: {pitch_mean}
    Energy: {energy}
    Tempo: {tempo}
    MFCCs: {mfcc_mean}

    Predict the emotion (happy, calm, sad, stressed, angry, or anxious)
    and provide a short empathetic message (1–2 sentences).

    Return JSON like:
    {{"emotion": "<emotion>", "reflection": "<message>"}}
    """)


    chain = prompt | model
    return chain.invoke(features).content
