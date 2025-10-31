import whisper
import os
import subprocess

# Load Whisper model once (outside the function for efficiency)
model = whisper.load_model("base")  # you can change to "small", "medium", or "large" if needed

def transcribe_audio(audio_path: str) -> str:
    # Ensure audio is in correct format (convert if needed)
    wav_path = os.path.splitext(audio_path)[0] + "_converted.wav"

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", audio_path, "-ac", "1", "-ar", "16000", wav_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        print("FFmpeg conversion failed:", e)
        return ""

    # Use Whisper for transcription
    try:
        result = model.transcribe(wav_path)
        text = result["text"].strip()
        print("Transcribed Text:", text)
        return text
    except Exception as e:
        print("Whisper transcription failed:", e)
        return ""
