import React, { useState, useRef, useEffect } from "react";
import "../components-css/chatPage.css";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { sender: "ai", text: "Hey there 👋 How are you feeling today?" },
  ]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    // Dummy AI reply (replace with backend call later)
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "I'm here to listen 💬" },
      ]);
    }, 800);

    setInput("");
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
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
