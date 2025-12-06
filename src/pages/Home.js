import React from "react";
import GrowthCard from "../components/GrowthCard";
import { Link } from "react-router-dom";

export default function Home() {
  const cards = [
    {
      title: "Detect Fraudulent Claims",
      value: "Identify anomalies",
      desc: "AI scans claims for inconsistencies and potential fraud.",
    },
    {
      title: "Claim Analysis",
      value: "Comprehensive Reports",
      desc: "Highlights missing or mismatched documents and risk indicators.",
    },
    {
      title: "Risk Monitoring",
      value: "High-Risk Alerts",
      desc: "Flags suspicious claims across hospitals, doctors, and employees.",
    },
  ];

  return (
    <div className="home-container theme-ai" style={{ paddingTop: "80px" }}>
      {/* HERO SECTION */}
      <div className="hero-box ai-hero">
        <div className="hero-content">
          <div className="hero-left">
            <h1 className="hero-title">EricAI IFDS Care</h1>
            <p className="hero-subtitle">
              AI for automated detection of fraudulent insurance claims.
              <br />
              Detect anomalies and reduce financial risk instantly.
            </p>
            <div className="hero-buttons">
              <Link to="/login">
                <button className="btn-primary">Login</button>
              </Link>
            </div>
          </div>

          {/* FRAUD-AI NODE NETWORK VISUAL */}
          <div className="hero-graph">
            <svg width="260" height="200" viewBox="0 0 260 200">
              <circle cx="50" cy="150" r="10" fill="#005BBB" opacity="0.9" />
              <circle cx="120" cy="90" r="12" fill="#008C9E" opacity="0.9" />
              <circle cx="200" cy="140" r="10" fill="#4C9A2A" opacity="0.9" />
              <circle cx="180" cy="60" r="8" fill="#CC5500" opacity="0.9" />
              <circle cx="90" cy="40" r="9" fill="#005BBB" opacity="0.9" />
              <line x1="50" y1="150" x2="120" y2="90" stroke="#005BBB" strokeWidth="3" opacity="0.7" />
              <line x1="120" y1="90" x2="200" y2="140" stroke="#008C9E" strokeWidth="3" opacity="0.7" />
              <line x1="120" y1="90" x2="180" y2="60" stroke="#4C9A2A" strokeWidth="3" opacity="0.7" />
              <line x1="90" y1="40" x2="180" y2="60" stroke="#CC5500" strokeWidth="3" opacity="0.7" />
              <circle
                cx="120"
                cy="90"
                r="18"
                fill="none"
                stroke="#005BBB"
                strokeWidth="2"
                opacity="0.3"
              >
                <animate attributeName="r" from="12" to="30" dur="2s" repeatCount="indefinite" />
                <animate attributeName="opacity" from="0.5" to="0" dur="2s" repeatCount="indefinite" />
              </circle>
            </svg>
          </div>
        </div>
      </div>

      {/* METRIC CARDS */}
      <div id="cards" className="cards-grid">
        {cards.map((c, i) => (
          <GrowthCard key={i} title={c.title} value={c.value}>
            {c.desc}
          </GrowthCard>
        ))}
      </div>

      {/* TREND AREA */}
      <div
        style={{
          padding: "25px",
          background: "#f0f4f8",
          borderRadius: "15px",
          boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
          marginTop: "25px",
          fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          transition: "all 0.3s ease",
        }}
      >
        <h3
          style={{
            marginBottom: "16px",
            background: "linear-gradient(90deg, #005BBB, #008C9E)",
            WebkitBackgroundClip: "text",
            color: "transparent",
            fontSize: "1.5rem",
            fontWeight: "700",
          }}
        >
          AI Fraud Insights
        </h3>

        <p style={{ color: "#333", lineHeight: "1.5", fontSize: "1rem", marginBottom: "20px" }}>
          AI analyzes claims to detect anomalies, inconsistencies, and risks. Key insights include:
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "16px",
          }}
        >
          <div
            style={{
              background: "#ffffff",
              borderRadius: "12px",
              padding: "15px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              transition: "transform 0.3s",
              cursor: "default",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-5px)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0px)")}
          >
            <h4 style={{ marginBottom: "8px", color: "#005BBB", fontWeight: "600" }}>
              Claim Types
            </h4>
            <p style={{ fontSize: "0.9rem", color: "#555" }}>
              Shows trends in Hospitalization, Surgery, Outpatient claims.
            </p>
          </div>

          <div
            style={{
              background: "#ffffff",
              borderRadius: "12px",
              padding: "15px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              transition: "transform 0.3s",
              cursor: "default",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-5px)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0px)")}
          >
            <h4 style={{ marginBottom: "8px", color: "#005BBB", fontWeight: "600" }}>
              Hospital Activity
            </h4>
            <p style={{ fontSize: "0.9rem", color: "#555" }}>
              Monitors claims per hospital and flags unusual spikes.
            </p>
          </div>

          <div
            style={{
              background: "#ffffff",
              borderRadius: "12px",
              padding: "15px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              transition: "transform 0.3s",
              cursor: "default",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-5px)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0px)")}
          >
            <h4 style={{ marginBottom: "8px", color: "#005BBB", fontWeight: "600" }}>
              High-Risk Claims
            </h4>
            <p style={{ fontSize: "0.9rem", color: "#555" }}>
              Flags claims with anomalies or missing sections for review.
            </p>
          </div>

          <div
            style={{
              background: "#ffffff",
              borderRadius: "12px",
              padding: "15px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              transition: "transform 0.3s",
              cursor: "default",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-5px)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0px)")}
          >
            <h4 style={{ marginBottom: "8px", color: "#005BBB", fontWeight: "600" }}>
              Anomaly Patterns
            </h4>
            <p style={{ fontSize: "0.9rem", color: "#555" }}>
              Detects unusual activity across employees, doctors, and policy plans.
            </p>
          </div>
        </div>

        <p style={{ marginTop: "20px", color: "#666", fontSize: "0.9rem", lineHeight: "1.5" }}>
          Helps teams identify fraud quickly and prioritize investigations.
        </p>
      </div>
    </div>
  );
}
