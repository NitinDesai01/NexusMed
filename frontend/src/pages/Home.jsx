import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: '🩺',
      title: 'Symptom Analysis',
      description: 'AI-powered symptom analysis and disease prediction',
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200'
    },
    {
      icon: '💊',
      title: 'Medicine Information',
      description: 'Search medicines, check interactions and get recommendations',
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200'
    },
    {
      icon: '🏥',
      title: 'Hospital Locator',
      description: 'Find nearby hospitals with available beds and emergency services',
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200'
    },
    {
      icon: '🚨',
      title: 'Emergency Services',
      description: 'Real-time ambulance tracking and emergency response',
      color: 'from-red-500 to-red-600',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200'
    },
    {
      icon: '📄',
      title: 'Report Analysis',
      description: 'Upload and analyze medical reports using AI',
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200'
    },
    {
      icon: '🧠',
      title: 'Health Assistant',
      description: '24/7 AI health assistant for your queries',
      color: 'from-pink-500 to-pink-600',
      bgColor: 'bg-pink-50',
      borderColor: 'border-pink-200'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="card-modern text-center py-12 perspective">
        <div className="max-w-3xl mx-auto">
          <div className="text-6xl mb-4 transform hover:scale-110 transition-transform duration-500 float">🏥</div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
            Welcome to <span className="text-gradient">NexusMed</span>
          </h1>
          <p className="text-lg text-gray-600 mb-6">
            Your AI-powered healthcare assistant for symptom analysis, disease prediction, 
            medicine recommendations, and emergency services.
          </p>
          <Link 
            to={isAuthenticated ? '/dashboard' : '/login'} 
            className="btn-3d inline-block"
          >
            {isAuthenticated ? 'Go to Dashboard' : 'Get Started'}
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">🌟 Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div 
              key={index}
              className={`card-modern transform transition-all duration-500 hover:-translate-y-2 hover:shadow-xl perspective group`}
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} flex items-center justify-center text-3xl mb-4 shadow-lg transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">{feature.title}</h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card-gradient-blue text-center py-6 transform hover:scale-105 transition-all duration-300">
          <div className="text-3xl font-bold">24/7</div>
          <div className="text-sm opacity-80">AI Assistant</div>
        </div>
        <div className="card-gradient-green text-center py-6 transform hover:scale-105 transition-all duration-300">
          <div className="text-3xl font-bold text-gray-800">1000+</div>
          <div className="text-sm text-gray-700/80">Diseases Covered</div>
        </div>
        <div className="card-gradient-purple text-center py-6 transform hover:scale-105 transition-all duration-300">
          <div className="text-3xl font-bold text-gray-800">500+</div>
          <div className="text-sm text-gray-700/80">Medicines</div>
        </div>
        <div className="card-gradient-orange text-center py-6 transform hover:scale-105 transition-all duration-300">
          <div className="text-3xl font-bold text-gray-800">100+</div>
          <div className="text-sm text-gray-700/80">Hospitals</div>
        </div>
      </div>

      {/* Footer */}
      <footer className="card-modern text-center py-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-center gap-2 mb-2">
            <span className="text-2xl">🏥</span>
            <span className="text-xl font-bold text-gray-800">NexusMed</span>
          </div>
          <p className="text-gray-500 text-sm">AI-Powered Healthcare Assistant</p>
          <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-gray-400 text-sm">
              © 2026 <span className="text-gray-600 font-medium">Nitin Desai</span>. All rights reserved.
            </p>
            <p className="text-gray-400 text-xs mt-2">
              ⚠️ Disclaimer: This is an AI-powered tool. Always consult a healthcare professional.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;