import { useState, useRef } from "react";
import {
  Room,
  RoomEvent,
  createLocalAudioTrack,
} from "livekit-client";
import "./App.css";

export default function App() {
  const [screen, setScreen] = useState("welcome"); // welcome | call
  const [room, setRoom] = useState(null);
  const [micOn, setMicOn] = useState(true);
  const [agentSpeaking, setAgentSpeaking] = useState(false);
  const [transcripts, setTranscripts] = useState([]);

  const micTrack = useRef(null);
  const transcriptMap = useRef({}); // FIX for partial spam

  async function joinRoom() {
    // const roomName = `healthflow_${crypto.randomUUID()}`;

    // const res = await fetch(
    //   `http://localhost:8000/token?identity=web-user&room=${roomName}`
    // );

    const res = await fetch(
      `http://localhost:8000/token?identity=web-user`
    );
    const data = await res.json();

    const lkRoom = new Room({ adaptiveStream: true, dynacast: true });

    // 🔊 Agent audio autoplay
    lkRoom.on(RoomEvent.TrackSubscribed, track => {
      if (track.kind === "audio") track.attach();
    });

    // 🟢 Agent speaking pulse
    lkRoom.on(RoomEvent.ActiveSpeakersChanged, speakers => {
      setAgentSpeaking(
        speakers.some(p => p.identity.includes("agent"))
      );
    });

    // 📝 CLEAN transcripts (FINAL ONLY)
    lkRoom.on(
      RoomEvent.TranscriptionReceived,
      (segments, participant) => {
        segments.forEach(seg => {
          if (!seg.text || !seg.final) return;

          transcriptMap.current[seg.id] = {
            speaker: participant.identity.includes("agent")
              ? "agent"
              : "you",
            text: seg.text,
          };
        });

        setTranscripts(Object.values(transcriptMap.current));
      }
    );

    await lkRoom.connect(data.url, data.token);
    await lkRoom.localParticipant.setMicrophoneEnabled(true);

    setRoom(lkRoom);
    setScreen("call");
  }

  async function toggleMic() {
    if (!room) return;

    if (micOn) {
      room.localParticipant.setMicrophoneEnabled(false);
    } else {
      room.localParticipant.setMicrophoneEnabled(true);
    }
    setMicOn(!micOn);
  }

  async function endCall() {
    if (room) {
      await room.disconnect();
      setRoom(null);
    }
    transcriptMap.current = {};
    setTranscripts([]);
    setScreen("welcome");
  }

  // ---------------- UI ----------------

if (screen === "welcome") {
  return (
    <div className="welcome-wrapper">
      <div className="welcome-card">
        <h1>Welcome to Agent</h1>
        <p>Your AI Voice Assistant</p>
        <button className="join-btn" onClick={joinRoom}>
          Join Call
        </button>
      </div>
    </div>
  );
}

return (
  <div className="call-root">
    {/* LEFT — AGENT (FIXED 50%) */}
    <div className="agent-panel">
      <div className={`agent-avatar ${agentSpeaking ? "pulse" : ""}`}>
        V
      </div>

      <div
        className={`agent-status ${
          agentSpeaking ? "speaking" : "listening"
        }`}
      >
        {agentSpeaking ? "Agent speaking" : "Listening…"}
      </div>

      <div className="agent-controls">
        <button onClick={toggleMic}>
          {micOn ? "Mute" : "Unmute"}
        </button>
        <button className="end" onClick={endCall}>
          End
        </button>
      </div>
    </div>

    {/* RIGHT — CONVERSATION (FIXED 50%) */}
    <div className="conversation-panel">
      <h3>Conversation</h3>

      <div className="conversation-scroll">
        {transcripts.map((t, i) => (
          <div key={i} className={`bubble ${t.speaker}`}>
            {t.text}
          </div>
        ))}
      </div>
    </div>
  </div>
);
}
