import React, { useState } from 'react';

const Medicines = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedMedicines, setSelectedMedicines] = useState([]);
  const [interactions, setInteractions] = useState(null);
  const [searchPerformed, setSearchPerformed] = useState(false);

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
    setSearchPerformed(true);
    setSelectedMedicines([]);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/medicines/search?q=${encodeURIComponent(query)}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (response.ok) {
        setResults(data.medicines || []);
        if (!data.medicines || data.medicines.length === 0) {
          setError('No medicines found');
        }
      } else if (response.status === 401) {
        setError('Session expired. Please login again.');
        localStorage.removeItem('token');
        setTimeout(() => window.location.href = '/login', 2000);
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
      setError('Select at least 2 medicines to check interactions');
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      return;
    }

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
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">💊 Medicine Search</h1>
        <p className="text-gray-600 mb-6">Search for medicines and check drug interactions</p>

        <form onSubmit={handleSearch} className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="flex gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by medicine name, generic name, or category..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {loading ? '⏳ Searching...' : '🔍 Search'}
            </button>
          </div>
        </form>

        {error && (
          <div className={`p-4 rounded-lg mb-6 ${error.includes('login') ? 'bg-yellow-50 border border-yellow-200 text-yellow-800' : 'bg-red-50 border border-red-200 text-red-700'}`}>
            {error}
          </div>
        )}

        {searchPerformed && !loading && results.length === 0 && !error && (
          <div className="bg-white rounded-xl shadow-md p-8 text-center">
            <p className="text-gray-500">No medicines found. Try a different search term.</p>
          </div>
        )}

        {results.length > 0 && (
          <div>
            <div className="flex flex-wrap justify-between items-center gap-4 mb-4">
              <h2 className="text-xl font-semibold text-gray-800">
                Search Results ({results.length} medicines found)
              </h2>
              {selectedMedicines.length > 0 && (
                <button
                  onClick={checkInteractions}
                  className="px-6 py-2 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors"
                >
                  🔄 Check Interactions ({selectedMedicines.length})
                </button>
              )}
            </div>
            <p className="text-sm text-gray-500 mb-4">
              Click the + button to select up to 5 medicines for interaction checking
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {results.map((medicine) => {
                const isSelected = selectedMedicines.some(m => m.id === medicine.id);
                return (
                  <div 
                    key={medicine.id}
                    className={`bg-white rounded-xl shadow-md p-5 cursor-pointer transition-all duration-200 border-2 hover:shadow-lg ${
                      isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                    }`}
                    onClick={() => toggleSelect(medicine)}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-800">{medicine.name}</h3>
                        {medicine.generic_name && (
                          <p className="text-sm text-gray-500">Generic: {medicine.generic_name}</p>
                        )}
                      </div>
                      <button 
                        className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors flex-shrink-0 ${
                          isSelected ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-600 hover:bg-blue-500 hover:text-white'
                        }`}
                      >
                        {isSelected ? '✓' : '+'}
                      </button>
                    </div>
                    
                    {medicine.category && (
                      <span className="inline-block mt-2 px-2.5 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                        {medicine.category}
                      </span>
                    )}
                    
                    <div className="mt-3 flex flex-wrap gap-3 text-sm">
                      {medicine.strength && (
                        <span className="text-gray-600">💊 {medicine.strength}</span>
                      )}
                      {medicine.price && (
                        <span className="text-gray-600">💰 ₹{medicine.price}</span>
                      )}
                    </div>
                    
                    {medicine.requires_prescription && (
                      <span className="inline-block mt-2 px-2.5 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                        Prescription Required
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {interactions && (
          <div className="mt-8 bg-white rounded-xl shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">🔄 Drug Interactions</h3>
            
            {interactions.interactions && interactions.interactions.length > 0 ? (
              <div className="space-y-3">
                {interactions.interactions.map((interaction, index) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                    <div className="flex items-center gap-3 flex-wrap">
                      <span className="font-semibold text-gray-800">{interaction.medicine1}</span>
                      <span className="text-gray-400">↔</span>
                      <span className="font-semibold text-gray-800">{interaction.medicine2}</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                        interaction.severity === 'high' ? 'bg-red-100 text-red-700' :
                        interaction.severity === 'moderate' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-green-100 text-green-700'
                      }`}>
                        {interaction.severity.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">{interaction.description}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <p className="text-green-700">✅ No interactions found between selected medicines</p>
              </div>
            )}
            
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">⚠️ {interactions.disclaimer || "This is a preliminary check. Always consult a healthcare professional."}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Medicines;
