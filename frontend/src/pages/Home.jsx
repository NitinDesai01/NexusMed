import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const { isAuthenticated } = useAuth();

  const features = [
    { icon: '🩺', title: 'Symptom Analysis', description: 'AI-powered symptom analysis and disease prediction' },
    { icon: '💊', title: 'Medicine Information', description: 'Search medicines, check interactions and get recommendations' },
    { icon: '🏥', title: 'Hospital Locator', description: 'Find nearby hospitals with available beds and emergency services' },
    { icon: '🚨', title: 'Emergency Services', description: 'Real-time ambulance tracking and emergency response' },
    { icon: '📄', title: 'Report Analysis', description: 'Upload and analyze medical reports using AI' },
    { icon: '🧠', title: 'Health Assistant', description: '24/7 AI health assistant for your queries' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center max-w-4xl mx-auto">
          <div className="text-6xl mb-6">🏥</div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">Welcome to NexusMed</h1>
          <p className="text-xl text-gray-600 mb-8">
            Your AI-powered healthcare assistant for symptom analysis, disease prediction, 
            medicine recommendations, and emergency services.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            {isAuthenticated ? (
              <Link to="/dashboard" className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-lg">
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link to="/register" className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-lg">
                  Get Started
                </Link>
                <Link to="/login" className="px-8 py-3 bg-white text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-lg">
                  Login
                </Link>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-lg font-semibold">NexusMed</p>
          <p className="text-gray-400 text-sm mt-2">AI-Powered Healthcare Assistant</p>
          <p className="text-gray-500 text-xs mt-4">© 2024 NexusMed. All rights reserved.</p>
          <p className="text-gray-500 text-xs mt-2">Disclaimer: This is an AI-powered tool. Always consult a healthcare professional.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
