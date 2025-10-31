import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useTheme } from "./ThemeContext";
import "../components-css/chatPage.css";

export default function ChatPage() {
  const { setEmotion } = useTheme();
  const [messages, setMessages] = useState([
    { sender: "ai", text: "Hey there 👋 How are you feeling today?" },
  ]);
  const [input, setInput] = useState("");
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [isFirstMessage, setIsFirstMessage] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      // For the first message, analyze the emotion
      if (isFirstMessage) {
        const analyzeResponse = await axios.post(
          "http://127.0.0.1:8000/analyze/analyze-text",
          { text: input.trim() }
        );
        
        // Update the theme based on the emotion
        const emotion = analyzeResponse.data.analysis?.mood_label || "neutral";
        setEmotion(emotion.toLowerCase());
        
        // Add emotion analysis message
        setMessages((prev) => [
          ...prev,
          { 
            sender: "ai", 
            text: `I sense that you're feeling ${emotion.toLowerCase()}. Let's talk about it.` 
          },
        ]);
        
        setIsFirstMessage(false);
      }

      // Then proceed with the chat response
      const response = await axios.post("http://127.0.0.1:8000/chat/chat", {
        user_message: input.trim(),
        session_id: sessionId
      });

      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: response.data.response },
      ]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "I'm having trouble responding right now. Please try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <h2 className="chat-title">AI Companion 🤖</h2>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </div>

      <div className="chat-input-area">
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading}>
          {isLoading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}
