import React, { useState } from "react";
import InputPage from "../pages/InputPage";
import ChatPage from "./ChatPage";
import "../components-css/inputWithChat.css";

export default function InputWithChat() {
  const [showChat, setShowChat] = useState(true);

  return (
    <div className="input-chat-wrapper">
      <div className="left-section">
        <InputPage />
      </div>

      <div className={`right-section ${showChat ? "visible" : "hidden"}`}>
        <ChatPage />
      </div>

      <button
        className="toggle-chat-btn"
        onClick={() => setShowChat((prev) => !prev)}
      >
        {showChat ? "Hide Chat 🤖" : "Show Chat 💬"}
      </button>
    </div>
  );
}
