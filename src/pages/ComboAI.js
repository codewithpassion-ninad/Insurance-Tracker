import React, { useState, useRef, useEffect } from "react";
import GrowthCard from "../components/GrowthCard";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import AIAgent from "./AIAgent";

// Sample fraud data
const fraudTrendData = [
  { name: 'Week 1', flagged: 50 },
  { name: 'Week 2', flagged: 75 },
  { name: 'Week 3', flagged: 60 },
  { name: 'Week 4', flagged: 90 },
  { name: 'Week 5', flagged: 80 },
];

const fraudCategoryData = [
  { name: 'Auto Claims', v: 45 },
  { name: 'Health Claims', v: 30 },
  { name: 'Property Claims', v: 25 },
];

export default function ComboAI() {
  const [leftWidth, setLeftWidth] = useState(600);
  const dragRef = useRef(false);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (dragRef.current) {
        const newWidth = e.clientX;
        if (newWidth > 250 && newWidth < window.innerWidth - 250) setLeftWidth(newWidth);
      }
    };
    const handleMouseUp = () => (dragRef.current = false);

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, []);

  const startDrag = () => (dragRef.current = true);

  const scrollHiddenStyle = {
    overflowY: "auto",
    msOverflowStyle: "none",
    scrollbarWidth: "none",
  };

  return React.createElement(
    "div",
    { style: { display: "flex", width: "100vw", height: "100vh", fontFamily: "Arial, sans-serif" } },

    // LEFT: Dashboard with cards & charts only
    React.createElement(
      "div",
      {
        style: {
          width: leftWidth,
          minWidth: 250,
          backgroundColor: "#f8f9fa",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          padding: 20
        }
      },

      React.createElement("h2", { style: { marginBottom: 20, color: "#004085" } }, "Fraud AI Dashboard"),

      // Cards
      React.createElement(
        "div",
        { style: { display: "flex", flexWrap: "wrap", gap: 15, marginBottom: 30 } },
        React.createElement(GrowthCard, { title: "High-Risk Claims", value: "1,248", change: 5.3 }, "Number of claims flagged as suspicious"),
        React.createElement(GrowthCard, { title: "Detection Accuracy", value: "94.1%", change: 2.7 }, "AI prediction accuracy over last month"),
        React.createElement(GrowthCard, { title: "Avg Processing Time", value: "4.2s", change: -1.1 }, "Time to analyze a claim")
      ),

      // Charts
      React.createElement(
        "div",
        { style: { display: "flex", flexWrap: "wrap", gap: 20, ...scrollHiddenStyle, flex: 1 } },

        // Line Chart
        React.createElement(
          "div",
          {
            style: {
              flex: 1,
              minWidth: 250,
              height: 300,
              backgroundColor: "#fff",
              padding: 15,
              borderRadius: 10,
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
            }
          },
          React.createElement("h4", { style: { marginBottom: 10 } }, "Flagged Claims Trend"),
          React.createElement(
            ResponsiveContainer,
            { width: "100%", height: "85%" },
            React.createElement(
              LineChart,
              { data: fraudTrendData },
              React.createElement(CartesianGrid, { strokeDasharray: "3 3" }),
              React.createElement(XAxis, { dataKey: "name" }),
              React.createElement(YAxis, null),
              React.createElement(Tooltip, null),
              React.createElement(Line, { type: "monotone", dataKey: "flagged", stroke: "#DC3545", strokeWidth: 3, dot: false })
            )
          )
        ),

        // Bar Chart
        React.createElement(
          "div",
          {
            style: {
              flex: 1,
              minWidth: 250,
              height: 300,
              backgroundColor: "#fff",
              padding: 15,
              borderRadius: 10,
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
            }
          },
          React.createElement("h4", { style: { marginBottom: 10 } }, "Claims by Category"),
          React.createElement(
            ResponsiveContainer,
            { width: "100%", height: "85%" },
            React.createElement(
              BarChart,
              { data: fraudCategoryData },
              React.createElement(CartesianGrid, { strokeDasharray: "3 3" }),
              React.createElement(XAxis, { dataKey: "name" }),
              React.createElement(YAxis, null),
              React.createElement(Tooltip, null),
              React.createElement(Bar, { dataKey: "v", fill: "#FFC107" })
            )
          )
        )
      )
    ),

    // Drag Handle
    React.createElement("div", {
      onMouseDown: startDrag,
      style: { width: 6, cursor: "col-resize", backgroundColor: "#ccc", zIndex: 10 }
    }),

    // RIGHT: AI Agent
    React.createElement(
      "div",
      { style: { flex: 1, backgroundColor: "#e6ebf1", padding: 20, ...scrollHiddenStyle } },
      React.createElement(AIAgent, null)
    )
  );
}
