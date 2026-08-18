import React, { useState, useEffect } from 'react';

const Symptoms = () => {
  const [symptoms, setSymptoms] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symptoms.trim()) {
      setError('Please describe your symptoms');
      return;
    }

    const token = localStorage.getItem('token');
    console.log('Token:', token ? 'Found' : 'Not found');

    if (!token) {
      setError('Please login first. Redirecting...');
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      console.log('Sending symptoms:', symptoms);
      
      const response = await fetch('http://localhost:5000/api/symptoms/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ symptoms: symptoms })
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);

      if (response.ok) {
        setResult(data);
        setError('');
      } else if (response.status === 401) {
        setError('Session expired. Please login again.');
        localStorage.removeItem('token');
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
      } else {
        setError(data.error || data.message || `Error ${response.status}: Analysis failed`);
      }
    } catch (error) {
      console.error('Fetch error:', error);
      setError('Cannot connect to backend. Make sure it\'s running on http://localhost:5000');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">🩺 Symptom Analysis</h1>
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-8">
            <p className="text-yellow-800 text-lg">⚠️ Please login to use symptom analysis</p>
            <button 
              onClick={() => window.location.href = '/login'}
              className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Go to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🩺 Symptom Analysis</h1>
        <p className="text-gray-600 mb-6">
          Describe your symptoms and get AI-powered analysis
          <span className="block text-sm text-yellow-600 mt-1">⚠️ Always consult a healthcare professional</span>
        </p>

        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe your symptoms:
            </label>
            <textarea
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="e.g., I have a headache, fever, and sore throat..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows="4"
            />
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !symptoms.trim()}
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {loading ? '⏳ Analyzing...' : '🔍 Analyze Symptoms'}
          </button>
        </form>

        {result && result.analysis && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Analysis Results</h2>

            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Symptoms Analyzed:</p>
              <p className="text-lg font-medium text-gray-800">{result.analysis.symptoms_analyzed}</p>
            </div>

            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Possible Conditions:</p>
              <div className="flex flex-wrap gap-2">
                {result.analysis.possible_conditions?.map((condition, i) => (
                  <span key={i} className="px-3 py-1.5 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                    {condition}
                  </span>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Severity:</p>
              <span className={`inline-block px-4 py-2 rounded-lg text-sm font-bold border ${getSeverityColor(result.analysis.severity)}`}>
                {result.analysis.severity?.toUpperCase()}
              </span>
            </div>

            {result.analysis.emergency_signs && (
              <div className="mb-4 p-4 bg-red-50 border-2 border-red-300 rounded-lg">
                <p className="text-red-700 font-bold text-lg">🚨 EMERGENCY SIGNS DETECTED</p>
                <p className="text-red-600">Please seek immediate medical attention!</p>
              </div>
            )}

            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Recommendations:</p>
              <ul className="list-disc pl-5 space-y-1">
                {result.analysis.recommendations?.map((rec, i) => (
                  <li key={i} className="text-gray-600">{rec}</li>
                ))}
              </ul>
            </div>

            {result.predictions?.predictions?.length > 0 && (
              <div className="mt-4 pt-4 border-t">
                <p className="text-sm font-medium text-gray-700 mb-3">Disease Predictions:</p>
                <div className="space-y-2">
                  {result.predictions.predictions.map((pred, i) => (
                    <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-gray-800">{pred.disease}</span>
                      <div className="flex items-center gap-3">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full transition-all"
                            style={{ width: `${pred.confidence}%` }}
                          />
                        </div>
                        <span className="text-sm font-semibold text-blue-600">{pred.confidence}%</span>
                      </div>
                    </div>
                  ))}
                </div>
                <p className="text-xs text-gray-400 mt-2">Model: {result.predictions.model_used}</p>
              </div>
            )}

            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">⚠️ {result.disclaimer || "This is an AI-based analysis. Always consult a healthcare professional."}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Symptoms;
