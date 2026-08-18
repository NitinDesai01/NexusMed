import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center">
          <Link to="/" className="flex items-center space-x-2 text-2xl font-bold text-blue-600">
            <span>🏥</span>
            <span className="hidden sm:inline">NexusMed</span>
          </Link>
        </div>

        <div className="flex items-center space-x-4">
          <Link to="/dashboard" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg hover:bg-blue-50">Dashboard</Link>
          <Link to="/symptoms" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg hover:bg-blue-50">Symptoms</Link>
          <Link to="/medicines" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg hover:bg-blue-50">Medicines</Link>
          <Link to="/hospitals" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg hover:bg-blue-50">Hospitals</Link>
          <Link to="/emergency" className="text-red-600 hover:text-red-700 px-3 py-2 rounded-lg hover:bg-red-50 font-semibold">🚑 Emergency</Link>
          
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <Link to="/profile" className="flex items-center space-x-2">
                <span className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-semibold">
                  {user?.name?.charAt(0) || 'U'}
                </span>
                <span className="hidden md:inline">{user?.name || 'User'}</span>
              </Link>
              <button onClick={handleLogout} className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">Logout</button>
            </div>
          ) : (
            <div className="flex items-center space-x-4">
              <Link to="/login" className="text-blue-600 hover:text-blue-700">Login</Link>
              <Link to="/register" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Register</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
