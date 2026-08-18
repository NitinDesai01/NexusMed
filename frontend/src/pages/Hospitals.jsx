import React, { useState, useEffect } from 'react';

const Hospitals = () => {
  const [location, setLocation] = useState(null);
  const [hospitals, setHospitals] = useState([]);
  const [beds, setBeds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [radius, setRadius] = useState(25);
  const [specialty, setSpecialty] = useState('');

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
          // Default location (Bangalore)
          setLocation({ lat: 12.9716, lng: 77.5946 });
        }
      );
    } else {
      setLocation({ lat: 12.9716, lng: 77.5946 });
    }
  }, []);

  const handleSearch = async () => {
    setLoading(true);
    setError('');

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      // Get hospitals
      const hospitalResponse = await fetch('http://localhost:5000/api/hospitals/search', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const hospitalData = await hospitalResponse.json();

      // Get available beds
      const bedsResponse = await fetch('http://localhost:5000/api/hospitals/beds', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const bedsData = await bedsResponse.json();

      if (hospitalResponse.ok) {
        setHospitals(hospitalData.hospitals || []);
      } else {
        setError('Failed to fetch hospitals');
      }

      if (bedsResponse.ok) {
        setBeds(bedsData.available_beds || []);
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const getBedStatusColor = (available, total) => {
    const percentage = (available / total) * 100;
    if (percentage > 50) return 'text-green-600';
    if (percentage > 20) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🏥 Hospitals Near You</h1>
        <p className="text-gray-600 mb-6">Find hospitals, check bed availability, and locate emergency services</p>

        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Radius (km)</label>
              <input
                type="number"
                value={radius}
                onChange={(e) => setRadius(Number(e.target.value))}
                min="1"
                max="100"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Specialty</label>
              <input
                type="text"
                value={specialty}
                onChange={(e) => setSpecialty(e.target.value)}
                placeholder="Cardiology, Neurology..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={handleSearch}
                disabled={loading}
                className="w-full px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? '⏳ Searching...' : '🔍 Search'}
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
            {error}
          </div>
        )}

        {beds.length > 0 && (
          <div className="bg-green-50 border border-green-200 rounded-xl p-4 mb-6">
            <h3 className="font-semibold text-green-800 mb-2">🛏️ Available Beds Summary</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {beds.map((bed, index) => (
                <div key={index} className="bg-white rounded-lg p-3 shadow-sm">
                  <p className="font-medium text-gray-800 text-sm">{bed.hospital_name}</p>
                  <p className="text-green-600 font-bold">{bed.available_beds} beds available</p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {hospitals.map((hospital) => (
            <div key={hospital.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">{hospital.name}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-yellow-400">⭐</span>
                      <span className="text-gray-600">{hospital.rating || 4.5}</span>
                      {hospital.emergency_services && (
                        <span className="px-2 py-0.5 bg-red-500 text-white text-xs font-semibold rounded-full animate-pulse">
                          🚨 Emergency
                        </span>
                      )}
                    </div>
                  </div>
                  {hospital.ambulance_available && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full">
                      🚑 Ambulance
                    </span>
                  )}
                </div>

                <p className="text-gray-600 text-sm">{hospital.address}</p>
                <p className="text-gray-500 text-sm">{hospital.city}, {hospital.state}</p>

                <div className="grid grid-cols-4 gap-2 mt-4 p-3 bg-gray-50 rounded-lg">
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Total Beds</p>
                    <p className="text-lg font-bold text-gray-800">{hospital.total_beds}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Available</p>
                    <p className={`text-lg font-bold ${getBedStatusColor(hospital.available_beds, hospital.total_beds)}`}>
                      {hospital.available_beds}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Occupancy</p>
                    <p className="text-lg font-bold text-gray-800">
                      {Math.round(((hospital.total_beds - hospital.available_beds) / hospital.total_beds) * 100)}%
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Distance</p>
                    <p className="text-lg font-bold text-gray-800">
                      {hospital.distance_km ? `${hospital.distance_km}km` : 'N/A'}
                    </p>
                  </div>
                </div>

                {hospital.specialties && (
                  <div className="mt-3 pt-3 border-t">
                    <p className="text-xs text-gray-500 mb-1">Specialties:</p>
                    <div className="flex flex-wrap gap-1">
                      {hospital.specialties.split(',').slice(0, 3).map((spec, i) => (
                        <span key={i} className="px-2 py-0.5 bg-blue-50 text-blue-600 text-xs rounded-full">
                          {spec.trim()}
                        </span>
                      ))}
                      {hospital.specialties.split(',').length > 3 && (
                        <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">
                          +{hospital.specialties.split(',').length - 3} more
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {!loading && hospitals.length === 0 && !error && (
          <div className="bg-white rounded-xl shadow-md p-8 text-center">
            <p className="text-gray-500">No hospitals found. Click "Search" to find hospitals near you.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Hospitals;
