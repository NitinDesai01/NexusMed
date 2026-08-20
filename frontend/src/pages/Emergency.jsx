import React, { useState, useEffect } from 'react';

const Emergency = () => {
  const [location, setLocation] = useState(null);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState(null);
  const [countdown, setCountdown] = useState(0);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => setLocation({ lat: position.coords.latitude, lng: position.coords.longitude }),
        () => setError('Unable to get location')
      );
    } else {
      setError('Geolocation not supported');
    }
  }, []);

  const handleEmergency = async () => {
    if (!location) {
      setError('Location not available');
      return;
    }

    setStatus('requesting');
    setCountdown(5);
    setError(null);

    const interval = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) { clearInterval(interval); return 0; }
        return prev - 1;
      });
    }, 1000);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/emergency/request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(location)
      });
      const data = await response.json();
      if (response.ok) {
        setStatus('success');
        setError(null);
      } else {
        setError(data.error || 'Request failed');
        setStatus('error');
      }
    } catch (error) {
      setError('Failed to connect');
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="card-modern border-2 border-green-300">
          <div className="flex items-center gap-4">
            <div className="text-5xl">🚑</div>
            <div>
              <h2 className="text-2xl font-bold text-green-700">Emergency Help Dispatched!</h2>
              <p className="text-gray-600">An ambulance has been dispatched to your location.</p>
            </div>
          </div>
        </div>
        <div className="card-modern">
          <h3 className="text-lg font-bold text-gray-800 mb-4">📍 Emergency Details</h3>
          <div className="space-y-3">
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Status</p>
              <p className="text-green-600 font-semibold animate-pulse">🚨 Active</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Estimated Arrival</p>
              <p className="text-blue-600 font-semibold">5-10 minutes</p>
            </div>
            <button onClick={() => window.location.reload()} className="btn-primary w-full">Check Status</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="card-modern border-2 border-red-200">
        <div className="flex items-center gap-4">
          <div className="text-5xl">🚨</div>
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Emergency Help</h1>
            <p className="text-gray-500">Request immediate emergency assistance</p>
          </div>
        </div>
      </div>

      <div className="card-modern text-center">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">❌ {error}</div>
        )}

        {location && (
          <div className="bg-gray-50 p-4 rounded-xl mb-6 text-left">
            <p className="text-sm text-gray-500">📍 Your Location</p>
            <p className="text-sm text-gray-600">Lat: {location.lat.toFixed(6)}</p>
            <p className="text-sm text-gray-600">Lng: {location.lng.toFixed(6)}</p>
          </div>
        )}

        {status === 'requesting' && countdown > 0 && (
          <div className="mb-6">
            <div className="text-5xl font-bold text-red-600 animate-pulse">{countdown}</div>
            <p className="text-gray-500">Connecting to emergency services...</p>
          </div>
        )}

        <button
          onClick={handleEmergency}
          disabled={status === 'requesting' || !location}
          className={`w-full py-5 text-lg font-bold rounded-xl transition-all ${
            status === 'requesting' || !location
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-red-500 text-white hover:bg-red-600 hover:shadow-lg'
          }`}
        >
          {status === 'requesting' ? '⏳ Requesting...' : '🚑 Request Emergency Help'}
        </button>

        <div className="mt-6 text-sm text-gray-500">
          ⚠️ Only use in genuine emergency. Call <span className="font-bold text-gray-800">112</span> directly.
        </div>
      </div>
    </div>
  );
};

export default Emergency;