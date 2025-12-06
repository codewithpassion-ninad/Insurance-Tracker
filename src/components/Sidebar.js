import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Sidebar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("gm-auth");
    navigate("/login");
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-title">Admin Panel</div>
        <div className="sidebar-subtitle">Welcome back!</div>
      </div>

      <nav className="sidebar-menu">
        {/* <Link to="/admin" className="sidebar-item">Dashboard</Link>
        <Link to="/ai" className="sidebar-item">AI Agent</Link>
        <Link to="/comboai" className="sidebar-item">Advanced AI</Link> */}

        {/* NEW ITEMS */}
        <Link to="/highrisk" className="sidebar-item">Top 5 High-Risk</Link>
        {/* <Link to="/riskevaluation" className="sidebar-item">Risk Evaluation</Link> */}

        <br /><br />

        <button className="sidebar-logout" onClick={logout}>
          Logout
        </button>
      </nav>
    </aside>
  );
}
