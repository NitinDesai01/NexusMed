import React, { useState } from 'react';

const Emergency = () => {
  const [status, setStatus] = useState('idle');

  const handleEmergency = async () => {
    setStatus('requesting');
    
    try {
      const response = await fetch('http://localhost:5000/api/ambulances/request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          lat: 12.9716,
          lng: 77.5946,
          patient_name: 'Demo Patient',
          patient_phone: '1234567890'
        })
      });

      const data = await response.json();
      setStatus('success');
      alert('🚑 Ambulance dispatched! Request ID: ' + data.request_id);
    } catch (error) {
      setStatus('error');
      alert('Error requesting ambulance. Make sure the backend is running.');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🚨</div>
            <h1 className="text-3xl font-bold text-gray-800">Emergency Help</h1>
            <p className="text-gray-600 mt-2">Click the button below to request immediate emergency assistance</p>
          </div>

          <button
            onClick={handleEmergency}
            disabled={status === 'requesting'}
            className={`w-full py-4 text-white text-lg font-semibold rounded-lg transition-colors ${
              status === 'requesting' ? 'bg-gray-400 cursor-not-allowed' : 'bg-red-600 hover:bg-red-700'
            }`}
          >
            {status === 'requesting' ? 'Requesting Help...' : '🚑 Request Emergency Help'}
          </button>

          <div className="mt-6 text-sm text-gray-500 text-center">
            <p>⚠️ Only use this in case of a genuine medical emergency.</p>
            <p className="mt-1">You can also call emergency services directly at 112</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Emergency;
