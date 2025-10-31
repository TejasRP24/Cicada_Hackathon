import React, { useEffect, useState } from "react";
import DynamicBackground from "../components/DynamicBackground";
import { useTheme } from "../components/ThemeContext";
import "../components-css/advicePage.css";

export default function Advice() {
  const { emotion } = useTheme();
  const [advice, setAdvice] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAdvice = async () => {
      try {
        setLoading(true);
        setError("");

        // 🧠 Call your backend — adjust URL as needed
        const response = await fetch("http://localhost:5000/api/advice", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ emotion }), // send current emotion
        });

        if (!response.ok) {
          throw new Error("Server error: " + response.statusText);
        }

        const data = await response.json();
        setAdvice(data.message || "No advice received from backend.");
      } catch (err) {
        console.error(err);
        setError("Failed to fetch advice. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchAdvice();
  }, [emotion]);

  return (
    <div className="advice-page">
      <DynamicBackground />

      <div className="advice-card">
        <h1 className="advice-title">Your Emotional Insight</h1>

        {loading && <p className="advice-text">Fetching advice...</p>}
        {error && <p className="advice-text error">{error}</p>}
        {!loading && !error && <p className="advice-text">{advice}</p>}
      </div>
    </div>
  );
}
