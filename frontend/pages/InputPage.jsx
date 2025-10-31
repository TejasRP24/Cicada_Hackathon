import React, { useState } from "react";
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

    const formData = new FormData();
    if (text) formData.append("text", text);
    if (audioFile) formData.append("file", audioFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const result = await response.json();

      setEmotion(result.emotion || "neutral");
      setOutput(result.message || "Analysis complete.");
    } catch (error) {
      console.error(error);
      setOutput("Something went wrong while analyzing 😔");
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
