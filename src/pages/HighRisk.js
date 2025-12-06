import React from "react";
import Sidebar from "../components/Sidebar";
import { useNavigate } from "react-router-dom";

export default function HighRisk() {
  const navigate = useNavigate();

  const riskClaims = [
    { id: "CLM-3042", score: 98, reason: "Repeated past claims" },
    { id: "CLM-1129", score: 95, reason: "Document mismatch" },
    { id: "CLM-8890", score: 92, reason: "Suspicious injury pattern" },
    { id: "CLM-5521", score: 90, reason: "High-value claim anomaly" },
    { id: "CLM-7720", score: 88, reason: "Location inconsistency" },
  ];

  return (
    <div className="page-layout">
      <Sidebar />

      <div className="page-content">
        <h2>Top 5 High-Risk Claims</h2>
        <p className="page-subtitle">Highest fraud probability identified by AI</p>

        <div className="risk-list">
          {riskClaims.map((c, i) => (
            <div
              key={i}
              className="risk-card"
              onClick={() => navigate(`/claim/${c.id}`)}   // ← CLICK = GO TO CLAIM DETAILS
              style={{ cursor: "pointer" }}
            >
              <h3>{c.id}</h3>
              <p><strong>Risk Score:</strong> {c.score}%</p>
              <p><strong>Reason:</strong> {c.reason}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Inline CSS */}
      <style>{`
        .page-layout {
          display: flex;
          background: #f5f7fb;
          min-height: 100vh;
        }
        .page-content {
          padding: 30px;
          width: 100%;
        }
        .page-subtitle {
          color: #666;
          margin-bottom: 20px;
        }
        .risk-list {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 20px;
        }
        .risk-card {
          background: white;
          padding: 20px;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.08);
          border-left: 5px solid #e63946;
          transition: transform 0.2s;
        }
        .risk-card:hover {
          transform: scale(1.02);
        }
      `}</style>
    </div>
  );
}
