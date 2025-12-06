import React from "react";

export default function MarketSparkline({ data = [2, 4, 3, 6, 8, 5, 9] }) {
  const max = Math.max(...data);

  const points = data
    .map((v, i) => {
      const x = (i / (data.length - 1)) * 100;     // spread on X axis
      const y = 40 - (v / max) * 35;               // Y scale inverted
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div className="sparkline-box">
      <svg
        width="100%"
        height="40"
        viewBox="0 0 100 40"
        preserveAspectRatio="none"
      >
        <polyline
          fill="none"
          stroke="#3A7AFE"    // GrowthMarkets blue
          strokeWidth="2"
          points={points}
        />
      </svg>
    </div>
  );
}
