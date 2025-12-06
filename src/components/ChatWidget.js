import React from "react";
import { useNavigate } from "react-router-dom";

export default function ChatWidget() {
  const navigate = useNavigate();

  return (
    <div className="chat-bubble fixed bottom-6 right-6 z-50">
      <button
        onClick={() => navigate("/ai")}
        className="w-14 h-14 rounded-full bg-gradient-to-br from-[var(--gm-blue-1)] to-[var(--gm-blue-2)] text-white flex items-center justify-center shadow-2xl transform hover:scale-105 transition"
        title="AI Assistant"
      >
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
          <rect
            x="3"
            y="6"
            width="18"
            height="12"
            rx="3"
            fill="white"
            opacity="0.12"
          />
          <circle cx="9" cy="12" r="1.2" fill="white" />
          <circle cx="15" cy="12" r="1.2" fill="white" />
          <rect x="8" y="3" width="8" height="2" rx="1" fill="white" />
        </svg>
      </button>
    </div>
  );
}
