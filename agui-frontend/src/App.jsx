import { useState } from "react";
import MessageRenderer from "./MessageRenderer";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    setMessages(prev => [...prev, { role: "user", content: input }]);

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: input }],
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);

      chunk
        .split("\n")
        .filter(line => line.startsWith("data: "))
        .forEach(line => {
          const json = line.replace("data: ", "").trim();
          if (!json || json === "[DONE]") return;

          const payload = JSON.parse(json);
          setMessages(prev => [...prev, payload]);
        });
    }

    setInput("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>AG-UI + Microsoft Agent Framework</h2>

      <div style={{ border: "1px solid #ccc", minHeight: 300, padding: 10 }}>
        {messages.map((m, i) => (
          <MessageRenderer key={i} msg={m} />
        ))}
      </div>

      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Ask something..."
        style={{ width: "80%" }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}