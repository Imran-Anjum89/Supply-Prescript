import React, { useState } from 'react';
import { PlusCircle, Send } from 'lucide-react';

const ShipmentForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    origin: 'Shanghai',
    destination: 'Los Angeles',
    carrier: 'Maersk Line',
    transit_days: 18,
    quantity: 500,
    total_cost: 4500,
    weather_risk_score: 0.65,
    traffic_risk_score: 0.40,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name.includes('score') || name.includes('days') || name.includes('cost') || name === 'quantity'
        ? Number(value)
        : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="glass-card">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.25rem' }}>
        <PlusCircle size={20} color="var(--primary)" />
        <h3 style={{ color: 'white', fontSize: '1.1rem' }}>Register New Shipment</h3>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div className="form-group">
          <label className="form-label">Origin Port/Hub</label>
          <input
            type="text"
            name="origin"
            className="form-input"
            value={formData.origin}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Destination</label>
          <input
            type="text"
            name="destination"
            className="form-input"
            value={formData.destination}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Logistics Carrier</label>
          <select name="carrier" className="form-input" value={formData.carrier} onChange={handleChange}>
            <option value="Maersk Line">Maersk Line (Sea)</option>
            <option value="DHL Express">DHL Express (Air)</option>
            <option value="FedEx Supply Chain">FedEx Express (Air)</option>
            <option value="OceanNet Logistics">OceanNet Logistics (Sea)</option>
            <option value="Global Freight Air">Global Freight Air</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Planned Transit Days</label>
          <input
            type="number"
            name="transit_days"
            className="form-input"
            value={formData.transit_days}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Cargo Quantity (Units)</label>
          <input
            type="number"
            name="quantity"
            className="form-input"
            value={formData.quantity}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Total Freight Cost ($)</label>
          <input
            type="number"
            name="total_cost"
            className="form-input"
            value={formData.total_cost}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Weather Risk Index (0.0 to 1.0)</label>
          <input
            type="number"
            step="0.05"
            min="0"
            max="1"
            name="weather_risk_score"
            className="form-input"
            value={formData.weather_risk_score}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Traffic/Port Risk Index (0.0 to 1.0)</label>
          <input
            type="number"
            step="0.05"
            min="0"
            max="1"
            name="traffic_risk_score"
            className="form-input"
            value={formData.traffic_risk_score}
            onChange={handleChange}
          />
        </div>
      </div>

      <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%', marginTop: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
        <Send size={18} />
        {loading ? "Registering & Analyzing..." : "Create Shipment & Evaluate Risk"}
      </button>
    </form>
  );
};

export default ShipmentForm;
