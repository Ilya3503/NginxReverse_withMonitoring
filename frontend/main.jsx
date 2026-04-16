import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import axios from "axios";

function App() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);

  const checkPassword = async () => {
    try {
      const res = await axios.post("/api/check-password", {
        password: password
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Password Checker</h1>

      <input
        type="text"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter password"
        style={{ padding: "10px", width: "300px" }}
      />

      <br /><br />

      <button onClick={checkPassword} style={{ padding: "10px 20px" }}>
        Check
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <p><b>Strength:</b> {result.strength}</p>
          <p><b>Score:</b> {result.score}</p>
          <p><b>Instance:</b> {result.instance}</p>
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);