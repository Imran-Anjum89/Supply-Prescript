import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import Shipment from './pages/Shipment';
import Prediction from './pages/Prediction';
import Recommendation from './pages/Recommendation';
import Analytics from './pages/Analytics';
import DecisionHistory from './pages/DecisionHistory';
import Feedback from './pages/Feedback';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import { canAccessPath, normalizeRole } from './utils/rbac';
import { ShieldAlert } from 'lucide-react';
import './styles/global.css';

const AccessDenied = ({ path }) => {
  const { user } = useAuth();
  const role = normalizeRole(user?.role);
  return (
    <div style={{ padding: '3rem 2rem', textAlign: 'center', maxWidth: '600px', margin: '3rem auto' }} className="glass-card">
      <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'rgba(239, 68, 68, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem auto' }}>
        <ShieldAlert size={34} color="#EF4444" />
      </div>
      <h2 style={{ color: 'white', fontSize: '1.35rem', marginBottom: '0.5rem' }}>Access Restricted</h2>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.25rem' }}>
        Your account role <span className="badge badge-low">{role}</span> is not authorized to perform actions on <code>{path}</code>.
      </p>
      <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', fontSize: '0.85rem', color: 'var(--text-dim)', marginBottom: '1.5rem' }}>
        Each role has dedicated system responsibilities to ensure segregation of operational duties.
      </div>
      <a href="/" className="btn-primary" style={{ display: 'inline-block', textDecoration: 'none', padding: '0.75rem 1.5rem' }}>
        Return to Authorized Dashboard
      </a>
    </div>
  );
};

const RoleProtectedWrapper = ({ path, element }) => {
  const { user } = useAuth();
  const allowed = canAccessPath(user?.role, path);
  return allowed ? element : <AccessDenied path={path} />;
};

const ProtectedLayout = () => {
  const { user, loading } = useAuth();

  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<RoleProtectedWrapper path="/" element={<Dashboard />} />} />
          <Route path="/shipments" element={<RoleProtectedWrapper path="/shipments" element={<Shipment />} />} />
          <Route path="/predictions" element={<RoleProtectedWrapper path="/predictions" element={<Prediction />} />} />
          <Route path="/recommendations" element={<RoleProtectedWrapper path="/recommendations" element={<Recommendation />} />} />
          <Route path="/analytics" element={<RoleProtectedWrapper path="/analytics" element={<Analytics />} />} />
          <Route path="/history" element={<RoleProtectedWrapper path="/history" element={<DecisionHistory />} />} />
          <Route path="/feedback" element={<RoleProtectedWrapper path="/feedback" element={<Feedback />} />} />
          <Route path="/profile" element={<RoleProtectedWrapper path="/profile" element={<Profile />} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <Footer />
      </div>
    </div>
  );
};

const App = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/*" element={<ProtectedLayout />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
