import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ChatWidget from "./components/ChatWidget";

// Pages
import Home from "./pages/Home";
import Login from "./pages/Login";
import Admin from "./pages/Admin";
import AIAgent from "./pages/AIAgent";
import ComboAI from "./pages/ComboAI";
import HighRisk from "./pages/HighRisk";   // NEW
import ClaimDetails from "./pages/ClaimDetails";
import RiskEvaluation from "./pages/RiskEvaluation";

  // NEW

import './App.css';

// PrivateRoute wrapper
function PrivateRoute({ children }) {
  const isLoggedIn = localStorage.getItem("gm-auth") === "true";
  return isLoggedIn ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <div className="App">
      <Navbar />

      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />

          <Route 
            path="/admin" 
            element={
              <PrivateRoute>
                <Admin />
              </PrivateRoute>
            } 
          />

          <Route path="/ai" element={<AIAgent />} />
          <Route path="/comboai" element={<ComboAI />} />

          {/* NEW ROUTES */}
          <Route 
            path="/highrisk" 
            element={
              <PrivateRoute>
                <HighRisk />
              </PrivateRoute>
            }
          />
          <Route path="/riskevaluation" element={<RiskEvaluation />} />
          <Route 
  path="/claim/:id" 
  element={
    <PrivateRoute>
      <ClaimDetails />
    </PrivateRoute>
  }
/>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
                  

      </main>

      <Footer />
      <ChatWidget />
    </div>
  );
}

export default App;
