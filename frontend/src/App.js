import React, { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [question, setQuestion] = useState("");
  const [chart, setChart] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question,
        chart,
      });
      setResponse(res.data);
    } catch (err) {
      setResponse({ error: err.message });
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1 className="main-heading">EcomAgent</h1>
      <form onSubmit={handleAsk} style={{ marginBottom: 24 }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your data..."
          style={{ width: "70%", padding: 8, fontSize: 16 }}
          required
        />
        <label style={{ marginLeft: 16 }}>
          <input
            type="checkbox"
            checked={chart}
            onChange={(e) => setChart(e.target.checked)}
          />{" "}
          Show chart
        </label>
        <button
          type="submit"
          style={{
            marginLeft: 16,
            padding: "8px 24px",
            fontSize: 16,
            background: "#1976d2",
            color: "#fff",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          {loading ? "Loading..." : "Ask"}
        </button>
      </form>

      {response && (
        <div>
          {response.error && <div style={{ color: "red" }}>{response.error}</div>}
          {response.sql_query && (
            <div>
              <strong>SQL Query:</strong>
              <pre>{response.sql_query}</pre>
            </div>
          )}
          {response.result && response.result.columns && Array.isArray(response.result.rows) && (
            <div>
              <strong>Result Table:</strong>
              <table border="1" cellPadding="6" style={{ borderCollapse: "collapse", marginTop: 8 }}>
                <thead>
                  <tr>
                    {response.result.columns.map((col) => (
                      <th key={col}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {response.result.rows.map((row, i) => (
                    <tr key={i}>
                      {row.map((cell, j) => (
                        <td key={j}>{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {/* Show error if rows is not an array */}
          {response.result && response.result.rows && !Array.isArray(response.result.rows) && (
            <div style={{ color: "red", marginTop: 16 }}>
              <strong>Error:</strong> {response.result.rows}
            </div>
          )}
          {response.chart && (
            <div style={{ marginTop: 24 }}>
              <strong>Chart:</strong>
              <br />
              <img
                src={`data:image/png;base64,${response.chart}`}
                alt="Chart"
                style={{ maxWidth: "100%", border: "1px solid #ccc", marginTop: 8 }}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;