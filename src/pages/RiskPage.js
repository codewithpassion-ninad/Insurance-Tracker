import React from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import 'react-circular-progressbar/dist/styles.css';

export default function RiskPage() {
  const claims = [
    { id: "CLM-1001", customer: "Alice", amount: "₹25,000", risk: 85 },
    { id: "CLM-1002", customer: "Bob", amount: "₹10,500", risk: 45 },
    { id: "CLM-1003", customer: "Charlie", amount: "₹72,300", risk: 65 },
    { id: "CLM-1004", customer: "Diana", amount: "₹8,900", risk: 20 },
    { id: "CLM-1005", customer: "Ethan", amount: "₹42,700", risk: 95 },
  ];

  const getRiskLabel = (score) => {
    if (score >= 80) return "High";
    if (score >= 50) return "Medium";
    return "Low";
  };

  const getRiskColor = (score) => {
    if (score >= 80) return "#FF3B30"; // Red for High
    if (score >= 50) return "#FF9500"; // Orange for Medium
    return "#34C759"; // Green for Low
  };

  return (
    <div className="riskpage-container">
      <h2 className="riskpage-title">Real-Time Claim Risk Evaluation</h2>
      <p className="riskpage-subtitle">
        Automated routing based on risk scores
      </p>

      <div className="riskpage-grid">
        {claims.map((c) => (
          <div key={c.id} className="riskpage-card">
            <h3 className="riskpage-claimid">{c.id}</h3>
            <p className="riskpage-customer"><strong>Customer:</strong> {c.customer}</p>
            <p className="riskpage-amount"><strong>Amount:</strong> {c.amount}</p>
            <div className="riskpage-score">
              <CircularProgressbar
                value={c.risk}
                text={`${getRiskLabel(c.risk)}`}
                styles={buildStyles({
                  textSize: '16px',
                  pathColor: getRiskColor(c.risk),
                  textColor: "#111",
                  trailColor: "#eee",
                })}
              />
            </div>
            <button
              className="riskpage-button"
              onClick={() => alert(`Claim ${c.id} routed based on risk.`)}
            >
              Process Claim
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
