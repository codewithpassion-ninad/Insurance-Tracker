import React from "react";
import Sidebar from "../components/Sidebar";
import GrowthCard from "../components/GrowthCard";

import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

// --------- DATA ---------
const claimsData = [
  { claim_id: 1, claim_type: "Maternity", claim_amount: 92384, raw_fraud_score: 0.05, policy_plan: 0 },
  { claim_id: 2, claim_type: "Maternity", claim_amount: 70160, raw_fraud_score: 0.05, policy_plan: 2 },
  { claim_id: 3, claim_type: "Outpatient", claim_amount: 130272, raw_fraud_score: 0.03, policy_plan: 2 },
  { claim_id: 4, claim_type: "Accident", claim_amount: 101860, raw_fraud_score: 0.04, policy_plan: 0 },
  { claim_id: 5, claim_type: "Hospitalization", claim_amount: 58780, raw_fraud_score: 0.02, policy_plan: 0 },
  { claim_id: 6, claim_type: "Maternity", claim_amount: 58699, raw_fraud_score: 0.04, policy_plan: 0 },
  { claim_id: 7, claim_type: "Outpatient", claim_amount: 39550, raw_fraud_score: 0.01, policy_plan: 0 },
  { claim_id: 8, claim_type: "Hospitalization", claim_amount: 85998, raw_fraud_score: 0.22, policy_plan: 1 },
  { claim_id: 9, claim_type: "Accident", claim_amount: 77363, raw_fraud_score: 0.02, policy_plan: 1 },
  { claim_id: 10, claim_type: "Outpatient", claim_amount: 25133, raw_fraud_score: 0.03, policy_plan: 1 },
];

// --------- Helper Functions ---------
const sumClaimAmountByPolicyPlan = () => {
  const map = {};
  claimsData.forEach((c) => {
    if (!map[c.policy_plan]) map[c.policy_plan] = 0;
    map[c.policy_plan] += c.claim_amount;
  });
  return Object.keys(map).map((plan) => ({ plan: `Plan ${plan}`, total: map[plan] }));
};

const countClaimsByType = () => {
  const map = {};
  claimsData.forEach((c) => {
    if (!map[c.claim_type]) map[c.claim_type] = 0;
    map[c.claim_type] += 1;
  });
  return Object.keys(map).map((type) => ({ type, count: map[type] }));
};

const topHighRiskClaims = claimsData
  .sort((a, b) => b.raw_fraud_score - a.raw_fraud_score)
  .slice(0, 5)
  .map((c) => ({ claim_id: `Claim ${c.claim_id}`, risk: c.raw_fraud_score * 100 }));

// --------- Admin Component ---------
export default function Admin() {
  const policyPlanData = sumClaimAmountByPolicyPlan();
  const claimTypeData = countClaimsByType();

  return (
    <div>
      <br />
      <br />
      <div className="admin-dashboard">
        <div className="ad-flex">
          <Sidebar className="ad-sidebar" />
          <div className="ad-main-content">
            <div className="ad-header">
              <h2 className="ad-header-title">Dashboard</h2>
              <div className="ad-header-subtitle">Welcome, Admin</div>
            </div>

            <div className="ad-cards-grid">
              <GrowthCard title="Total Claims" value={claimsData.length} change={claimsData.length}>
                Number of processed claims
              </GrowthCard>
              <GrowthCard
                title="Total Claim Amount"
                value={`₹${claimsData.reduce((a, c) => a + c.claim_amount, 0)}`}
                change={claimsData.length}
              >
                Sum of all claims
              </GrowthCard>
              <GrowthCard title="High Risk Claims" value={topHighRiskClaims.length} change={topHighRiskClaims.length}>
                Top fraud risk
              </GrowthCard>
            </div>

            {/* Charts */}
            <div className="ad-charts-grid">
              <div className="ad-chart-card">
                <h3 className="ad-chart-title">Claims by Type</h3>
                <div className="ad-chart-container">
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={claimTypeData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="type" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3A7AFE" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="ad-chart-card">
                <h3 className="ad-chart-title">Total Claim Amount by Policy Plan</h3>
                <div className="ad-chart-container">
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={policyPlanData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="plan" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="total" fill="#F6C90E" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="ad-chart-card">
                <h3 className="ad-chart-title">Top 5 High-Risk Claims</h3>
                <div className="ad-chart-container">
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={topHighRiskClaims}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="claim_id" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="risk" fill="#FF3B30" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
