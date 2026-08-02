import React from 'react';
import { TrendingUp, DollarSign, Clock, ShieldCheck } from 'lucide-react';
import '../styles/analytics.css';

const ROICard = ({ timeSaved = 42.5, avgRoi = 3.8, adoptionRate = 88.5 }) => {
  return (
    <div className="glass-card">
      <div className="roi-card-header">
        <div>
          <h3 style={{ fontSize: '1.1rem', color: 'white' }}>Prescriptive ROI Engine</h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>PuLP Linear Programming Impact</p>
        </div>
        <div style={{ padding: '0.4rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '8px', color: 'var(--primary)' }}>
          <TrendingUp size={20} />
        </div>
      </div>

      <div style={{ margin: '1.5rem 0' }}>
        <div className="roi-big-stat">{avgRoi}x</div>
        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Average Return on Intervention Cost</div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
            <Clock size={14} color="#34D399" />
            Transit Saved
          </div>
          <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'white', marginTop: '0.2rem' }}>
            {timeSaved} Days
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
            <ShieldCheck size={14} color="#60A5FA" />
            Decision Acceptance
          </div>
          <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'white', marginTop: '0.2rem' }}>
            {adoptionRate}%
          </div>
        </div>
      </div>
    </div>
  );
};

export default ROICard;
