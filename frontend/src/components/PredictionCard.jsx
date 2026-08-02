import React from 'react';
import { AlertTriangle, Cpu, ArrowUpRight } from 'lucide-react';

const PredictionCard = ({ prediction, onOptimize }) => {
  if (!prediction) return null;

  const getBadgeClass = (level) => {
    switch (level) {
      case 'LOW': return 'badge-low';
      case 'MEDIUM': return 'badge-medium';
      case 'HIGH': return 'badge-high';
      case 'CRITICAL': return 'badge-critical';
      default: return 'badge-low';
    }
  };

  const pct = (prediction.delay_probability * 100).toFixed(1);

  return (
    <div className="glass-card" style={{ position: 'relative', overflow: 'hidden' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.25rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Cpu size={20} color="var(--primary)" />
            <h3 style={{ color: 'white', fontSize: '1.1rem' }}>XGBoost Disruption Risk Assessment</h3>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Model Version: {prediction.model_version}
          </p>
        </div>

        <span className={`badge ${getBadgeClass(prediction.risk_level)}`}>
          {prediction.risk_level} RISK
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '12px', marginBottom: '1.25rem' }}>
        <div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Delay Probability</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: prediction.risk_level === 'HIGH' || prediction.risk_level === 'CRITICAL' ? '#F87171' : '#34D399' }}>
            {pct}%
          </div>
        </div>

        <div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Estimated Delay</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'white' }}>
            +{prediction.predicted_delay_days} Days
          </div>
        </div>
      </div>

      {prediction.feature_contributions && (
        <div style={{ marginBottom: '1.25rem' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            Top Risk Contributors
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {Object.entries(prediction.feature_contributions).slice(0, 4).map(([k, v]) => (
              <div key={k} style={{
                fontSize: '0.75rem',
                background: 'rgba(255,255,255,0.05)',
                padding: '0.3rem 0.6rem',
                borderRadius: '6px',
                border: '1px solid var(--border-color)',
                color: 'var(--text-main)'
              }}>
                <span style={{ color: 'var(--text-dim)' }}>{k.replace('_', ' ')}:</span> {v}
              </div>
            ))}
          </div>
        </div>
      )}

      {onOptimize && (
        <button
          onClick={onOptimize}
          className="btn-primary"
          style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
        >
          <span>Run PuLP Optimization Prescriptions</span>
          <ArrowUpRight size={18} />
        </button>
      )}
    </div>
  );
};

export default PredictionCard;
