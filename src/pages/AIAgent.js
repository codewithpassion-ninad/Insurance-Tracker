import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function AIAgent() {
  const location = useLocation();
  const navigate = useNavigate();

  const { claimId, documents } = location.state || {};
  const [result, setResult] = useState("");
  const [selectedFiles, setSelectedFiles] = useState([]);

  // REDIRECT IF NOT LOGGED IN
  useEffect(() => {
    const loggedIn = localStorage.getItem("gm-auth") === "true";
    if (!loggedIn) navigate("/login?redirect=/ai");
  }, [navigate]);

  // AUTO-LOAD PDF FILES RECEIVED FROM ClaimDetails
  useEffect(() => {
    async function loadPDFFiles() {
      if (!documents) return;

      const loadedFiles = [];

      for (let url of documents) {
        const response = await fetch(url);
        const blob = await response.blob();
        const filename = url.split("/").pop();

        const fileObj = new File([blob], filename, { type: "application/pdf" });
        loadedFiles.push(fileObj);
      }

      setSelectedFiles(loadedFiles);
    }

    loadPDFFiles();
  }, [documents]);

  // PROCESS CLAIM
  const processClaim = async () => {
    if (!claimId) return;

    const formData = new FormData();
    const claimData = { claim_id: claimId };

    formData.append("claim_data", JSON.stringify(claimData));
    formData.append("policy_text", "Your policy text here");
    formData.append("employee_csv", "/data/employee_db.csv");

    selectedFiles.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await fetch("http://localhost:8000/evaluate", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Backend error");

      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setResult("Error: " + err.message);
      console.error(err);
    }
  };

  return (
    <div className="ai-page">
      <div className="ai-header"><br /></div>

      <div className="ai-box">
        <h3>AI Agent for Claim: {claimId || "No claim selected"}</h3>

        {/* Show Loaded PDF Files */}
        <div style={{ marginTop: "15px" }}>
          <h4>Attached Documents:</h4>
          <ul>
            {selectedFiles.map((file, idx) => (
              <li key={idx}>{file.name}</li>
            ))}
          </ul>
        </div>

        <div className="ai-input-row" style={{ marginTop: "20px" }}>
          <button onClick={processClaim}>Process Claim</button>
        </div>

        {result && (
          <div className="ai-messages" style={{ marginTop: "20px" }}>
            <div className="ai-msg bot">
              <h4>AI Output</h4>
              <pre style={{ whiteSpace: "pre-wrap" }}>{result}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
