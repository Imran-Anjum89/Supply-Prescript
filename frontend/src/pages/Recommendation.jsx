import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import RecommendationCard from '../components/RecommendationCard';
import Loader from '../components/Loader';
import { shipmentAPI, optimizationAPI, decisionAPI } from '../services/api';

const Recommendation = () => {
  const [shipments, setShipments] = useState([]);
  const [selectedShipment, setSelectedShipment] = useState('');
  const [maxBudget, setMaxBudget] = useState(1200);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    shipmentAPI.list().then(res => setShipments(res.data)).catch(console.error);
  }, []);

  const handleSolve = async () => {
    if (!selectedShipment) return;
    setLoading(true);
    try {
      const res = await optimizationAPI.recommend(Number(selectedShipment), Number(maxBudget));
      setRecommendation(res.data);
    } catch (err) {
      alert("Optimization solver failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDecision = async (recId, actionTaken, reason = '') => {
    try {
      await decisionAPI.submit(recId, actionTaken, reason);
      alert(`Decision ${actionTaken} successfully recorded!`);
      setRecommendation(prev => prev ? { ...prev, status: actionTaken } : null);
    } catch (err) {
      alert("Failed to record decision");
    }
  };

  return (
    <div>
      <Navbar title="PuLP MILP Prescriptive Solver" />
      <div className="page-wrapper">
        <div className="glass-card" style={{ marginBottom: '1.5rem', display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '1rem', alignItems: 'center' }}>
          <div>
            <label className="form-label">Select Target Shipment</label>
            <select className="form-input" value={selectedShipment} onChange={(e) => setSelectedShipment(e.target.value)}>
              <option value="">-- Choose Shipment --</option>
              {shipments.map(s => (
                <option key={s.id} value={s.id}>
                  {s.tracking_number} ({s.origin} → {s.destination})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="form-label">Max Intervention Budget ($)</label>
            <input type="number" className="form-input" value={maxBudget} onChange={(e) => setMaxBudget(e.target.value)} />
          </div>

          <button className="btn-primary" onClick={handleSolve} disabled={!selectedShipment || loading} style={{ marginTop: '1.4rem' }}>
            Solve MILP Strategy
          </button>
        </div>

        {loading && <Loader text="Formulating and Solving Linear Programming Model..." />}

        {recommendation && (
          <div style={{ maxWidth: '650px', margin: '0 auto' }}>
            <RecommendationCard recommendation={recommendation} onDecision={handleDecision} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Recommendation;
