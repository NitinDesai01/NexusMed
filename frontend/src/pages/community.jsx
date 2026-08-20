import React, { useState } from 'react';

const Community = () => {
  const [topic, setTopic] = useState('');
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGetAwareness = async () => {
    if (!topic.trim()) {
      setError('Please enter a health topic');
      return;
    }

    setLoading(true);
    setError('');
    setContent(null);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/community/awareness?topic=${encodeURIComponent(topic)}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const data = await response.json();
      if (response.ok) {
        setContent(data.content);
      } else {
        setError(data.error || 'Failed to fetch health awareness');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const healthTopics = [
    'Heart Health', 'Diabetes Prevention', 'Mental Health',
    'Nutrition', 'Exercise', 'Stress Management',
    'Vaccination', 'Cancer Screening', 'Asthma',
    'Allergies', 'Sleep Hygiene', 'First Aid'
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="card-modern">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-800">🧠 Health Awareness</h1>
          <p className="text-gray-500 mt-1">Get AI-powered health information and awareness content</p>
        </div>
      </div>

      {/* Search/Topic Input */}
      <div className="card-modern">
        <div className="flex gap-4">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter a health topic (e.g., Diabetes, Heart Health)..."
            className="input-field flex-1"
          />
          <button
            onClick={handleGetAwareness}
            disabled={loading}
            className="btn-3d px-8"
          >
            {loading ? '⏳' : '🔍 Get Info'}
          </button>
        </div>

        {/* Quick Topics */}
        <div className="flex flex-wrap gap-2 mt-4">
          {healthTopics.map((t) => (
            <button
              key={t}
              onClick={() => setTopic(t)}
              className="tag tag-blue"
            >
              {t}
            </button>
          ))}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">
            ❌ {error}
          </div>
        )}
      </div>

      {/* Content Display */}
      {content && (
        <div className="card-modern fade-in-up">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-3xl">{content.icon || '📚'}</span>
            <h2 className="text-xl font-bold text-gray-800">{content.title || topic}</h2>
          </div>

          <div className="bg-gray-50 p-4 rounded-xl mb-4">
            <p className="text-gray-700 leading-relaxed">{content.content}</p>
          </div>

          {content.symptoms && content.symptoms !== "No specific symptoms listed" && (
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Symptoms:</p>
              <div className="bg-gray-50 p-3 rounded-xl">
                <p className="text-gray-600">{content.symptoms}</p>
              </div>
            </div>
          )}

          {content.prevention && (
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Prevention:</p>
              <div className="bg-gray-50 p-3 rounded-xl">
                <p className="text-gray-600">{content.prevention}</p>
              </div>
            </div>
          )}

          {content.risk_factors && content.risk_factors !== "Consult your doctor for personalized advice" && (
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Risk Factors:</p>
              <div className="bg-gray-50 p-3 rounded-xl">
                <p className="text-gray-600">{content.risk_factors}</p>
              </div>
            </div>
          )}

          {content.tips && content.tips.length > 0 && (
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">💡 Tips:</p>
              <ul className="space-y-1">
                {content.tips.map((tip, i) => (
                  <li key={i} className="text-gray-600 text-sm flex items-start gap-2">
                    <span className="text-blue-500">•</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Community;