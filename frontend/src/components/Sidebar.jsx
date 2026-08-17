import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { canAccessPath, normalizeRole } from '../utils/rbac';
import {
  LayoutDashboard,
  Truck,
  TrendingUp,
  Sliders,
  BarChart3,
  History,
  MessageSquare,
  User,
  LogOut,
  Layers
} from 'lucide-react';
import '../styles/sidebar.css';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Shipments', path: '/shipments', icon: Truck },
    { label: 'Predictions', path: '/predictions', icon: TrendingUp },
    { label: 'Optimization', path: '/recommendations', icon: Sliders },
    { label: 'Analytics', path: '/analytics', icon: BarChart3 },
    { label: 'Decision History', path: '/history', icon: History },
    { label: 'Feedback Loop', path: '/feedback', icon: MessageSquare },
    { label: 'Profile', path: '/profile', icon: User },
  ];

  // Filter navigation items based on user's authorized role
  const userRole = normalizeRole(user?.role);
  const authorizedNavItems = navItems.filter((item) => canAccessPath(userRole, item.path));

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo-icon">
          <Layers size={22} />
        </div>
        <div className="sidebar-brand-text">SupplyPrescript</div>
      </div>

      <nav className="sidebar-nav">
        {authorizedNavItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-user">
        <div className="user-info">
          <div className="avatar">
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div className="user-details">
            <span className="user-name">{user?.full_name || 'User'}</span>
            <span className="user-role" title={userRole}>{userRole}</span>
          </div>
        </div>
        <button onClick={handleLogout} title="Logout" style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}>
          <LogOut size={18} />
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
