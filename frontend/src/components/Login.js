/*
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

*/

import React, { useState } from "react";
import { login, register } from "../api/auth";

const Login = ({ onLogin }) => {
  const [mode, setMode] = useState("login"); // login | register
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);
  const [role, setRole] = useState("user");


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

  const handleRegister = async () => {
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    const res = await register(username, password, role);

    if (!res.success) {
      setError(res.error || "Registration failed");
      return;
    }

    alert("User created successfully. You can now log in.");
    setIsRegistering(false);
    setPassword("");
    setConfirmPassword("");
    setUsername("");
    setRole("user");
  };


  return (
    <div className="login-wrapper">
      <div className="card" style={{ width: 320 }}>
        <h2>{isRegistering ? "Create Account" : "Login"}</h2>

        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {isRegistering && (
          <input
            type="password"
            placeholder="Confirm password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        )}

        {isRegistering && (
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            style={{ marginTop: 8 }}
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        )}


        {error && (
          <div style={{ color: "var(--danger)", marginTop: 8 }}>
            {error}
          </div>
        )}

        <button
          style={{ width: "100%", marginTop: 10 }}
          onClick={isRegistering ? handleRegister : handleLogin}
        >
          {isRegistering ? "Register" : "Login"}
        </button>

        <button
          style={{
            width: "100%",
            marginTop: 8,
            background: "transparent",
            color: "var(--primary)"
          }}
          onClick={() => {
            setIsRegistering(!isRegistering);
            setError("");
          }}
        >
          {isRegistering ? "Back to login" : "Create new user"}
        </button>
      </div>

    </div>
  );
};

export default Login;
