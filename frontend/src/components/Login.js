import React, { useState } from "react";
import { login } from "../api/auth";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    const res = await login(username, password);

    if (res.token) {
      localStorage.setItem("token", res.token);
      onLogin(res.token);
    } else {
      setError("Invalid credentials");
    }
  };

  const container = {
    maxWidth: "300px",
    margin: "80px auto",
    padding: "20px",
    border: "1px solid #ccc",
    borderRadius: "5px",
    textAlign: "center",
  };

  return (
        <div className="card login-card">
          <h2>Login</h2>

          <input
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />

          <input
            className="input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />

          <button onClick={handleLogin}>Sign In</button>

          {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
        </div>

  );
};

export default Login;
