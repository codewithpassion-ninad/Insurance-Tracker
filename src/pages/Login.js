import React, { useState } from "react";
import { useNavigate } from "react-router-dom";


export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Hard-coded demo credentials
    if (username === "admin" && password === "password123") {
      localStorage.setItem("gm-auth", "true");
      navigate("/admin");
      return;
    }
    setError("Invalid credentials — demo uses admin / password123");
  };

  return (
    <div className="login-container">
      {/* Floating Bubbles */}
      <div className="bubble bubble1"></div>
      <div className="bubble bubble2"></div>
      <div className="bubble bubble3"></div>
      <div className="bubble bubble4"></div>
      <div className="bubble bubble5"></div>
      <div className="bubble bubble6"></div>
      <div className="bubble bubble7"></div>
      <div className="bubble bubble8"></div>
      <div className="bubble bubble9"></div>
      <div className="bubble bubble10"></div>

      {/* Login Box */}
      <div className="login-box">
        <h2 className="login-title">Admin Login</h2>
        <p className="login-subtitle">
          Use <strong>admin</strong> / <strong>password123</strong> (demo)
        </p>
        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            className="login-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            className="login-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className="login-btn">
            Login
          </button>
          {error && <div className="login-error">{error}</div>}
        </form>
      </div>
    </div>
  );
}
