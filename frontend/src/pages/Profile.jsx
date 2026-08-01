import React from 'react';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import { User, Shield, Key, Mail } from 'lucide-react';

const Profile = () => {
  const { user } = useAuth();

  return (
    <div>
      <Navbar title="User Profile & Security Settings" />
      <div className="page-wrapper">
        <div style={{ maxWidth: '600px', margin: '0 auto' }} className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-color)' }}>
            <div className="avatar" style={{ width: '60px', height: '60px', fontSize: '1.5rem' }}>
              {user?.full_name ? user.full_name.charAt(0) : 'U'}
            </div>
            <div>
              <h2 style={{ color: 'white', fontSize: '1.25rem' }}>{user?.full_name || 'Supply Chain Lead'}</h2>
              <span className="badge badge-low" style={{ marginTop: '0.2rem' }}>
                {user?.role?.toUpperCase() || 'PLANNER'}
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '10px' }}>
              <Mail size={20} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Email Address</div>
                <div style={{ color: 'white', fontWeight: 500 }}>{user?.email || 'admin@supplyprescript.com'}</div>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '10px' }}>
              <Shield size={20} color="var(--accent-cyan)" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>System Authorization Level</div>
                <div style={{ color: 'white', fontWeight: 500 }}>Full Prescriptive Interventions & Overrides</div>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '10px' }}>
              <Key size={20} color="#F59E0B" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>JWT Access Token Status</div>
                <div style={{ color: '#34D399', fontWeight: 500 }}>Authenticated & Active (HS256)</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
