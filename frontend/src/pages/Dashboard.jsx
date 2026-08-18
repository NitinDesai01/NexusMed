import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import ChatBot from '../components/ChatBot/ChatBot';

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Welcome back, {user?.name || 'User'}!</h1>
        <span className="text-sm text-gray-500">{new Date().toLocaleDateString()}</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-sm font-medium text-gray-500">Health Score</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">85%</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-sm font-medium text-gray-500">Reports</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">12</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-sm font-medium text-gray-500">Appointments</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">3</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-sm font-medium text-gray-500">Emergency Status</p>
          <p className="text-2xl font-bold text-green-600 mt-1">Safe</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Recent Reports</h2>
            <p className="text-gray-500">No reports uploaded yet</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Upcoming Appointments</h2>
            <p className="text-gray-500">No upcoming appointments</p>
          </div>
        </div>
        <div className="lg:col-span-1">
          <ChatBot />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
