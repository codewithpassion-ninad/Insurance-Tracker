import React, { useState } from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import "react-circular-progressbar/dist/styles.css";

export default function RiskEvaluation() {
  const [claim, setClaim] = useState({ id: "", customer: "", amount: "" });
  const [riskScore, setRiskScore] = useState(null);
  const [riskLevel, setRiskLevel] = useState("");
  const [anomalies, setAnomalies] = useState([]);
  const [routingMessage, setRoutingMessage] = useState("");

  const anomalyPool = [
    "Multiple claims in last 60 days",
    "Document mismatch pattern",
    "Suspicious location change",
    "Unusual claim amount",
    "Past claim frequency abnormal",
  ];

  const generateRisk = () => {
    const score = Math.floor(Math.random() * 100) + 1;
    setRiskScore(score);

    if (score <= 40) setRiskLevel("Low");
    else if (score <= 70) setRiskLevel("Medium");
    else setRiskLevel("High");

    const shuffled = anomalyPool.sort(() => 0.5 - Math.random());
    setAnomalies(shuffled.slice(0, 3));

    if (score <= 40) setRoutingMessage("Claim routed to Standard Processing ✅");
    else if (score <= 70) setRoutingMessage("Claim forwarded to Analyst Review ⚠️");
    else setRoutingMessage("High Risk! Sent to Fraud Investigation Unit 🚨");
  };

  const sampleChartData = [
    { stage: "Submitted", claims: 10 },
    { stage: "Reviewed", claims: 7 },
    { stage: "In Investigation", claims: 3 },
    { stage: "Approved", claims: 5 },
  ];

  return (
    <div className="riskpage-container">
      <h2 className="riskpage-title">Real-Time Risk Evaluation</h2>
      <p className="riskpage-subtitle">Simulate risk scoring and automated routing for claims</p>

      {/* Claim Form */}
      <div className="riskpage-form">
        <h3>Claim Details</h3>
        <div className="riskpage-form-row">
          <input
            type="text"
            placeholder="Claim ID"
            value={claim.id}
            onChange={(e) => setClaim({ ...claim, id: e.target.value })}
          />
          <input
            type="text"
            placeholder="Customer Name"
            value={claim.customer}
            onChange={(e) => setClaim({ ...claim, customer: e.target.value })}
          />
          <input
            type="text"
            placeholder="Claim Amount"
            value={claim.amount}
            onChange={(e) => setClaim({ ...claim, amount: e.target.value })}
          />
          <button onClick={generateRisk}>Generate Risk Score</button>
        </div>
      </div>

      {/* Risk Score + Routing */}
      {riskScore !== null && (
        <div className="riskpage-result">
          <div className="riskpage-score-card">
            <h3>Risk Score</h3>
            <CircularProgressbar
              value={riskScore}
              text={`${riskScore}%`}
              styles={buildStyles({
                textColor: "#333",
                pathColor:
                  riskLevel === "Low"
                    ? "#34C759"
                    : riskLevel === "Medium"
                    ? "#FF9500"
                    : "#FF3B30",
                trailColor: "#d6d6d6",
              })}
            />
            <p className={`riskpage-risklevel riskpage-${riskLevel.toLowerCase()}`}>
              {riskLevel} Risk
            </p>
          </div>

          <div className="riskpage-routing-card">
            <h3>Automated Routing</h3>
            <p>{routingMessage}</p>

            {anomalies.length > 0 && (
              <>
                <h4>Detected Anomalies:</h4>
                <ul>
                  {anomalies.map((a, i) => (
                    <li key={i}>{a}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        </div>
      )}

      {/* Sample Chart */}
      <div className="riskpage-chart">
        <h3>Claims Progression</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={sampleChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="stage" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="claims" fill="#3A7AFE" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
