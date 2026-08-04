import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import PredictionCard from '../components/PredictionCard';
import Loader from '../components/Loader';
import { shipmentAPI, predictionAPI, optimizationAPI } from '../services/api';

const Prediction = () => {
  const [shipments, setShipments] = useState([]);
  const [selectedShipment, setSelectedShipment] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    shipmentAPI.list().then(res => setShipments(res.data)).catch(console.error);
  }, []);

  const handlePredict = async () => {
    if (!selectedShipment) return;
    setLoading(true);
    try {
      const res = await predictionAPI.predict(Number(selectedShipment));
      setPrediction(res.data);
    } catch (err) {
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar title="XGBoost Disruption Risk Predictor" />
      <div className="page-wrapper">
        <div className="glass-card" style={{ marginBottom: '1.5rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ flex: 1 }}>
            <label className="form-label">Select Shipment for Disruption Assessment</label>
            <select className="form-input" value={selectedShipment} onChange={(e) => setSelectedShipment(e.target.value)}>
              <option value="">-- Choose Shipment --</option>
              {shipments.map(s => (
                <option key={s.id} value={s.id}>
                  {s.tracking_number} ({s.origin} → {s.destination} | {s.carrier})
                </option>
              ))}
            </select>
          </div>
          <button className="btn-primary" onClick={handlePredict} disabled={!selectedShipment || loading} style={{ marginTop: '1.4rem' }}>
            Evaluate Risk Model
          </button>
        </div>

        {loading && <Loader text="Executing XGBoost Inference Model..." />}

        {prediction && (
          <div style={{ maxWidth: '650px', margin: '0 auto' }}>
            <PredictionCard prediction={prediction} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Prediction;
