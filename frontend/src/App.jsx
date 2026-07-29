import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
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
import './styles/global.css';

const ProtectedLayout = () => {
  const { user, loading } = useAuth();

  if (loading) return null;
  // If user is not logged in, redirect to /login
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/shipments" element={<Shipment />} />
          <Route path="/predictions" element={<Prediction />} />
          <Route path="/recommendations" element={<Recommendation />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/history" element={<DecisionHistory />} />
          <Route path="/feedback" element={<Feedback />} />
          <Route path="/profile" element={<Profile />} />
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
