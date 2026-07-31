import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Bell, Search, ShieldCheck } from 'lucide-react';

const Navbar = ({ title = "Dashboard" }) => {
  const { user } = useAuth();

  return (
    <header className="navbar" style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '1rem 2rem',
      borderBottom: '1px solid var(--border-color)',
      background: 'rgba(13, 17, 27, 0.7)',
      backdropFilter: 'blur(10px)'
    }}>
      <div>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'white' }}>{title}</h2>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.4rem 0.8rem',
          background: 'rgba(16, 185, 129, 0.1)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          borderRadius: '20px',
          color: '#34D399',
          fontSize: '0.8rem',
          fontWeight: 600
        }}>
          <ShieldCheck size={16} />
          XGBoost & PuLP MILP Active
        </div>

        <button style={{
          background: 'rgba(255, 255, 255, 0.05)',
          border: '1px solid var(--border-color)',
          borderRadius: '50%',
          width: '36px',
          height: '36px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--text-muted)'
        }}>
          <Bell size={18} />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div className="avatar">
            {user?.full_name ? user.full_name.charAt(0) : 'U'}
          </div>
          <div style={{ fontSize: '0.85rem' }}>
            <div style={{ color: 'white', fontWeight: 600 }}>{user?.full_name || 'User'}</div>
            <div style={{ color: 'var(--text-dim)', fontSize: '0.75rem' }}>{user?.role || 'Planner'}</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
