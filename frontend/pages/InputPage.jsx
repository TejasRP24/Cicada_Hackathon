import React, { useState } from "react";
import axios from "axios";
import DynamicBackground from "../components/DynamicBackground";
import "../components-css/inputPage.css";
import { useTheme } from "../components/ThemeContext";

export default function InputPage() {
  const { setEmotion } = useTheme();
  const [text, setText] = useState("");
  const [audioFile, setAudioFile] = useState(null);
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyse = async () => {
    if (!text && !audioFile) {
      setOutput("Please enter a message or upload an audio file 🎤");
      return;
    }

    setLoading(true);
    setOutput("");

    try {
      // If user uploaded an audio file, call the voice analysis endpoint
      if (audioFile) {
        const fd = new FormData();
        fd.append("file", audioFile);

        const resp = await axios.post(
          "http://127.0.0.1:8000/analyze/analyze-voice",
          fd,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        const result = resp.data;
        setEmotion(result.emotion || "neutral");
        setOutput(result.message || "Voice analysis complete.");
      } else {
        // Otherwise call the text analysis endpoint
        const resp = await axios.post(
          "http://127.0.0.1:8000/analyze/analyze-text",
          { text },
          { headers: { "Content-Type": "application/json" } }
        );

        const result = resp.data;
        setEmotion(result.emotion || "neutral");
        setOutput(result.message || "Text analysis complete.");
      }
    } catch (error) {
      console.error(error?.response || error);
      // Show server-sent message if available
      const serverMsg = error?.response?.data?.message;
      setOutput(serverMsg || "Something went wrong while analyzing 😔");
    } finally {
      setLoading(false);
    }
  };

  const onFileChange = (e) => {
    setAudioFile(e.target.files?.[0] ?? null);
  };

  return (
    <div className="input-page">
      <DynamicBackground />

      <div className="input-container">
        <h2 className="page-title">How are you feeling today?</h2>

        {output && (
          <div className="ai-response">
            <strong>AI Insight:</strong> {output}
          </div>
        )}

        <textarea
          className="text-input"
          placeholder="Type your thoughts..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div
          className="audio-drop"
          onDrop={(e) => {
            e.preventDefault();
            setAudioFile(e.dataTransfer.files[0]);
          }}
          onDragOver={(e) => e.preventDefault()}
        >
          {audioFile ? (
            <p>🎵 {audioFile.name}</p>
          ) : (
            <p>🎧 Drag & drop audio or click below</p>
          )}
        </div>

        <input
          id="audio-upload"
          type="file"
          accept="audio/*"
          onChange={onFileChange}
        />
        <label htmlFor="audio-upload" className="file-upload-label">
          Choose Audio File
        </label>

        <button
          className="analyse-btn"
          onClick={handleAnalyse}
          disabled={loading}
        >
          {loading ? "Analysing..." : "Analyse"}
        </button>
      </div>
    </div>
  );
}
