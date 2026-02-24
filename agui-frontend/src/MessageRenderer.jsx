export default function MessageRenderer({ msg }) {
  if (!msg) return null;

  // STEP 1: Normalize message (string → object)
  let payload = msg;

  if (typeof msg === "string") {
    try {
      payload = JSON.parse(msg);
    } catch {
      return <pre>{msg}</pre>;
    }
  }

  if (typeof msg.content === "string") {
    try {
      payload = JSON.parse(msg.content);
    } catch {
      payload = msg.content;
    }
  }

  // STEP 2: Render TABLE
  if (payload?.type === "table") {
    return (
      <div style={{ overflowX: "auto", marginTop: 12 }}>
        <table border="1" cellPadding="6" cellSpacing="0">
          <thead>
            <tr>
              {payload.columns.map((col, i) => (
                <th key={i}>{col}</th>
              ))}
            </tr>
          </thead>

          <tbody>
            {payload.rows.map((row, rIdx) => (
              <tr key={rIdx}>
                {row.map((cell, cIdx) => (
                  <td key={cIdx}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  // STEP 3: Render normal text
  if (typeof payload === "string") {
    return <div>{payload}</div>;
  }

  if (payload?.content) {
    return <div>{payload.content}</div>;
  }

  return <pre>{JSON.stringify(payload, null, 2)}</pre>;
}