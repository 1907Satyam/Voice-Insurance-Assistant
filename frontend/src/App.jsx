import { useEffect, useRef, useState } from "react";
import { BadgeCheck, ChevronDown, CircleHelp, Languages, Shield, Sparkles } from "lucide-react";
import ChatBubble from "./components/ChatBubble.jsx";
import VoiceRecorder from "./components/VoiceRecorder.jsx";
import ClaimIntakeForm from "./components/ClaimIntakeForm.jsx";
import useAudioPlayer from "./hooks/useAudioPlayer.js";
import useAudioRecorder from "./hooks/useAudioRecorder.js";
import { fetchPolicies, sendAudio, sendText } from "./services/api.js";

const PROMPTS = [
  { label: "Ambulance cover?", text: "Kya meri health policy ambulance ka kharcha cover karti hai?" },
  { label: "File a motor claim", text: "Meri gaadi ka bumper accident mein toot gaya, claim kaise file karun?" },
  { label: "Track my claim", text: "Mere claim CLM-9842 ki kya sthiti hai?" },
];

const clockTime = () => new Intl.DateTimeFormat("en-IN", { hour: "numeric", minute: "2-digit" }).format(new Date());

export default function App() {
  const [messages, setMessages] = useState([]);
  const [policies, setPolicies] = useState([]);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [claimSubmitted, setClaimSubmitted] = useState(false);
  const feedRef = useRef(null);
  const recorder = useAudioRecorder();
  const player = useAudioPlayer();

  useEffect(() => {
    fetchPolicies()
      .then(setPolicies)
      .catch((error) =>
        setNotice(
          `Policy options are temporarily unavailable (${error.message}). You can still submit a claim without selecting a policy.`,
        ),
      );
  }, []);

  useEffect(() => {
    feedRef.current?.scrollTo({ top: feedRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, busy]);

  async function submitRequest(request) {
    setBusy(true);
    setNotice("");
    try {
      const result = await request();
      if (result.intent === "FILE_CLAIM") setClaimSubmitted(false);
      const assistantMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        transcript: result.transcript,
        text: result.response,
        intent: result.intent,
        policy: result.policy,
        claim: result.claim,
        audio: result.audio_base64,
        audioType: result.audio_content_type,
        time: clockTime(),
      };
      setMessages((current) => [...current, assistantMessage]);
      if (result.audio_base64) {
        try {
          await player.play(result.audio_base64, result.audio_content_type);
        } catch {
          setNotice("जवाब तैयार है, लेकिन ऑडियो अपने आप नहीं चल पाया। सुनने के लिए replay दबाएँ।");
        }
      }
    } catch (error) {
      setNotice(error.message || "अभी जवाब नहीं मिल पाया। कृपया दोबारा कोशिश करें।");
    } finally {
      setBusy(false);
    }
  }

  async function submitAudio() {
    const blob = await recorder.finish();
    if (!blob) {
      setNotice("रिकॉर्डिंग बहुत छोटी थी। कृपया फिर से बोलें।");
      return;
    }
    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", text: "🎙️ Voice message", time: clockTime() },
    ]);
    await submitRequest(() => sendAudio(blob));
  }

  function choosePrompt(prompt) {
    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", text: prompt.text, time: clockTime() },
    ]);
    submitRequest(() => sendText(prompt.text));
  }

  function addClaim(claim, uploadError = "") {
    setClaimSubmitted(true);
    setNotice(uploadError);
    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "assistant", text: "आपकी claim जानकारी दर्ज हो गई है।", claim, time: clockTime() },
    ]);
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a href="#" className="brand" aria-label="Aawaaz home">
          <span className="brand-mark"><Shield size={20} /></span>
          <span>Aawaaz<span className="brand-dot">.</span></span>
        </a>
        <div className="topbar-right">
          <span className="secure-label"><BadgeCheck size={14} /> Secure & private</span>
          <button className="language-button"><Languages size={16} /> हिन्दी <ChevronDown size={14} /></button>
        </div>
      </header>

      <section className="workspace">
        <aside className="intro-panel">
          <div className="availability"><span /> आपकी मदद के लिए तैयार · Here to help</div>
          <h1>बीमा की बातें,<br /><span>अपनी भाषा में।</span></h1>
          <p className="intro-description">Ask about your policy, start a claim, or check its status — just speak naturally.</p>
          <div className="intro-proof"><span className="proof-icon"><Shield size={17} /></span><span>आपकी पॉलिसी, साफ़ शब्दों में।<small>Insurance made easier, one conversation at a time.</small></span></div>
          <div className="privacy-note"><BadgeCheck size={15} /> आपकी बातचीत सुरक्षित रखी जाती है</div>
        </aside>

        <section className="chat-panel" aria-label="Assistant conversation">
          <div className="chat-heading">
            <div className="assistant-avatar"><Sparkles size={19} /></div>
            <div><h2>Aawaaz सहायक</h2><p><span className="online-dot" /> Online · Hindi & Hinglish</p></div>
            <button className="help-button" aria-label="Help"><CircleHelp size={18} /></button>
          </div>
          <div className="chat-feed" ref={feedRef} aria-live="polite">
            <div className="welcome-block">
              <span className="welcome-spark"><Sparkles size={19} /></span>
              <p className="eyebrow">NAMASTE</p>
              <h2>नमस्ते! मैं आपकी कैसे मदद करूँ?</h2>
              <p>आप अपनी पॉलिसी के बारे में पूछ सकते हैं या claim का status जान सकते हैं।</p>
            </div>
            {messages.length === 0 && (
              <div className="prompt-section">
                <p className="eyebrow">TRY ASKING</p>
                <div className="prompt-list">
                  {PROMPTS.map((prompt) => (
                    <button className="prompt-chip" key={prompt.label} disabled={busy} onClick={() => choosePrompt(prompt)}>
                      <span>{prompt.label}</span><span className="prompt-arrow">↗</span>
                    </button>
                  ))}
                </div>
              </div>
            )}
            {messages.map((message) => (
              <ChatBubble key={message.id} message={message} onPlay={player.play} playing={player.isPlaying} />
            ))}
            {!claimSubmitted && messages.some((message) => message.role === "assistant" && message.intent === "FILE_CLAIM") && (
              <ClaimIntakeForm policies={policies} onCreated={addClaim} />
            )}
            {busy && <div className="typing-indicator"><span /><span /><span /> जवाब तैयार हो रहा है…</div>}
            {notice && <div className="notice" role="alert">{notice}</div>}
            {recorder.error && <div className="notice" role="alert">{recorder.error}</div>}
          </div>
          <div className="composer">
            <div className="composer-topline">
              <span><span className="live-dot" /> Voice assistant</span>
            </div>
            <VoiceRecorder
              isRecording={recorder.isRecording}
              duration={recorder.duration}
              onStart={() => { setNotice(""); recorder.start(); }}
              onStop={submitAudio}
              disabled={busy}
            />
            <p className="composer-footnote">आप हिंदी, Hinglish या अपनी सहज भाषा में बोल सकते हैं</p>
          </div>
        </section>
      </section>
      <footer className="page-footer"><span>© 2026 Aawaaz Insurance Assistant</span><span>आपकी बीमा जानकारी को समझना अब आसान है</span><span>{policies.length ? `${policies.length} sample policies` : "For informational support only"}</span></footer>
    </main>
  );
}
