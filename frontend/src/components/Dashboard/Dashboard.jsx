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
          <div className="spinner-3d mx-auto"></div>
          <p className="text-white/40 mt-4">Loading your health dashboard...</p>
        </div>
      </div>
    );
  }

  const quickActions = [
    { icon: '🩺', label: 'Symptom Check', path: '/symptoms', color: 'from-blue-500/20 to-blue-600/20' },
    { icon: '📅', label: 'Book Appointment', path: '/appointment', color: 'from-green-500/20 to-green-600/20' },
    { icon: '💊', label: 'Medicine Search', path: '/medicines', color: 'from-purple-500/20 to-purple-600/20' },
    { icon: '🚨', label: 'Emergency', path: '/emergency', color: 'from-red-500/20 to-red-600/20' },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="glass-3d p-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-white">
              Welcome back, <span className="text-gradient-3d">{user?.name || 'User'}</span>! 👋
            </h1>
            <p className="text-white/40 mt-1">Here's your health overview and personalized recommendations</p>
          </div>
          <div className="glass-light px-6 py-3 rounded-2xl text-white/60 text-sm flex items-center gap-2">
            <span>📅</span>
            {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total Appointments', value: stats?.total_appointments || 0, icon: '📅', color: 'from-blue-500 to-blue-600' },
          { label: 'Upcoming', value: stats?.upcoming_appointments || 0, icon: '⏰', color: 'from-green-500 to-green-600' },
          { label: 'Completed', value: stats?.completed_appointments || 0, icon: '✅', color: 'from-purple-500 to-purple-600' },
          { label: 'Health Score', value: `${stats?.health_score || 70}%`, icon: '❤️', color: 'from-orange-500 to-orange-600' },
        ].map((stat, index) => (
          <div key={index} className="card-3d p-6 group perspective">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/40 text-sm">{stat.label}</p>
                <p className="text-3xl font-bold text-white mt-1">{stat.value}</p>
              </div>
              <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${stat.color} flex items-center justify-center text-2xl shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform`}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Next Appointment */}
      {stats?.next_appointment && (
        <div className="glass-3d p-6 border border-blue-500/20">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <p className="text-white/40 text-sm">📋 Next Appointment</p>
              <p className="text-xl font-semibold text-white">{stats.next_appointment.doctor_name}</p>
              <p className="text-white/60 text-sm">{stats.next_appointment.specialization} • {stats.next_appointment.hospital}</p>
              <p className="text-blue-400 text-sm mt-1">📅 {stats.next_appointment.date} at {stats.next_appointment.time}</p>
            </div>
            <button className="btn-3d text-sm py-2 px-6">
              View Details
            </button>
          </div>
        </div>
      )}

      {/* Health Tip */}
      {healthTip && (
        <div className="glass-3d p-6 border border-yellow-500/20 bg-gradient-to-r from-yellow-500/5 to-orange-500/5">
          <div className="flex items-center gap-4">
            <span className="text-4xl float">{healthTip.icon}</span>
            <div>
              <p className="text-white/40 text-sm">💡 Health Tip of the Day</p>
              <p className="text-white font-semibold">{healthTip.title}</p>
              <p className="text-white/60 text-sm">{healthTip.description}</p>
            </div>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-white mb-4">🤖 AI Health Recommendations</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec) => (
              <div key={rec.id} className={`glass-3d p-6 border-l-4 ${
                rec.priority === 'high' ? 'border-l-red-500' :
                rec.priority === 'medium' ? 'border-l-yellow-500' :
                'border-l-blue-500'
              }`}>
                <div className="flex items-start gap-3">
                  <span className="text-2xl">{rec.icon}</span>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-white">{rec.title}</h3>
                      {rec.priority === 'high' && (
                        <span className="badge-3d badge-3d-danger text-[10px]">Urgent</span>
                      )}
                    </div>
                    <p className="text-white/60 text-sm">{rec.description}</p>
                    {rec.action && (
                      <button className="mt-2 text-sm text-blue-400 hover:text-blue-300 font-medium transition">
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
      <div className="glass-3d p-6">
        <h2 className="text-xl font-bold text-white mb-4">⚡ Quick Actions</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {quickActions.map((action) => (
            <button 
              key={action.path}
              onClick={() => navigate(action.path)}
              className={`p-4 rounded-2xl bg-gradient-to-br ${action.color} border border-white/5 hover:border-white/20 transition-all duration-300 hover:scale-105 hover:-translate-y-1 group perspective`}
            >
              <span className="text-3xl block group-hover:scale-110 transition-transform">{action.icon}</span>
              <span className="text-white/80 text-sm font-medium mt-1 block">{action.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;