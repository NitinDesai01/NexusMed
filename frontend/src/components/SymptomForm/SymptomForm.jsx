import React, { useState } from 'react';
import './SymptomForm.css';

const SymptomForm = ({ onSubmit, loading }) => {
  const [symptoms, setSymptoms] = useState('');
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [customSymptom, setCustomSymptom] = useState('');

  const commonSymptoms = [
    'Fever', 'Headache', 'Cough', 'Sore throat', 'Fatigue',
    'Nausea', 'Vomiting', 'Diarrhea', 'Muscle pain', 'Joint pain',
    'Shortness of breath', 'Chest pain', 'Dizziness', 'Rash',
    'Abdominal pain', 'Back pain', 'Neck pain', 'Sweating',
    'Chills', 'Loss of appetite', 'Weight loss', 'Insomnia'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (symptoms.trim() || selectedSymptoms.length > 0) {
      const allSymptoms = [
        ...selectedSymptoms,
        ...(symptoms.trim() ? [symptoms] : [])
      ].join(', ');
      onSubmit(allSymptoms);
    }
  };

  const toggleSymptom = (symptom) => {
    setSelectedSymptoms(prev => {
      if (prev.includes(symptom)) {
        return prev.filter(s => s !== symptom);
      } else {
        return [...prev, symptom];
      }
    });
  };

  const addCustomSymptom = () => {
    if (customSymptom.trim() && !selectedSymptoms.includes(customSymptom)) {
      setSelectedSymptoms([...selectedSymptoms, customSymptom.trim()]);
      setCustomSymptom('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="symptom-form">
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select common symptoms:
        </label>
        <div className="flex flex-wrap gap-2">
          {commonSymptoms.map((symptom) => (
            <button
              key={symptom}
              type="button"
              onClick={() => toggleSymptom(symptom)}
              className={`px-3 py-1 rounded-full text-sm transition-colors ${
                selectedSymptoms.includes(symptom)
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {symptom}
            </button>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Or add custom symptoms:
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={customSymptom}
            onChange={(e) => setCustomSymptom(e.target.value)}
            placeholder="Enter a symptom..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomSymptom())}
          />
          <button
            type="button"
            onClick={addCustomSymptom}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
          >
            Add
          </button>
        </div>
      </div>

      {selectedSymptoms.length > 0 && (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Selected symptoms:
          </label>
          <div className="flex flex-wrap gap-2">
            {selectedSymptoms.map((symptom) => (
              <span
                key={symptom}
                className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm flex items-center"
              >
                {symptom}
                <button
                  type="button"
                  onClick={() => toggleSymptom(symptom)}
                  className="ml-2 text-blue-500 hover:text-blue-700"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Describe your symptoms in detail (optional):
        </label>
        <textarea
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          placeholder="Describe your symptoms, when they started, severity, any triggers..."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows="4"
        />
      </div>

      <button
        type="submit"
        disabled={loading || (selectedSymptoms.length === 0 && !symptoms.trim())}
        className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Analyzing...' : 'Analyze Symptoms'}
      </button>
    </form>
  );
};

export default SymptomForm;