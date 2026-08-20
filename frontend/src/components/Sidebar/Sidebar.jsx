import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const { user } = useAuth();

  const menuItems = [
    { path: '/dashboard', icon: '📊', label: 'Dashboard' },
    { path: '/symptoms', icon: '🩺', label: 'Symptoms' },
    { path: '/appointment', icon: '📅', label: 'Book Appointment' },
    { path: '/reports', icon: '📄', label: 'Reports' },
    { path: '/medicines', icon: '💊', label: 'Medicines' },
    { path: '/hospitals', icon: '🏥', label: 'Hospitals' },
    { path: '/community', icon: '🧠', label: 'Health Awareness' },
    { path: '/emergency', icon: '🚨', label: 'Emergency' },
    { path: '/profile', icon: '👤', label: 'Profile' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className="sidebar">
      {/* User Profile */}
      <div className="sidebar-user">
        <div className="sidebar-user-avatar">
          {user?.name?.charAt(0) || 'U'}
        </div>
        <div className="sidebar-user-info">
          <div className="sidebar-user-name">{user?.name || 'Guest'}</div>
          <div className="sidebar-user-email">{user?.email || 'guest@nexusmed.com'}</div>
          <div className="sidebar-user-status">
            <span className="dot"></span>
            <span className="text">Online</span>
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${isActive(item.path) ? 'active' : ''}`}
          >
            <span className="icon">{item.icon}</span>
            <span className="label">{item.label}</span>
            {item.path === '/emergency' && (
              <span className="badge">URGENT</span>
            )}
          </Link>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="version">NexusMed v1.0.0</div>
      </div>
    </div>
  );
};

export default Sidebar;