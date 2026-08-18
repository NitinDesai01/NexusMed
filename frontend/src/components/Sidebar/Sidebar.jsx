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
    { path: '/emergency', icon: '🚨', label: 'Emergency' },
    { path: '/profile', icon: '👤', label: 'Profile' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <>
      <div className="sidebar">
        <div className="sidebar-user">
          <div className="sidebar-avatar">
            {user?.name?.charAt(0) || 'U'}
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">{user?.name || 'Guest'}</div>
            <div className="sidebar-user-email">{user?.email || 'guest@nexusmed.com'}</div>
          </div>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`sidebar-link ${isActive(item.path) ? 'active' : ''}`}
            >
              <span className="sidebar-link-icon">{item.icon}</span>
              <span className="sidebar-link-label">{item.label}</span>
              {item.path === '/emergency' && (
                <span className="sidebar-badge sidebar-badge-emergency">Emergency</span>
              )}
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-status">
            <span className="sidebar-status-dot"></span>
            <span className="sidebar-status-text">Online</span>
          </div>
          <div className="sidebar-version">v1.0.0</div>
        </div>
      </div>

      <style>{`
        .sidebar {
          width: 256px;
          background: white;
          box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
          display: flex;
          flex-direction: column;
          height: 100%;
          position: fixed;
          left: 0;
          top: 64px;
          bottom: 0;
          z-index: 100;
          transition: transform 0.3s ease;
        }

        .sidebar-user {
          padding: 24px;
          border-bottom: 1px solid #f3f4f6;
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .sidebar-avatar {
          width: 48px;
          height: 48px;
          border-radius: 50%;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 18px;
          flex-shrink: 0;
        }

        .sidebar-user-info {
          flex: 1;
          min-width: 0;
        }

        .sidebar-user-name {
          font-weight: 600;
          color: #1f2937;
          font-size: 14px;
        }

        .sidebar-user-email {
          font-size: 12px;
          color: #6b7280;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .sidebar-nav {
          flex: 1;
          padding: 16px 12px;
          overflow-y: auto;
        }

        .sidebar-link {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 10px 16px;
          border-radius: 10px;
          color: #4b5563;
          text-decoration: none;
          font-weight: 500;
          font-size: 14px;
          transition: all 0.2s ease;
          margin-bottom: 2px;
        }

        .sidebar-link:hover {
          background: #eff6ff;
          color: #2563eb;
        }

        .sidebar-link.active {
          background: #eff6ff;
          color: #2563eb;
          font-weight: 600;
        }

        .sidebar-link-icon {
          font-size: 20px;
          width: 24px;
          text-align: center;
          flex-shrink: 0;
        }

        .sidebar-link-label {
          flex: 1;
        }

        .sidebar-badge {
          padding: 2px 10px;
          border-radius: 9999px;
          font-size: 11px;
          font-weight: 600;
        }

        .sidebar-badge-emergency {
          background: #dc2626;
          color: white;
          animation: pulse 2s infinite;
        }

        .sidebar-footer {
          padding: 16px 24px;
          border-top: 1px solid #f3f4f6;
        }

        .sidebar-status {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .sidebar-status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #22c55e;
          animation: pulse 2s infinite;
        }

        .sidebar-status-text {
          font-size: 13px;
          color: #6b7280;
        }

        .sidebar-version {
          font-size: 11px;
          color: #9ca3af;
          margin-top: 4px;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }

        @media (max-width: 768px) {
          .sidebar {
            transform: translateX(-100%);
            width: 280px;
          }
          .sidebar.open {
            transform: translateX(0);
          }
        }
      `}</style>
    </>
  );
};

export default Sidebar;
