import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [healthTip, setHealthTip] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const statsResponse = await fetch('http://localhost:5000/api/dashboard/stats', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const statsData = await statsResponse.json();
      if (statsResponse.ok) setStats(statsData);

      const recResponse = await fetch('http://localhost:5000/api/dashboard/recommendations', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const recData = await recResponse.json();
      if (recResponse.ok) setRecommendations(recData.recommendations || []);

      const tipResponse = await fetch('http://localhost:5000/api/dashboard/health-tips', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const tipData = await tipResponse.json();
      if (tipResponse.ok) setHealthTip(tipData.tip);

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="spinner mx-auto"></div>
          <p className="text-gray-500 mt-4">Loading your health dashboard...</p>
        </div>
      </div>
    );
  }

  const quickActions = [
    { icon: '🩺', label: 'Symptom Check', path: '/symptoms' },
    { icon: '📅', label: 'Book Appointment', path: '/appointment' },
    { icon: '💊', label: 'Medicine Search', path: '/medicines' },
    { icon: '🚨', label: 'Emergency', path: '/emergency' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Welcome Header */}
      <div className="card-modern">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
              Welcome back, {user?.name || 'User'}! 👋
            </h1>
            <p className="text-gray-500 mt-1">Here's your health overview</p>
          </div>
          <div className="bg-gray-50 px-4 py-2 rounded-xl text-gray-600 text-sm flex items-center gap-2">
            📅 {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card-gradient-blue p-6 rounded-xl">
          <p className="text-white/80 text-sm">Total Appointments</p>
          <p className="text-3xl font-bold text-white mt-1">{stats?.total_appointments || 0}</p>
        </div>
        <div className="card-gradient-green p-6 rounded-xl">
          <p className="text-gray-700/70 text-sm">Upcoming</p>
          <p className="text-3xl font-bold text-gray-800 mt-1">{stats?.upcoming_appointments || 0}</p>
        </div>
        <div className="card-gradient-purple p-6 rounded-xl">
          <p className="text-gray-700/70 text-sm">Completed</p>
          <p className="text-3xl font-bold text-gray-800 mt-1">{stats?.completed_appointments || 0}</p>
        </div>
        <div className="card-gradient-orange p-6 rounded-xl">
          <p className="text-gray-700/70 text-sm">Health Score</p>
          <p className="text-3xl font-bold text-gray-800 mt-1">{stats?.health_score || 70}%</p>
        </div>
      </div>

      {/* Next Appointment */}
      {stats?.next_appointment && (
        <div className="card-modern border-l-4 border-blue-500">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <p className="text-sm text-gray-500">📋 Next Appointment</p>
              <p className="text-lg font-semibold text-gray-800">{stats.next_appointment.doctor_name}</p>
              <p className="text-gray-600 text-sm">{stats.next_appointment.specialization} • {stats.next_appointment.hospital}</p>
              <p className="text-blue-600 text-sm mt-1">📅 {stats.next_appointment.date} at {stats.next_appointment.time}</p>
            </div>
            <button className="btn-primary text-sm py-2 px-6">View Details</button>
          </div>
        </div>
      )}

      {/* Health Tip */}
      {healthTip && (
        <div className="card-modern border-l-4 border-yellow-400 bg-gradient-to-r from-yellow-50 to-orange-50">
          <div className="flex items-center gap-4">
            <span className="text-3xl">{healthTip.icon}</span>
            <div>
              <p className="text-xs text-gray-500">💡 Health Tip of the Day</p>
              <p className="font-semibold text-gray-800">{healthTip.title}</p>
              <p className="text-sm text-gray-600">{healthTip.description}</p>
            </div>
          </div>
        </div>
      )}

      {/* AI Recommendations */}
      {recommendations.length > 0 && (
        <div>
          <h2 className="text-lg font-bold text-gray-800 mb-3">🤖 AI Health Recommendations</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.slice(0, 4).map((rec) => (
              <div key={rec.id} className="card-modern border-l-4 border-blue-400">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">{rec.icon}</span>
                  <div>
                    <h3 className="font-semibold text-gray-800">{rec.title}</h3>
                    <p className="text-sm text-gray-600">{rec.description}</p>
                    {rec.action && (
                      <button className="mt-2 text-sm text-blue-600 hover:text-blue-800 font-medium">
                        {rec.action} →
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="card-modern">
        <h2 className="text-lg font-bold text-gray-800 mb-4">⚡ Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {quickActions.map((action) => (
            <button 
              key={action.path}
              onClick={() => navigate(action.path)}
              className="p-4 bg-gray-50 hover:bg-gray-100 rounded-xl transition-all text-center hover:shadow-md"
            >
              <span className="text-3xl block">{action.icon}</span>
              <span className="text-sm font-medium text-gray-700 mt-1 block">{action.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;