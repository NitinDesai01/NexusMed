import React from 'react';

const AmbulanceTracker = ({ latitude, longitude, ambulanceData }) => {
  const ambulances = ambulanceData || [];

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">🚑 Ambulance Tracker</h3>
        <span className="text-sm font-medium text-gray-600">
          {ambulances.length > 0 ? '🟢 Active' : '🟡 No ambulances nearby'}
        </span>
      </div>

      <div className="max-h-96 overflow-y-auto">
        {ambulances.length > 0 ? (
          <div className="space-y-3">
            {ambulances.map((ambulance, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">🚑</div>
                  <div>
                    <p className="font-medium text-gray-800">{ambulance.vehicle_number || `Ambulance ${index + 1}`}</p>
                    <p className="text-sm text-gray-600">
                      Status: <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${ambulance.status === 'available' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {ambulance.status || 'Available'}
                      </span>
                    </p>
                    {ambulance.distance_km && (
                      <p className="text-sm text-gray-500">Distance: {ambulance.distance_km} km</p>
                    )}
                  </div>
                </div>
                {ambulance.driver_phone && (
                  <a href={`tel:${ambulance.driver_phone}`} className="px-3 py-1 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm">
                    📞 Call
                  </a>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500">No ambulances available in your area</p>
            <p className="text-sm text-gray-400 mt-1">Please try again later or call emergency services</p>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <span className="text-gray-400">📍</span>
          <span className="text-sm text-gray-600">
            {latitude && longitude ? `${latitude.toFixed(4)}, ${longitude.toFixed(4)}` : 'Location not available'}
          </span>
        </div>
        <button onClick={() => window.location.reload()} className="px-3 py-1 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm">
          🔄 Refresh
        </button>
      </div>
    </div>
  );
};

export default AmbulanceTracker;
