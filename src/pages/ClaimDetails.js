import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function ClaimDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [claimData, setClaimData] = useState(null);

  useEffect(() => {
    const allClaims = {
      "CLM-3042": {
        documents: [
          "/data/consultation/letter1.pdf",
          "/data/discharge/ds1.pdf",
          "/data/bill1.pdf",
        ],
      },
      "CLM-1129": {
        documents: [
          "/data/consultation/letter2.pdf",
          "/data/discharge/ds2.pdf",
          "/data/bill/bill2.pdf",
        ],
      },
      "CLM-8890": {
        documents: [
          "/data/consultation/letter3.pdf",
          "/data/discharge/ds3.pdf",
          "/data/bill/bill3.pdf",
        ],
      },
      "CLM-5521": {
        documents: [
          "/data/consultation/letter4.pdf",
          "/data/discharge/ds4.pdf",
          "/data/bill/bill4.pdf",
        ],
      },
    };

    const data = allClaims[id];
    if (data) setClaimData({ id, ...data });
  }, [id]);

  const goToAIAgent = () => {
    if (!claimData) return;
    navigate("/ai", { state: { claimId: claimData.id, documents: claimData.documents } });
  };

  if (!claimData) return <p>Loading...</p>;

  return (
    <div style={{ padding: "40px", background: "#f5f7fb", minHeight: "100vh" }}>
      <div
        style={{
          padding: "25px",
          background: "white",
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
        }}
      >
        <h2>Claim ID: {claimData.id}</h2>

        <h3 style={{ marginTop: "30px", marginBottom: "15px" }}>Attached Documents</h3>

        <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
          {claimData.documents.map((pdf, index) => (
            <div
              key={index}
              style={{
                padding: "18px",
                background: "white",
                borderRadius: "10px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                borderLeft: "5px solid #005BBB",
              }}
            >
              <div>
                <p style={{ margin: 0, fontSize: "15px" }}>
                  <strong>Document {index + 1}</strong>
                </p>
                <p style={{ margin: "4px 0 0", color: "#666", fontSize: "14px" }}>
                  {pdf.split("/").pop()}
                </p>
              </div>

              <a
                href={pdf}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: "white",
                  background: "#005BBB",
                  padding: "10px 20px",
                  borderRadius: "8px",
                  textDecoration: "none",
                  fontWeight: "500",
                  fontSize: "14px",
                }}
              >
                View PDF
              </a>
            </div>
          ))}
        </div>

        <button
          onClick={goToAIAgent}
          style={{
            marginTop: "30px",
            padding: "12px 25px",
            background: "#005BBB",
            color: "white",
            border: "none",
            borderRadius: "8px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Process with AI →
        </button>
      </div>
    </div>
  );
}
