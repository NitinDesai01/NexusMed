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
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-3d p-8">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold text-white">🧠 Health Awareness</h1>
          <p className="text-white/40 mt-1">Get AI-powered health information and awareness content</p>
        </div>
      </div>

      {/* Search/Topic Input */}
      <div className="glass-3d p-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter a health topic (e.g., Diabetes, Heart Health)..."
            className="input-3d flex-1"
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
              className="tag-3d tag-3d-blue text-sm"
            >
              {t}
            </button>
          ))}
        </div>

        {error && (
          <div className="mt-4 p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400">
            ❌ {error}
          </div>
        )}
      </div>

      {/* Content Display */}
      {content && (
        <div className="glass-3d p-8 animate-fade-in">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">📚</span>
            <h2 className="text-xl font-bold text-white">{content.title || topic}</h2>
          </div>
          <div className="glass-light p-6 rounded-2xl">
            <p className="text-white/80 leading-relaxed">{content.content}</p>
          </div>
          {content.tips && (
            <div className="mt-4">
              <p className="text-white/60 text-sm font-medium mb-2">💡 Tips:</p>
              <ul className="space-y-1">
                {content.tips.map((tip, i) => (
                  <li key={i} className="text-white/60 text-sm flex items-start gap-2">
                    <span className="text-blue-400">•</span>
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