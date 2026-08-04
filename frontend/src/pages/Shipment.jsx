import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import ShipmentForm from '../components/ShipmentForm';
import Loader from '../components/Loader';
import { shipmentAPI, predictionAPI, optimizationAPI } from '../services/api';
import PredictionCard from '../components/PredictionCard';
import RecommendationCard from '../components/RecommendationCard';
import { decisionAPI } from '../services/api';

const Shipment = () => {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selectedPrediction, setSelectedPrediction] = useState(null);
  const [selectedRecommendation, setSelectedRecommendation] = useState(null);
  const [selectedShipmentId, setSelectedShipmentId] = useState(null);

  const fetchShipments = async () => {
    try {
      const res = await shipmentAPI.list();
      setShipments(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchShipments();
  }, []);

  const handleCreateShipment = async (formData) => {
    setSubmitting(true);
    try {
      const res = await shipmentAPI.create(formData);
      const newShipment = res.data;
      
      // Auto trigger prediction
      const predRes = await predictionAPI.predict(newShipment.id);
      setSelectedPrediction(predRes.data);
      setSelectedShipmentId(newShipment.id);

      // Auto trigger optimization recommendation
      const recRes = await optimizationAPI.recommend(newShipment.id);
      setSelectedRecommendation(recRes.data);

      await fetchShipments();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDecision = async (recId, actionTaken, reason = '') => {
    try {
      await decisionAPI.submit(recId, actionTaken, reason);
      alert(`Decision ${actionTaken} successfully recorded in PostgreSQL write-back!`);
      setSelectedRecommendation(prev => prev ? { ...prev, status: actionTaken } : null);
      fetchShipments();
    } catch (err) {
      alert("Failed to submit decision");
    }
  };

  if (loading) return <Loader text="Loading Shipment Records..." />;

  return (
    <div>
      <Navbar title="Shipment Management & Real-Time Prescriptions" />
      <div className="page-wrapper">
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
          <div>
            <ShipmentForm onSubmit={handleCreateShipment} loading={submitting} />
          </div>

          <div>
            {selectedPrediction ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <PredictionCard prediction={selectedPrediction} />
                {selectedRecommendation && (
                  <RecommendationCard recommendation={selectedRecommendation} onDecision={handleDecision} />
                )}
              </div>
            ) : (
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '380px', color: 'var(--text-dim)', textAlign: 'center' }}>
                <div style={{ fontSize: '1.1rem', color: 'white', fontWeight: 600, marginBottom: '0.5rem' }}>
                  Live Risk & Prescriptive Output
                </div>
                <p style={{ maxWidth: '300px', fontSize: '0.85rem' }}>
                  Register a shipment on the left form to evaluate XGBoost delay probabilities and solve PuLP prescriptive interventions in real time.
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="glass-card">
          <h3 style={{ color: 'white', marginBottom: '1rem', fontSize: '1.1rem' }}>Registered Logistics Shipments</h3>
          <div className="custom-table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Tracking #</th>
                  <th>Origin → Destination</th>
                  <th>Carrier</th>
                  <th>Transit Days</th>
                  <th>Freight Cost</th>
                  <th>Weather/Traffic Risk</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {shipments.map((s) => (
                  <tr key={s.id}>
                    <td style={{ fontWeight: 600, color: 'var(--primary)' }}>{s.tracking_number}</td>
                    <td>{s.origin} → {s.destination}</td>
                    <td>{s.carrier}</td>
                    <td>{s.transit_days} d</td>
                    <td>${s.total_cost}</td>
                    <td>
                      <span style={{ color: s.weather_risk_score > 0.5 ? '#F87171' : '#34D399' }}>
                        W: {(s.weather_risk_score * 100).toFixed(0)}%
                      </span> / <span style={{ color: s.traffic_risk_score > 0.5 ? '#F87171' : '#34D399' }}>
                        T: {(s.traffic_risk_score * 100).toFixed(0)}%
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${s.status === 'DELAY_RISK' ? 'badge-high' : 'badge-low'}`}>
                        {s.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Shipment;
