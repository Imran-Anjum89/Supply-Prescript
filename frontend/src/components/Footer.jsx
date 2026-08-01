import React from 'react';

const Footer = () => {
  return (
    <footer style={{
      padding: '1.5rem 2rem',
      borderTop: '1px solid var(--border-color)',
      color: 'var(--text-dim)',
      fontSize: '0.8rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginTop: 'auto'
    }}>
      <div>SupplyPrescript Control Center &copy; 2026. Closed-Loop AI Prescriptive Operations.</div>
      <div>XGBoost + PuLP MILP Engine v1.0</div>
    </footer>
  );
};

export default Footer;
