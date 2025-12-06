import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-logo">
        <Link to="/" className="navbar-brand">EricAI IFDS</Link>
      </div>

      <nav className="navbar-links">
        <Link to="/" className="nav-item">Home</Link>
        <Link to="/login" className="nav-item">Login</Link>
        <Link to="/admin" className="nav-item">Admin</Link>
        {/* <Link to="/ai" className="nav-item">AI Agent</Link>
        <Link to="/comboai" className="nav-item">Advance AI</Link> */}



      </nav>
    </header>
  );
}
