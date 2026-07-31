import React from 'react';
import '../styles/dashboard.css';

const DashboardCard = ({ title, value, icon: Icon, color = "var(--primary)", subtext }) => {
  return (
    <div className="stat-card glass-card">
      <div className="stat-icon" style={{ background: `${color}15`, color }}>
        {Icon && <Icon size={24} />}
      </div>
      <div>
        <div className="stat-val">{value}</div>
        <div className="stat-lbl">{title}</div>
        {subtext && <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '0.2rem' }}>{subtext}</div>}
      </div>
    </div>
  );
};

export default DashboardCard;
