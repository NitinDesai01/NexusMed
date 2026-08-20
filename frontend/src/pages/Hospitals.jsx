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
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        () => {
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
      const hospitalResponse = await fetch('http://localhost:5000/api/hospitals/search', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const hospitalData = await hospitalResponse.json();

      const bedsResponse = await fetch('http://localhost:5000/api/hospitals/beds', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const bedsData = await bedsResponse.json();

      if (hospitalResponse.ok) {
        setHospitals(hospitalData.hospitals || []);
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-3d p-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-white">🏥 Hospitals Near You</h1>
            <p className="text-white/40 mt-1">Find hospitals, check bed availability, and locate emergency services</p>
          </div>
          <div className="glass-light px-4 py-2 rounded-xl text-green-400/80 text-sm flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            {location ? 'Location detected' : 'Location unavailable'}
          </div>
        </div>
      </div>

      {/* Search Filters */}
      <div className="glass-3d p-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-white/60 text-sm font-medium mb-1">Radius (km)</label>
            <input
              type="number"
              value={radius}
              onChange={(e) => setRadius(Number(e.target.value))}
              min="1"
              max="100"
              className="input-3d"
            />
          </div>
          <div>
            <label className="block text-white/60 text-sm font-medium mb-1">Specialty</label>
            <input
              type="text"
              value={specialty}
              onChange={(e) => setSpecialty(e.target.value)}
              placeholder="Cardiology, Neurology..."
              className="input-3d"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleSearch}
              disabled={loading}
              className="btn-3d w-full"
            >
              {loading ? '⏳ Searching...' : '🔍 Search'}
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400">
          ❌ {error}
        </div>
      )}

      {/* Available Beds Summary */}
      {beds.length > 0 && (
        <div className="glass-3d p-6 border border-green-500/20">
          <h3 className="text-green-400 font-semibold mb-3">🛏️ Available Beds Summary</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {beds.map((bed, index) => (
              <div key={index} className="glass-light p-3 rounded-xl">
                <p className="text-white/60 text-sm">{bed.hospital_name}</p>
                <p className="text-green-400 font-bold">{bed.available_beds} beds</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Hospitals List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {hospitals.map((hospital) => (
          <div key={hospital.id} className="card-3d p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold text-white">{hospital.name}</h3>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-yellow-400">⭐</span>
                  <span className="text-white/60">{hospital.rating || 4.5}</span>
                  {hospital.emergency_services && (
                    <span className="badge-3d badge-3d-danger text-xs animate-pulse">🚨 Emergency</span>
                  )}
                </div>
              </div>
              {hospital.ambulance_available && (
                <span className="badge-3d badge-3d-success text-xs">🚑 Ambulance</span>
              )}
            </div>

            <p className="text-white/60 text-sm">{hospital.address}</p>
            <p className="text-white/40 text-sm">{hospital.city}, {hospital.state}</p>

            <div className="grid grid-cols-4 gap-2 mt-4 p-4 glass-light rounded-2xl">
              <div className="text-center">
                <p className="text-white/40 text-xs">Total Beds</p>
                <p className="text-white font-bold">{hospital.total_beds}</p>
              </div>
              <div className="text-center">
                <p className="text-white/40 text-xs">Available</p>
                <p className="text-green-400 font-bold">{hospital.available_beds}</p>
              </div>
              <div className="text-center">
                <p className="text-white/40 text-xs">Occupancy</p>
                <p className="text-white font-bold">
                  {Math.round(((hospital.total_beds - hospital.available_beds) / hospital.total_beds) * 100)}%
                </p>
              </div>
              <div className="text-center">
                <p className="text-white/40 text-xs">Distance</p>
                <p className="text-white font-bold">
                  {hospital.distance_km ? `${hospital.distance_km}km` : 'N/A'}
                </p>
              </div>
            </div>

            {hospital.specialties && (
              <div className="mt-4 pt-4 border-t border-white/5">
                <p className="text-white/40 text-xs mb-2">Specialties:</p>
                <div className="flex flex-wrap gap-1">
                  {hospital.specialties.split(',').slice(0, 3).map((spec, i) => (
                    <span key={i} className="tag-3d tag-3d-blue text-xs">
                      {spec.trim()}
                    </span>
                  ))}
                  {hospital.specialties.split(',').length > 3 && (
                    <span className="text-white/30 text-xs">+{hospital.specialties.split(',').length - 3} more</span>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {!loading && hospitals.length === 0 && !error && (
        <div className="glass-3d p-12 text-center">
          <p className="text-white/40">No hospitals found. Click "Search" to find hospitals near you.</p>
        </div>
      )}
    </div>
  );
};

export default Hospitals;