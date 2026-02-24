import { useState, useRef, useEffect } from "react";
import {
  Room,
  RoomEvent,
} from "livekit-client";
import "./App.css";

export default function App() {
  const [screen, setScreen] = useState("welcome"); // welcome | loading | call
  const [room, setRoom] = useState(null);
  const [micOn, setMicOn] = useState(true);
  const [agentSpeaking, setAgentSpeaking] = useState(false);
  const [userSpeaking, setUserSpeaking] = useState(false);
  const [transcripts, setTranscripts] = useState([]);
  const [chatInput, setChatInput] = useState("");

  const scrollRef = useRef(null);

  // Auto-scroll to bottom of conversation
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [transcripts]);

  // -----------------------------------------------------------------------
  // DataReceived: Handle messages from the agent (text chat replies)
  // -----------------------------------------------------------------------
  useEffect(() => {
    if (!room) return;

    const handleData = (payload, participant) => {
      const decoder = new TextDecoder();
      const text = decoder.decode(payload);

      const participantId = participant?.identity ?? "";
      const isAgent =
        participantId.startsWith("agent") ||
        participantId.includes("assistant");

      // Try to parse as JSON (for structured events like agent_started_speaking)
      try {
        const jsonData = JSON.parse(text);
        if (jsonData?.event === "agent_started_speaking") {
          setAgentSpeaking(jsonData.value);
          return;
        }
      } catch (_) {
        // Not JSON — treat as plain text chat message below
      }

      // Handle normal text from agent as a chat bubble
      if (isAgent && text.trim()) {
        const messageId = `agent-msg-${Date.now()}`;
        setTranscripts(prev => [
          ...prev,
          { id: messageId, speaker: "agent", text: text.trim(), final: true }
        ]);
      }
    };

    room.on(RoomEvent.DataReceived, handleData);
    return () => room.off(RoomEvent.DataReceived, handleData);
  }, [room]);

  async function joinRoom() {
    setScreen("loading");
    try {
      const res = await fetch(`http://localhost:8000/token?identity=web-user`);
      const data = await res.json();

      const lkRoom = new Room({ adaptiveStream: true, dynacast: true });

      // 🔊 Agent audio autoplay
      lkRoom.on(RoomEvent.TrackSubscribed, track => {
        if (track.kind === "audio") track.attach();
      });

      // 🟢 Speaking indicators
      lkRoom.on(RoomEvent.ActiveSpeakersChanged, speakers => {
        setAgentSpeaking(speakers.some(p => p.identity.includes("agent")));
        setUserSpeaking(speakers.some(p => !p.identity.includes("agent")));
      });

      // 📝 Real-time transcripts (Streaming effect via voice)
      lkRoom.on(RoomEvent.TranscriptionReceived, (segments, participant) => {
        setTranscripts(prev => {
          const newTranscripts = [...prev];
          segments.forEach(seg => {
            if (!seg.text) return;
            const idx = newTranscripts.findIndex(t => t.id === seg.id);
            const entry = {
              id: seg.id,
              speaker: participant.identity.includes("agent") ? "agent" : "you",
              text: seg.text,
              final: seg.final,
            };
            if (idx > -1) {
              newTranscripts[idx] = entry;
            } else {
              newTranscripts.push(entry);
            }
          });
          return newTranscripts;
        });
      });

      await lkRoom.connect(data.url, data.token);
      await lkRoom.localParticipant.setMicrophoneEnabled(true);

      setRoom(lkRoom);
      setScreen("call");
    } catch (err) {
      console.error("Failed to join room:", err);
      setScreen("welcome");
    }
  }

  async function toggleMic() {
    if (!room) return;
    const isEnabled = !micOn;
    await room.localParticipant.setMicrophoneEnabled(isEnabled);
    setMicOn(isEnabled);
  }

  async function endCall() {
    if (room) {
      await room.disconnect();
      setRoom(null);
    }
    setTranscripts([]);
    setScreen("welcome");
  }

  // -----------------------------------------------------------------------
  // Text chat: use sendText (topic: 'lk.chat') so the agent receives it
  // natively without any custom data_received handler on the agent side
  // -----------------------------------------------------------------------
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || !room) return;

    const msg = chatInput.trim();
    setChatInput("");

    // Add the user message immediately to the conversation
    setTranscripts(prev => [
      ...prev,
      { id: `manual-${Date.now()}`, speaker: "you", text: msg, final: true }
    ]);

    // Send via LiveKit's native text channel — the agent pipeline picks this up automatically
    try {
      await room.localParticipant.sendText(msg, { topic: "lk.chat" });
    } catch (err) {
      console.error("Failed to send text:", err);
    }
  };

  // ---------------- UI ----------------

  if (screen === "welcome") {
    return (
      <div className="welcome-wrapper">
        <div className="welcome-card">
          <h1>Welcome to AZ Bank</h1>
          <p className="subtitle">Your 24/7 Premium AI Concierge</p>
          <p className="info-text">Talk with our agent for your issues</p>
          <button className="join-btn" onClick={joinRoom}>
            Talk to Assistant
          </button>
        </div>
      </div>
    );
  }

  if (screen === "loading") {
    return (
      <div className="loading-wrapper">
        <div className="spinner"></div>
        <p>Connecting to secure bank gateway...</p>
      </div>
    );
  }

  return (
    <div className="call-root">
      {/* LEFT — AGENT PANEL */}
      <div className="agent-panel">
        <div className="agent-avatar-container">
          <div className={`agent-avatar ${(agentSpeaking || userSpeaking) ? "pulse" : ""}`}>
            AZ
          </div>
          <div className={`visualizer-ring ${(agentSpeaking || userSpeaking) ? "active" : ""}`}></div>
        </div>

        <div className="agent-status">
          <h2>AZ Support Agent</h2>
          <p>
            <span className={`status-indicator ${agentSpeaking ? "active" : ""}`}></span>
            {agentSpeaking ? "Speaking..." : userSpeaking ? "Listening..." : "Ready to assist"}
          </p>
        </div>

        <div className="agent-controls">
          <button className="control-btn" onClick={toggleMic}>
            {micOn ? "Mute Mic" : "Unmute Mic"}
          </button>
          <button className="control-btn end" onClick={endCall}>
            End Session
          </button>
        </div>
      </div>

      {/* RIGHT — CONVERSATION PANEL */}
      <div className="conversation-panel">
        <div className="panel-header">
          <h3>Secure Conversation</h3>
          <span className="live-tag">LIVE</span>
        </div>

        <div className="conversation-scroll" ref={scrollRef}>
          {transcripts.map((t) => (
            <div key={t.id} className={`bubble ${t.speaker} ${!t.final ? "partial" : ""}`}>
              {t.text}
            </div>
          ))}
          {transcripts.length === 0 && (
            <div className="empty-chat">
              How can I help you today?
            </div>
          )}
        </div>

        <form className="chat-input-container" onSubmit={handleSendMessage}>
          <input
            className="chat-input"
            placeholder="Type your message here..."
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
          />
          <button className="send-btn" type="submit" disabled={!chatInput.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
