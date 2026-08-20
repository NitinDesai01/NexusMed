import React, { useState } from 'react';

const Medicines = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedMedicines, setSelectedMedicines] = useState([]);
  const [interactions, setInteractions] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError('Please enter a medicine name');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);
    setInteractions(null);
    setSelectedMedicines([]);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/medicines/search?q=${encodeURIComponent(query)}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const data = await response.json();
      if (response.ok) {
        setResults(data.medicines || []);
        if (!data.medicines || data.medicines.length === 0) {
          setError('No medicines found');
        }
      } else {
        setError(data.error || 'Search failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const toggleSelect = (medicine) => {
    setSelectedMedicines(prev => {
      const exists = prev.find(m => m.id === medicine.id);
      if (exists) {
        return prev.filter(m => m.id !== medicine.id);
      } else if (prev.length < 5) {
        return [...prev, medicine];
      }
      return prev;
    });
  };

  const checkInteractions = async () => {
    if (selectedMedicines.length < 2) {
      setError('Select at least 2 medicines');
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) return;

    setLoading(true);
    setError('');

    try {
      const medicineIds = selectedMedicines.map(m => m.id);
      const response = await fetch('http://localhost:5000/api/medicines/interactions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ medicines: medicineIds })
      });

      const data = await response.json();
      if (response.ok) {
        setInteractions(data);
      } else {
        setError(data.error || 'Interaction check failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="card-modern">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">💊 Medicine Search</h1>
            <p className="text-gray-500 mt-1">Search for medicines and check drug interactions</p>
          </div>
          {selectedMedicines.length > 0 && (
            <div className="bg-blue-50 px-4 py-2 rounded-xl text-blue-600 text-sm font-medium">
              {selectedMedicines.length} selected
            </div>
          )}
        </div>
      </div>

      {/* Search Card */}
      <div className="card-modern">
        <form onSubmit={handleSearch} className="flex gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by name, generic name, or category..."
            className="input-field flex-1"
          />
          <button type="submit" disabled={loading} className="btn-primary px-6">
            {loading ? '⏳' : '🔍 Search'}
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">
          ❌ {error}
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">
              Results ({results.length})
            </h2>
            {selectedMedicines.length > 0 && (
              <button onClick={checkInteractions} className="btn-primary text-sm py-2 px-4">
                🔄 Check Interactions ({selectedMedicines.length})
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.map((medicine) => {
              const isSelected = selectedMedicines.some(m => m.id === medicine.id);
              return (
                <div
                  key={medicine.id}
                  className={`card-modern cursor-pointer transition-all ${
                    isSelected ? 'ring-2 ring-blue-500 shadow-lg' : ''
                  }`}
                  onClick={() => toggleSelect(medicine)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800">{medicine.name}</h3>
                      {medicine.generic_name && (
                        <p className="text-sm text-gray-500">Generic: {medicine.generic_name}</p>
                      )}
                    </div>
                    <button className={`w-8 h-8 rounded-full flex items-center justify-center transition-all ${
                      isSelected ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-400 hover:bg-blue-500 hover:text-white'
                    }`}>
                      {isSelected ? '✓' : '+'}
                    </button>
                  </div>

                  {medicine.category && (
                    <span className="tag tag-blue mt-2">{medicine.category}</span>
                  )}

                  <div className="mt-3 flex items-center gap-4 text-sm">
                    {medicine.strength && <span className="text-gray-600">💊 {medicine.strength}</span>}
                    {medicine.price && <span className="text-gray-600">💰 ₹{medicine.price}</span>}
                  </div>

                  {medicine.requires_prescription && (
                    <span className="badge badge-danger mt-2 text-xs">Prescription Required</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Interactions */}
      {interactions && (
        <div className="card-modern">
          <h3 className="text-lg font-bold text-gray-800 mb-4">🔄 Drug Interactions</h3>

          {interactions.interactions?.length > 0 ? (
            <div className="space-y-3">
              {interactions.interactions.map((interaction, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-xl">
                  <div className="flex items-center gap-3 flex-wrap">
                    <span className="font-semibold text-gray-800">{interaction.medicine1}</span>
                    <span className="text-gray-400">↔</span>
                    <span className="font-semibold text-gray-800">{interaction.medicine2}</span>
                    <span className={`badge ${
                      interaction.severity === 'high' ? 'badge-danger' :
                      interaction.severity === 'moderate' ? 'badge-warning' :
                      'badge-success'
                    }`}>
                      {interaction.severity.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{interaction.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-green-50 p-4 rounded-xl text-green-700">✅ No interactions found</div>
          )}

          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-xl text-sm text-yellow-700">
            ⚠️ {interactions.disclaimer || "Consult a healthcare professional for complete information."}
          </div>
        </div>
      )}
    </div>
  );
};

export default Medicines;