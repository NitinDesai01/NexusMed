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
    if (!token) {
      setError('Please login first');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/symptoms/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ symptoms: symptoms })
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || data.message || 'Analysis failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="text-6xl mb-4">🔒</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Please Login</h2>
          <p className="text-gray-500 mb-6">You need to be logged in to use symptom analysis</p>
          <button onClick={() => window.location.href = '/login'} className="btn-primary">
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="card-modern">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">🩺 Symptom Analysis</h1>
            <p className="text-gray-500 mt-1">Describe your symptoms and get AI-powered analysis</p>
          </div>
          <div className="bg-yellow-50 px-4 py-2 rounded-xl text-yellow-700 text-sm flex items-center gap-2 border border-yellow-200">
            ⚠️ Always consult a healthcare professional
          </div>
        </div>
      </div>

      {/* Main Form */}
      <div className="card-modern">
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe your symptoms:
            </label>
            <textarea
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="e.g., I have a headache, fever, and sore throat..."
              className="textarea-field"
              rows="4"
            />
          </div>

          {/* Quick Tags */}
          <div className="flex flex-wrap gap-2 mb-4">
            {['Fever', 'Headache', 'Cough', 'Fatigue', 'Nausea', 'Fever + Cough'].map((tag) => (
              <button
                key={tag}
                type="button"
                onClick={() => setSymptoms(tag)}
                className="tag tag-blue"
              >
                {tag}
              </button>
            ))}
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">
              ❌ {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !symptoms.trim()}
            className="btn-primary w-full"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="spinner w-5 h-5 border-2"></div>
                Analyzing...
              </span>
            ) : (
              '🔍 Analyze Symptoms'
            )}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && result.analysis && (
        <div className="card-modern fade-in-up">
          <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Analysis Results</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Left Column */}
            <div className="space-y-3">
              <div className="bg-gray-50 p-4 rounded-xl">
                <p className="text-sm text-gray-500">Symptoms Analyzed</p>
                <p className="text-gray-800 font-medium">{result.analysis.symptoms_analyzed}</p>
              </div>

              <div className="bg-gray-50 p-4 rounded-xl">
                <p className="text-sm text-gray-500">Severity</p>
                <span className={`badge ${getSeverityColor(result.analysis.severity)}`}>
                  {result.analysis.severity?.toUpperCase()}
                </span>
              </div>

              {result.analysis.emergency_signs && (
                <div className="p-4 bg-red-50 border-2 border-red-200 rounded-xl">
                  <p className="text-red-700 font-bold">🚨 EMERGENCY SIGNS DETECTED</p>
                  <p className="text-red-600">Please seek immediate medical attention!</p>
                </div>
              )}
            </div>

            {/* Right Column */}
            <div className="space-y-3">
              <div className="bg-gray-50 p-4 rounded-xl">
                <p className="text-sm text-gray-500 mb-2">Possible Conditions</p>
                <div className="flex flex-wrap gap-2">
                  {result.analysis.possible_conditions?.map((condition, i) => (
                    <span key={i} className="tag tag-purple">
                      {condition}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded-xl">
                <p className="text-sm text-gray-500 mb-2">Recommendations</p>
                <ul className="space-y-1">
                  {result.analysis.recommendations?.map((rec, i) => (
                    <li key={i} className="text-gray-700 text-sm flex items-start gap-2">
                      <span className="text-blue-500">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Disease Predictions */}
          {result.predictions?.predictions?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm font-medium text-gray-700 mb-3">Disease Predictions</p>
              <div className="space-y-2">
                {result.predictions.predictions.map((pred, i) => (
                  <div key={i} className="bg-gray-50 p-3 rounded-xl flex items-center justify-between">
                    <span className="text-gray-800 font-medium">{pred.disease}</span>
                    <div className="flex items-center gap-3">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-1000"
                          style={{ width: `${pred.confidence}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold text-blue-600 min-w-[40px]">{pred.confidence}%</span>
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-xs text-gray-400 mt-2">Model: {result.predictions.model_used}</p>
            </div>
          )}

          {/* Disclaimer */}
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-xl">
            <p className="text-sm text-yellow-700">⚠️ {result.disclaimer || "This is an AI-based analysis. Always consult a healthcare professional."}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Symptoms;