import React from "react";

export default function GrowthCard({ title, value, change, data = [], children }) {
  const up = change >= 0;

  // Inline Styles
  const cardStyle = {
    background: "#ffffff",
    border: "1px solid #DDE3EA",
    borderRadius: "12px",
    padding: "16px",
    minWidth: "260px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
    marginBottom: "20px",
  };

  const cardTitleStyle = {
    fontSize: "1rem",
    fontWeight: 600,
    color: "#005BBB",
    marginBottom: "4px",
  };

  const cardValueStyle = {
    fontSize: "1.4rem",
    fontWeight: 700,
    color: "#1A1A1A",
  };

  const cardChangeStyle = {
    fontSize: "1rem",
    fontWeight: 600,
    color: up ? "#4C9A2A" : "#CC5500",
  };

  const cardDescStyle = {
    marginTop: "10px",
    fontSize: "0.9rem",
    color: "#444444",
    lineHeight: "1.5",
  };

  const sparklineStyle = {
    marginTop: "10px",
    width: "100%",
    height: "40px",
  };

  // Prepare points for sparkline
  const max = Math.max(...data, 1); // avoid divide by zero
  const points = data
    .map((v, i) => {
      const x = (i / (data.length - 1)) * 100;
      const y = 40 - (v / max) * 35;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div style={cardStyle}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <div style={cardTitleStyle}>{title}</div>
          <div style={cardValueStyle}>{value}</div>
        </div>
        <div style={cardChangeStyle}>
          {up ? "↑" : "↓"} {Math.abs(change)}%
        </div>
      </div>

      <div style={cardDescStyle}>{children}</div>

      {data.length > 0 && (
        <svg viewBox="0 0 100 40" preserveAspectRatio="none" style={sparklineStyle}>
          <polyline
            fill="none"
            stroke="#005BBB"
            strokeWidth="2"
            points={points}
          />
        </svg>
      )}
    </div>
  );
}
