import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import DashboardCard from '../components/DashboardCard';
import { RiskPieChart, DecisionBarChart } from '../components/AnalyticsChart';
import ROICard from '../components/ROICard';
import Loader from '../components/Loader';
import { analyticsAPI, retrainingAPI } from '../services/api';
import { RefreshCw, BarChart2, Shield, Activity } from 'lucide-react';

const Analytics = () => {
  const [data, setData] = useState(null);
  const [modelStatus, setModelStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);

  const fetchAnalytics = async () => {
    try {
      const [res, modelRes] = await Promise.all([
        analyticsAPI.getAnalytics(),
        retrainingAPI.getModelStatus()
      ]);
      setData(res.data);
      setModelStatus(modelRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    try {
      const res = await retrainingAPI.trigger();
      alert(`Model retrained successfully! Version: ${res.data.retraining_log.version}`);
      fetchAnalytics();
    } catch (err) {
      alert("Retraining failed");
    } finally {
      setRetraining(false);
    }
  };

  if (loading) return <Loader text="Aggregating Supply Chain Performance Metrics..." />;

  const summary = data?.summary || {};

  return (
    <div>
      <Navbar title="Closed-Loop Analytics & Retraining Studio" />
      <div className="page-wrapper">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <div>
            <h1 className="dashboard-title">System Intelligence Overview</h1>
            <p className="dashboard-subtitle">Closed-Loop Model Evaluation & PuLP Optimization Metrics</p>
          </div>

          <button
            className="btn-primary"
            onClick={handleRetrain}
            disabled={retraining}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)' }}
          >
            <RefreshCw size={18} className={retraining ? 'spin' : ''} />
            {retraining ? "Retraining XGBoost Model..." : "Trigger Model Retraining"}
          </button>
        </div>

        <div className="stats-grid">
          <DashboardCard title="Active Model Version" value={modelStatus?.model_version || 'v1.0'} icon={Shield} color="#A855F7" subtext="XGBoost Classifier + Regressor" />
          <DashboardCard title="Model Accuracy" value={`${((modelStatus?.accuracy || 0.91) * 100).toFixed(1)}%`} icon={Activity} color="#10B981" subtext="Validation ROC-AUC / F1" />
          <DashboardCard title="Mean Absolute Error" value={`${modelStatus?.mae || 1.15} days`} icon={BarChart2} color="#22D3EE" subtext="Delay magnitude variance" />
        </div>

        <div className="analytics-grid">
          <div className="glass-card">
            <h3 style={{ color: 'white', marginBottom: '1rem', fontSize: '1.1rem' }}>Disruption Risk Breakdown</h3>
            <RiskPieChart data={data?.risk_distribution} />
          </div>

          <div className="glass-card">
            <h3 style={{ color: 'white', marginBottom: '1rem', fontSize: '1.1rem' }}>Human Decision Distribution</h3>
            <DecisionBarChart data={data?.decision_breakdown} />
          </div>
        </div>

        <div className="dashboard-sections-grid">
          <ROICard timeSaved={summary.total_transit_days_saved} avgRoi={summary.average_roi_multiplier} adoptionRate={summary.decision_adoption_rate_pct} />

          <div className="glass-card">
            <h3 style={{ color: 'white', marginBottom: '0.75rem', fontSize: '1.1rem' }}>Carrier Reliability Index</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {data?.carrier_breakdown?.map(c => (
                <div key={c.carrier} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.6rem 0.8rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', fontSize: '0.85rem' }}>
                  <span style={{ color: 'white', fontWeight: 500 }}>{c.carrier}</span>
                  <span style={{ color: 'var(--text-muted)' }}>{c.count} shipments</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
