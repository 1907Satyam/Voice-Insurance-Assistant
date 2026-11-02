import { Bot, Headphones, UserRound } from "lucide-react";
import PolicyCard from "./PolicyCard.jsx";
import ClaimStatusBadge from "./ClaimStatusBadge.jsx";

export default function ChatBubble({ message, onPlay, playing }) {
  const isAssistant = message.role === "assistant";
  return (
    <article className={`message-row ${isAssistant ? "message-assistant" : "message-user"}`}>
      <div className={`avatar ${isAssistant ? "avatar-bot" : "avatar-user"}`}>
        {isAssistant ? <Bot size={17} /> : <UserRound size={17} />}
      </div>
      <div className="message-content">
        {message.transcript && isAssistant && (
          <p className="transcript-label">आपने कहा <span>You said</span></p>
        )}
        {message.transcript && isAssistant && <div className="transcript-text">{message.transcript}</div>}
        <div className={`bubble ${isAssistant ? "bubble-assistant" : "bubble-user"}`}>
          {message.text}
          {isAssistant && message.audio && (
            <button type="button" className="audio-replay" onClick={() => onPlay(message.audio, message.audioType)}>
              <Headphones size={14} /> {playing ? "Playing" : "सुनें"}
            </button>
          )}
        </div>
        {message.policy && <PolicyCard policy={message.policy} />}
        {message.claim && <ClaimStatusBadge claim={message.claim} />}
        <time className="message-time">{message.time}</time>
      </div>
    </article>
  );
}
