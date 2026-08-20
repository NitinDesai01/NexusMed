import React, { useState, useEffect } from 'react';

const Emergency = () => {
  const [location, setLocation] = useState(null);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState(null);
  const [emergencyData, setEmergencyData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);

  useEffect(() => {
    // Get user location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        () => {
          // Use default location (Bangalore)
          setLocation({ lat: 12.9716, lng: 77.5946 });
        }
      );
    } else {
      setLocation({ lat: 12.9716, lng: 77.5946 });
    }
  }, []);

  const handleEmergency = async () => {
    if (!location) {
      setError('Location not available. Please enable location services.');
      return;
    }

    setLoading(true);
    setError(null);
    setStatus('requesting');
    setCountdown(5);

    // Countdown animation
    const interval = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Please login first');
        setStatus('error');
        setLoading(false);
        return;
      }

      const response = await fetch('http://localhost:5000/api/emergency/request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          lat: location.lat,
          lng: location.lng
        })
      });

      const data = await response.json();

      if (response.ok) {
        setEmergencyData(data);
        setStatus('success');
        setError(null);
      } else {
        setError(data.error || 'Failed to request emergency help');
        setStatus('error');
      }
    } catch (error) {
      console.error('Emergency request error:', error);
      setError('Failed to connect to emergency services. Please call 112 directly.');
      setStatus('error');
    } finally {
      setLoading(false);
    }
  };

  if (status === 'success' && emergencyData) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="card-modern border-2 border-green-300">
          <div className="flex items-center gap-4">
            <div className="text-5xl animate-pulse">🚑</div>
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
              <p className="text-sm text-gray-500">Request ID</p>
              <p className="font-semibold text-gray-800">{emergencyData.request_id}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Status</p>
              <p className="text-green-600 font-semibold animate-pulse">🚨 Dispatched</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Ambulance</p>
              <p className="font-semibold text-gray-800">{emergencyData.ambulance?.vehicle_number || 'En route'}</p>
              <p className="text-sm text-gray-500">Driver: {emergencyData.ambulance?.driver_name || 'Rajesh Kumar'}</p>
              <p className="text-sm text-gray-500">Phone: {emergencyData.ambulance?.driver_phone || '+91-9876543210'}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Estimated Arrival</p>
              <p className="text-blue-600 font-semibold">{emergencyData.ambulance?.estimated_arrival || '5-10 minutes'}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Equipment Level</p>
              <p className="text-gray-700">{emergencyData.ambulance?.equipment_level || 'Advanced'}</p>
            </div>
            <button
              onClick={() => window.location.reload()}
              className="btn-3d w-full"
            >
              Check Status
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="card-modern border-2 border-red-200">
        <div className="flex items-center gap-4">
          <div className="text-5xl animate-pulse">🚨</div>
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Emergency Help</h1>
            <p className="text-gray-500">Request immediate emergency assistance</p>
          </div>
        </div>
      </div>

      {/* Main Emergency Card */}
      <div className="card-modern text-center">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 text-left">
            ❌ {error}
          </div>
        )}

        {location && (
          <div className="bg-gray-50 p-4 rounded-xl mb-6 text-left">
            <p className="text-sm text-gray-500 mb-1">📍 Your Location</p>
            <p className="text-sm text-gray-600">Lat: {location.lat.toFixed(6)}</p>
            <p className="text-sm text-gray-600">Lng: {location.lng.toFixed(6)}</p>
          </div>
        )}

        {status === 'requesting' && countdown > 0 && (
          <div className="mb-6">
            <div className="text-6xl font-bold text-red-600 animate-pulse">{countdown}</div>
            <p className="text-gray-500 mt-2">Connecting to emergency services...</p>
          </div>
        )}

        <button
          onClick={handleEmergency}
          disabled={loading || status === 'requesting' || !location}
          className={`w-full py-5 text-lg font-bold rounded-2xl transition-all duration-300 ${
            loading || status === 'requesting' || !location
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-red-500 to-pink-600 text-white hover:shadow-lg hover:scale-105 transform'
          }`}
        >
          {loading || status === 'requesting' ? (
            <span className="flex items-center justify-center gap-3">
              <div className="spinner w-6 h-6 border-2"></div>
              Requesting...
            </span>
          ) : (
            '🚑 Request Emergency Help'
          )}
        </button>

        <div className="mt-6 text-sm text-gray-500">
          ⚠️ Only use in genuine emergency. Call <span className="font-bold text-gray-800">112</span> directly.
        </div>
      </div>
    </div>
  );
};

export default Emergency;