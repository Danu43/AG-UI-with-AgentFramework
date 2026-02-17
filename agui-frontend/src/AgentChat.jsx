import { useState } from "react";

export default function AgentChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    if (!input.trim()) return;

    const userContent = input;
    setInput("");

    // Add user message
    setMessages((prev) => [
      ...prev,
      { role: "user", text: userContent },
    ]);

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: [
          {
            role: "user",
            content: userContent,
          },
        ],
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      console.error("Backend error:", err);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let botText = "";

    // Add empty bot message (will be filled while streaming)
    setMessages((prev) => [...prev, { role: "bot", text: "" }]);

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (!line.startsWith("data:")) continue;

        try {
          const event = JSON.parse(
            line.replace("data:", "").trim()
          );

          if (
            event.type === "TEXT_MESSAGE_CONTENT" &&
            event.delta
          ) {
            botText += event.delta;

            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                role: "bot",
                text: botText,
              };
              return updated;
            });
          }
        } catch {
          // Ignore partial JSON chunks
        }
      }
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h3>AG-UI + Microsoft Agent Framework</h3>

      <div
        style={{
          minHeight: 300,
          border: "1px solid #ccc",
          padding: 10,
          marginBottom: 10,
        }}
      >
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 8 }}>
            <b>{m.role === "user" ? "You" : "Bot"}:</b>{" "}
            {m.text}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "75%", marginRight: 8 }}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}