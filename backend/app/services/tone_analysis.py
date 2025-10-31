from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
import torch

MODEL_NAME = "audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim"

feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)
model.to("cuda" if torch.cuda.is_available() else "cpu")

def analyze_tone_from_array(y, sr=16000):
    inputs = feature_extractor(y, sampling_rate=sr, return_tensors="pt", padding=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_id = torch.argmax(logits, dim=-1).item()
    predicted_label = model.config.id2label[predicted_id]
    confidence = float(torch.softmax(logits, dim=-1)[0][predicted_id])
    return {"emotion": predicted_label, "confidence": confidence}
