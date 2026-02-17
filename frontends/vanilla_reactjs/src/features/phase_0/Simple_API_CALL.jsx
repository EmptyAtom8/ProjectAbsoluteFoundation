import { useState } from "react";
import React from "react";

const Simple_API_Call =()=>{
    
    const [fakePassword, setFakePassword] = useState(6)
    const [helloWorldResponds, setHelloWorldResponds] = useState("")
    const [helloWorldRestful, setHelloWorldRestfulResponds] = useState("")
    const [error, setError] = useState("");
    const API_URL_BASE = import.meta.env.VITE_API_URL_LOCAL ?? "http://127.0.0.1:5000/api"
    async function handleHelloWorld() {
    setError("");
        try {
        const response = await fetch(`${API_URL_BASE}/hello`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result = await response.json();
            setHelloWorldResponds(`${result.content}`);
        } catch (e) {
            setError(String(e.message || e));
        }
    }

    async function handleHelloWorldRestful() {
            setError("");
        try {
        const response = await fetch(`${API_URL_BASE}/hello_restful/${fakePassword}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result = await response.json();
            setHelloWorldRestfulResponds(`${result.content} (${result.reason})`);
        } catch (e) {
            setError(String(e.message || e));
        }
    }
    return (
    <div style={{ padding: 16 }}>
      <h2>Backend Playground</h2>

      <div style={{ marginBottom: 12 }}>
        <button onClick={handleHelloWorld}>Hello World</button>
      </div>

      <div style={{ marginBottom: 12 }}>
        <p>Input Your Password Fake!</p>
        <input
          placeholder="password"
          type="number"
          value={fakePassword}
          onChange={(e) => setFakePassword(Number(e.target.value))}
        />
        <button onClick={handleHelloWorldRestful} style={{ marginLeft: 8 }}>
          Hello World with RESTful
        </button>
      </div>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      <div>
        <p>Response from Hello World: {helloWorldResponds}</p>
        <p>Response from Hello World RESTful: {helloWorldRestful}</p>
      </div>
    </div>
  );
}

export default Simple_API_Call