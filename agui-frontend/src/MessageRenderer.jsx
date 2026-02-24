export default function MessageRenderer({ msg }) {
  // 1️⃣ Table rendering
  if (msg?.type === "table") {
    // Safety checks
    if (!Array.isArray(msg.columns) || !Array.isArray(msg.rows)) {
      return <div>⚠️ Invalid table data</div>;
    }

    return (
      <div style={{ overflowX: "auto", marginTop: "10px" }}>
        <table
          border="1"
          cellPadding="6"
          style={{ borderCollapse: "collapse", width: "100%" }}
        >
          <thead style={{ background: "#f2f2f2" }}>
            <tr>
              {msg.columns.map((col, idx) => (
                <th key={idx}>{col}</th>
              ))}
            </tr>
          </thead>

          <tbody>
            {msg.rows.map((row, rowIdx) => (
              <tr key={rowIdx}>
                {row.map((cell, cellIdx) => (
                  <td key={cellIdx}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  // 2️⃣ Normal text rendering
  if (typeof msg === "string") {
    return <div>{msg}</div>;
  }

  if (msg?.content) {
    return <div>{msg.content}</div>;
  }

  // 3️⃣ Fallback (debug-safe)
  return <pre>{JSON.stringify(msg, null, 2)}</pre>;
}