import React from 'react';

const HospitalCard = ({ hospital }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-800">{hospital.name}</h3>
          {hospital.rating && (
            <div className="flex items-center mt-1">
              <span className="text-yellow-400">⭐</span>
              <span className="text-gray-600 ml-1">{hospital.rating.toFixed(1)}</span>
            </div>
          )}
        </div>
        {hospital.emergency_services && (
          <span className="px-3 py-1 bg-red-500 text-white rounded-full text-sm font-semibold animate-pulse">🚨 Emergency</span>
        )}
      </div>
      
      <p className="text-gray-600">{hospital.address}</p>
      <p className="text-sm text-gray-500 mt-1">{hospital.city}, {hospital.state}</p>
      
      <div className="grid grid-cols-4 gap-4 mt-4 p-3 bg-gray-50 rounded-lg">
        <div className="text-center">
          <span className="block text-xs text-gray-500">Total Beds</span>
          <span className="block text-lg font-semibold text-gray-800">{hospital.total_beds}</span>
        </div>
        <div className="text-center">
          <span className="block text-xs text-gray-500">Available</span>
          <span className="block text-lg font-semibold text-green-600">{hospital.available_beds}</span>
        </div>
        {hospital.ambulance_available && (
          <div className="text-center">
            <span className="block text-xs text-gray-500">Ambulance</span>
            <span className="block text-lg font-semibold text-green-600">✓</span>
          </div>
        )}
        {hospital.distance_km && (
          <div className="text-center">
            <span className="block text-xs text-gray-500">Distance</span>
            <span className="block text-lg font-semibold text-gray-800">{hospital.distance_km} km</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default HospitalCard;
