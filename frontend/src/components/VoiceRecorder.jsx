import { Mic, Square, AudioLines } from "lucide-react";

function formatTime(seconds) {
  return `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
}

export default function VoiceRecorder({ isRecording, duration, onStart, onStop, disabled }) {
  return (
    <div className="recorder">
      <div className={`waveform ${isRecording ? "waveform-active" : ""}`} aria-hidden="true">
        {Array.from({ length: 25 }, (_, index) => (
          <span key={index} style={{ "--bar": `${12 + ((index * 17) % 35)}px`, "--delay": `${index * 35}ms` }} />
        ))}
      </div>
      <button
        type="button"
        className={`mic-button ${isRecording ? "mic-recording" : ""}`}
        onClick={isRecording ? onStop : onStart}
        disabled={disabled}
        aria-label={isRecording ? "Stop recording" : "Start voice recording"}
      >
        {isRecording ? <Square size={22} fill="currentColor" /> : <Mic size={27} />}
      </button>
      <div className="recorder-hint">
        {isRecording ? (
          <><span className="recording-dot" /> सुन रहा हूँ <span className="timer">{formatTime(duration)}</span></>
        ) : (
          <><AudioLines size={15} /> बोलने के लिए टैप करें <span className="hint-en">Tap to speak</span></>
        )}
      </div>
    </div>
  );
}
