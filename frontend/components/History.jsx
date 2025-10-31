import React, { useEffect, useState } from "react";
import DynamicBackground from "../components/DynamicBackground";
import { useTheme } from "../components/ThemeContext";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import "../components-css/historyPage.css";

export default function History() {
  const { emotion } = useTheme();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        setError("");

        // 🔗 Replace with your actual backend endpoint
        const response = await fetch("http://localhost:5000/api/history");
        if (!response.ok) throw new Error("Failed to fetch history data");

        const json = await response.json();
        setData(json);
      } catch (err) {
        console.warn("⚠️ Backend unreachable — using mock data");
  setData([
    { date: "2025-10-20", happiness: 70, emotion: "happy" },
    { date: "2025-10-21", happiness: 45, emotion: "sad" },
    { date: "2025-10-22", happiness: 60, emotion: "neutral" },
    { date: "2025-10-23", happiness: 90, emotion: "happy" },
    { date: "2025-10-24", happiness: 30, emotion: "anger" },
    { date: "2025-10-25", happiness: 55, emotion: "neutral" },
  ]);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  // Calculate emotion distribution for pie chart
  const emotionCounts = data.reduce((acc, item) => {
    acc[item.emotion] = (acc[item.emotion] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.entries(emotionCounts).map(([name, value]) => ({
    name,
    value,
  }));

  const COLORS = ["#66a6ff", "#ff9a9e", "#ff416c", "#485563", "#f6d365"];

  return (
    <div className="history-page">
      <DynamicBackground />

      <div className="history-container">
        <h1 className="history-title">Your Emotional History</h1>

        {loading && <p className="history-text">Loading data...</p>}
        {error && <p className="history-text error">{error}</p>}

        {!loading && !error && data.length > 0 && (
          <>
            <div className="chart-section">
              <h2 className="chart-title">Happiness Rate Over Time</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                  <XAxis dataKey="date" stroke="#fff" />
                  <YAxis stroke="#fff" />
                  <Tooltip />
                  <Line type="monotone" dataKey="happiness" stroke="#66a6ff" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-section">
              <h2 className="chart-title">Emotion Distribution</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    dataKey="value"
                    label
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
