import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import DashboardCard from '../components/DashboardCard';
import ROICard from '../components/ROICard';
import { RiskPieChart, DecisionBarChart } from '../components/AnalyticsChart';
import DecisionTable from '../components/DecisionTable';
import Loader from '../components/Loader';
import { analyticsAPI, decisionAPI } from '../services/api';
import { Truck, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';
import '../styles/dashboard.css';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [analyticsRes, historyRes] = await Promise.all([
          analyticsAPI.getDashboard(),
          decisionAPI.getHistory(5)
        ]);
        setData(analyticsRes.data);
        setHistory(historyRes.data);
      } catch (err) {
        console.error("Dashboard data load failed", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <Loader text="Loading Supply Chain Intelligence..." />;

  const summary = data?.summary || {
    total_shipments: 14,
    high_risk_flagged: 4,
    recommendations_generated: 8,
    decision_adoption_rate_pct: 87.5,
    total_transit_days_saved: 42.5,
    average_roi_multiplier: 3.8
  };

  return (
    <div>
      <Navbar title="Supply Chain Operations Dashboard" />
      <div className="page-wrapper">
        <div className="dashboard-header">
          <div>
            <h1 className="dashboard-title">Closed-Loop Prescriptive Analytics</h1>
            <p className="dashboard-subtitle">Real-time XGBoost delay predictions & PuLP linear programming actions</p>
          </div>
        </div>

        <div className="stats-grid">
          <DashboardCard
            title="Active Shipments"
            value={summary.total_shipments}
            icon={Truck}
            color="#6366F1"
            subtext="Monitored in system"
          />
          <DashboardCard
            title="High Delay Risks"
            value={summary.high_risk_flagged}
            icon={AlertTriangle}
            color="#EF4444"
            subtext="XGBoost Flagged (>50%)"
          />
          <DashboardCard
            title="Prescriptions Generated"
            value={summary.recommendations_generated}
            icon={CheckCircle}
            color="#22D3EE"
            subtext="PuLP MILP Solved"
          />
          <DashboardCard
            title="Avg Intervention ROI"
            value={`${summary.average_roi_multiplier}x`}
            icon={TrendingUp}
            color="#10B981"
            subtext="Cost savings vs penalties"
          />
        </div>

        <div className="dashboard-sections-grid" style={{ marginBottom: '2rem' }}>
          <div className="glass-card">
            <h3 style={{ color: 'white', marginBottom: '1rem', fontSize: '1.1rem' }}>Disruption Risk Spectrum</h3>
            <RiskPieChart data={data?.risk_distribution} />
          </div>
          <div>
            <ROICard
              timeSaved={summary.total_transit_days_saved}
              avgRoi={summary.average_roi_multiplier}
              adoptionRate={summary.decision_adoption_rate_pct}
            />
          </div>
        </div>

        <div className="glass-card">
          <h3 style={{ color: 'white', marginBottom: '1rem', fontSize: '1.1rem' }}>Recent Decisions & Closed-Loop Feedback</h3>
          <DecisionTable history={history} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
