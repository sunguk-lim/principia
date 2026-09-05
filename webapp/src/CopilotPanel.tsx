import { useEffect, useMemo, useRef, useState } from "react";
import type { GraphNode } from "./types";

export interface CopilotStatus {
  available: boolean;
  agentName: string;
  mode: "read-only";
}

interface ChatMessage {
  role: "user" | "assistant";
  text: string;
}

interface Props {
  status: CopilotStatus;
  selected: GraphNode | null;
  onClose: () => void;
}

const MESSAGE_KEY = "principia-copilot-messages-v1";
const CONVERSATION_KEY = "principia-copilot-conversation-v1";

function conversationId(): string {
  let id = localStorage.getItem(CONVERSATION_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(CONVERSATION_KEY, id);
  }
  return id;
}

function initialMessages(): ChatMessage[] {
  try { return JSON.parse(sessionStorage.getItem(MESSAGE_KEY) || "[]"); }
  catch { return []; }
}

export function CopilotPanel({ status, selected, onClose }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);
  const suggestions = useMemo(() => selected ? [
    `Explain ${selected.title} simply.`,
    "What should I understand first?",
    "Give me a concrete example.",
  ] : [
    "How should I start exploring this graph?",
    "How do prerequisites work here?",
  ], [selected]);

  useEffect(() => { sessionStorage.setItem(MESSAGE_KEY, JSON.stringify(messages)); }, [messages]);
  useEffect(() => { scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" }); }, [messages, sending]);

  const send = async (text = draft) => {
    const question = text.trim();
    if (!question || sending) return;
    setMessages(current => [...current, { role: "user", text: question }]);
    setDraft("");
    setError("");
    setSending(true);
    try {
      const response = await fetch("/api/copilot/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: question, conversation_id: conversationId(), node_id: selected?.id || null }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.detail || "Principia Copilot is unavailable");
      setMessages(current => [...current, { role: "assistant", text: payload.answer }]);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Principia Copilot is unavailable");
    } finally { setSending(false); }
  };

  const newChat = () => {
    localStorage.setItem(CONVERSATION_KEY, crypto.randomUUID());
    setMessages([]);
    setDraft("");
    setError("");
  };

  return <aside className="node-panel codex-panel copilot-panel">
    <header className="panel-head"><div><span className="eyebrow">Private · {status.mode}</span><h2>{status.agentName}</h2></div><div className="panel-actions"><button className="codex-refresh" onClick={newChat}>New chat</button><button className="icon-button" onClick={onClose} aria-label="Close Principia Copilot">×</button></div></header>
    <div className="codex-safety"><span className="codex-dot"/><div><strong>Restricted agent</strong><p>No filesystem, command, web, messaging, session, or plugin tools are available to this copilot.</p></div></div>
    {selected && <div className="copilot-context"><span className="eyebrow">Discussing</span><strong>{selected.title}</strong><small>{selected.root} · level {selected.level}</small></div>}
    <div className="copilot-messages" ref={scrollRef} aria-live="polite">
      {!messages.length && <div className="copilot-welcome"><span>🧭</span><strong>Ask about the graph.</strong><p>I can explain the selected concept, connect it to prerequisites, or suggest what to study next.</p><div>{suggestions.map(item => <button key={item} onClick={() => void send(item)}>{item}</button>)}</div></div>}
      {messages.map((message, index) => <div key={index} className={`copilot-message ${message.role}`}><span>{message.role === "assistant" ? "Principia Copilot" : "You"}</span><p>{message.text}</p></div>)}
      {sending && <div className="copilot-message assistant thinking"><span>Principia Copilot</span><p><i/><i/><i/></p></div>}
    </div>
    {error && <div className="copilot-error">{error}</div>}
    <form className="copilot-composer" onSubmit={event => { event.preventDefault(); void send(); }}>
      <textarea value={draft} maxLength={3000} placeholder={selected ? `Ask about ${selected.title}…` : "Ask about the knowledge graph…"} onChange={event => setDraft(event.target.value)} onKeyDown={event => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); void send(); } }} />
      <button disabled={sending || !draft.trim()} aria-label="Send to Principia Copilot">↑</button>
    </form>
  </aside>;
}
