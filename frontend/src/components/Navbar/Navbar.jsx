import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      {/* Brand / Logo */}
      <Link to="/" className="navbar-brand">
        <span className="logo-icon">🏥</span>
        <div>
          <span className="logo-text">NexusMed</span>
          <span className="logo-sub">AI Healthcare</span>
        </div>
      </Link>

      {/* Navigation Links - Center */}
      <div className="navbar-links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/symptoms">Symptoms</Link>
        <Link to="/appointment">Book Appointment</Link>
        <Link to="/medicines">Medicines</Link>
        <Link to="/community">Health Awareness</Link>
        <Link to="/emergency" className="emergency-link">🚨 Emergency</Link>
      </div>

      {/* Right Side - User/Auth */}
      <div className="navbar-right">
        {isAuthenticated ? (
          <>
            <Link to="/profile" className="flex items-center gap-2">
              <div className="user-avatar">{user?.name?.charAt(0) || 'U'}</div>
              <span className="user-name hidden sm:block">{user?.name || 'User'}</span>
            </Link>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn-login">Login</Link>
            <Link to="/register" className="btn-register">Register</Link>
          </>
        )}

        {/* Mobile Menu Toggle */}
        <button className="navbar-mobile-btn" onClick={() => setIsMobileOpen(!isMobileOpen)}>
          {isMobileOpen ? '✕' : '☰'}
        </button>
      </div>

      {/* Mobile Menu */}
      <div className={`navbar-mobile-menu ${isMobileOpen ? 'open' : ''}`}>
        <Link to="/dashboard" onClick={() => setIsMobileOpen(false)}>Dashboard</Link>
        <Link to="/symptoms" onClick={() => setIsMobileOpen(false)}>Symptoms</Link>
        <Link to="/appointment" onClick={() => setIsMobileOpen(false)}>Book Appointment</Link>
        <Link to="/medicines" onClick={() => setIsMobileOpen(false)}>Medicines</Link>
        <Link to="/community" onClick={() => setIsMobileOpen(false)}>Health Awareness</Link>
        <Link to="/emergency" className="emergency-link" onClick={() => setIsMobileOpen(false)}>🚨 Emergency</Link>
        {isAuthenticated ? (
          <>
            <Link to="/profile" onClick={() => setIsMobileOpen(false)}>Profile</Link>
            <button onClick={handleLogout} style={{ width: '100%', textAlign: 'left', padding: '12px 16px', color: '#dc2626', background: 'none', border: 'none', fontSize: '14px', cursor: 'pointer' }}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" onClick={() => setIsMobileOpen(false)}>Login</Link>
            <Link to="/register" onClick={() => setIsMobileOpen(false)}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;