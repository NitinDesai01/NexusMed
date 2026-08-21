import React, { useState } from 'react';

const AutomatedAgent = () => {
  const [symptoms, setSymptoms] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1);
  const [patientDetails, setPatientDetails] = useState({
    name: '',
    phone: '',
    email: ''
  });
  const [sessionId, setSessionId] = useState('');
  const [bookingStatus, setBookingStatus] = useState(null);
  const [ambulanceStatus, setAmbulanceStatus] = useState(null);
  const [showPermissionModal, setShowPermissionModal] = useState(false);
  const [permissionType, setPermissionType] = useState('');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!symptoms.trim()) {
      setError('Please describe your symptoms');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/automated/analyze-and-act', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          symptoms: symptoms,
          patient_name: patientDetails.name || 'Patient',
          patient_phone: patientDetails.phone || '',
          patient_email: patientDetails.email || ''
        })
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
        setSessionId(data.session_id);
        setStep(2);
        setError('');
        
        // Check if permission is needed
        if (data.permission_requests?.appointment?.required || data.permission_requests?.ambulance?.required) {
          setShowPermissionModal(true);
        }
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const handlePermissionResponse = async (action, confirm) => {
    setLoading(true);
    setError('');
    setShowPermissionModal(false);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      let endpoint = '';
      let body = { session_id: sessionId, confirm: confirm };

      if (action === 'appointment') {
        endpoint = 'http://localhost:5000/api/automated/confirm-appointment';
      } else if (action === 'ambulance') {
        endpoint = 'http://localhost:5000/api/automated/confirm-ambulance';
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });

      const data = await response.json();
      if (response.ok) {
        if (action === 'appointment') {
          setBookingStatus(data);
          setStep(3);
        } else if (action === 'ambulance') {
          setAmbulanceStatus(data);
          setStep(4);
        }
        setError('');
      } else {
        setError(data.error || 'Action failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setStep(1);
    setResult(null);
    setSymptoms('');
    setError('');
    setSessionId('');
    setBookingStatus(null);
    setAmbulanceStatus(null);
    setShowPermissionModal(false);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="card-modern">
        <div className="flex items-center gap-3">
          <span className="text-4xl">🤖</span>
          <div>
            <h1 className="text-2xl font-bold text-gray-800">AI Health Assistant</h1>
            <p className="text-gray-500">Describe your symptoms and our AI will handle everything automatically</p>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">❌ {error}</div>
      )}

      {/* Permission Modal */}
      {showPermissionModal && result && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <div className="text-center mb-4">
              <div className="text-4xl mb-2">🤔</div>
              <h3 className="text-xl font-bold text-gray-800">Permission Required</h3>
              <p className="text-gray-500 text-sm">AI needs your permission to proceed</p>
            </div>

            <div className="space-y-4">
              {result.permission_requests?.appointment?.required && (
                <div className="p-4 bg-blue-50 rounded-xl">
                  <p className="font-semibold text-gray-800">📅 Appointment Booking</p>
                  <p className="text-sm text-gray-600">{result.permission_requests.appointment.message}</p>
                  <div className="flex gap-3 mt-3">
                    <button
                      onClick={() => handlePermissionResponse('appointment', true)}
                      className="flex-1 btn-3d text-sm py-2"
                    >
                      Yes, Book
                    </button>
                    <button
                      onClick={() => handlePermissionResponse('appointment', false)}
                      className="flex-1 btn-secondary text-sm py-2"
                    >
                      No, Skip
                    </button>
                  </div>
                </div>
              )}

              {result.permission_requests?.ambulance?.required && (
                <div className="p-4 bg-red-50 rounded-xl">
                  <p className="font-semibold text-gray-800 text-red-700">🚨 Emergency Ambulance</p>
                  <p className="text-sm text-gray-600">{result.permission_requests.ambulance.message}</p>
                  <div className="flex gap-3 mt-3">
                    <button
                      onClick={() => handlePermissionResponse('ambulance', true)}
                      className="flex-1 btn-3d-danger text-sm py-2"
                    >
                      Yes, Call Ambulance
                    </button>
                    <button
                      onClick={() => handlePermissionResponse('ambulance', false)}
                      className="flex-1 btn-secondary text-sm py-2"
                    >
                      No, Skip
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Step 1: Symptoms Input */}
      {step === 1 && (
        <div className="card-modern">
          <h2 className="text-lg font-bold text-gray-800 mb-3">🩺 Describe Your Symptoms</h2>
          <p className="text-gray-500 text-sm mb-4">Our AI will analyze, find the right doctor, recommend medicines, and handle emergencies.</p>
          <form onSubmit={handleAnalyze}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Your Symptoms</label>
              <textarea
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                placeholder="e.g., I have chest pain, shortness of breath, and sweating..."
                className="textarea-field"
                rows="4"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Your Name</label>
                <input
                  type="text"
                  value={patientDetails.name}
                  onChange={(e) => setPatientDetails({ ...patientDetails, name: e.target.value })}
                  className="input-field"
                  placeholder="Enter your name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Phone Number</label>
                <input
                  type="tel"
                  value={patientDetails.phone}
                  onChange={(e) => setPatientDetails({ ...patientDetails, phone: e.target.value })}
                  className="input-field"
                  placeholder="Enter your phone number"
                />
              </div>
            </div>

            <button type="submit" disabled={loading} className="btn-3d w-full">
              {loading ? '🤖 AI is analyzing...' : '🚀 Analyze & Take Action'}
            </button>

            <div className="mt-3 flex flex-wrap gap-2">
              <button type="button" onClick={() => setSymptoms('I have chest pain and shortness of breath')} className="tag tag-blue text-xs">Chest Pain</button>
              <button type="button" onClick={() => setSymptoms('I have severe headache and dizziness')} className="tag tag-blue text-xs">Headache</button>
              <button type="button" onClick={() => setSymptoms('I have knee pain and swelling')} className="tag tag-blue text-xs">Knee Pain</button>
              <button type="button" onClick={() => setSymptoms('I have skin rash and itching')} className="tag tag-blue text-xs">Skin Rash</button>
              <button type="button" onClick={() => setSymptoms('I have fever and cough')} className="tag tag-blue text-xs">Fever + Cough</button>
            </div>
          </form>
        </div>
      )}

      {/* Step 2: Analysis Results */}
      {step === 2 && result && !showPermissionModal && (
        <div className="card-modern fade-in-up">
          <h2 className="text-lg font-bold text-gray-800 mb-4">📊 Analysis Results</h2>

          {/* Emergency Alert */}
          {result.emergency_check.is_emergency && (
            <div className="p-4 bg-red-50 border-2 border-red-300 rounded-xl mb-4">
              <p className="text-red-700 font-bold text-lg">🚨 EMERGENCY DETECTED</p>
              <p className="text-red-600">{result.emergency_check.message}</p>
            </div>
          )}

          {/* Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Symptoms Analyzed</p>
              <p className="font-medium text-gray-800">{result.analysis.symptoms_analyzed}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-xl">
              <p className="text-sm text-gray-500">Severity</p>
              <span className={`badge ${result.analysis.severity === 'high' ? 'badge-danger' : result.analysis.severity === 'medium' ? 'badge-warning' : 'badge-success'}`}>
                {result.analysis.severity.toUpperCase()}
              </span>
            </div>
          </div>

          {/* Predictions */}
          {result.predictions && result.predictions.length > 0 && (
            <div className="mt-4">
              <p className="text-sm font-medium text-gray-700 mb-2">🔍 Possible Conditions</p>
              <div className="space-y-2">
                {result.predictions.slice(0, 3).map((pred, i) => (
                  <div key={i} className="bg-gray-50 p-3 rounded-xl flex items-center justify-between">
                    <span className="text-gray-800">{pred.disease}</span>
                    <div className="flex items-center gap-3">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${pred.confidence}%` }}></div>
                      </div>
                      <span className="text-sm font-semibold text-blue-600">{pred.confidence}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommended Medicines */}
          {result.recommended_medicines && result.recommended_medicines.length > 0 && (
            <div className="mt-4">
              <p className="text-sm font-medium text-gray-700 mb-2">💊 Recommended Medicines</p>
              <div className="space-y-2">
                {result.recommended_medicines.map((med, i) => (
                  <div key={i} className="bg-green-50 p-3 rounded-xl flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-gray-800">{med.name}</p>
                      <p className="text-sm text-gray-600">{med.dosage} - {med.frequency}</p>
                    </div>
                    <span className="text-xs text-gray-500">{med.purpose}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Summary */}
          <div className="mt-4 p-3 bg-gray-50 rounded-xl">
            <p className="text-sm text-gray-600">{result.summary}</p>
          </div>

          <button onClick={handleReset} className="mt-4 btn-secondary w-full">
            🔄 Start New Analysis
          </button>
        </div>
      )}

      {/* Step 3: Appointment Booked */}
      {step === 3 && bookingStatus && (
        <div className="card-modern border-2 border-green-300">
          <div className="text-center">
            <div className="text-5xl mb-3">✅</div>
            <h2 className="text-2xl font-bold text-green-700">Appointment Booked!</h2>
            <p className="text-gray-600">Your appointment has been confirmed.</p>
          </div>
          <div className="mt-4 space-y-3">
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Doctor</span>
              <span className="font-medium">{bookingStatus.booking?.doctor_name}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Specialization</span>
              <span className="font-medium">{bookingStatus.booking?.specialization}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Hospital</span>
              <span className="font-medium">{bookingStatus.booking?.hospital}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Date & Time</span>
              <span className="font-medium">{bookingStatus.booking?.date} at {bookingStatus.booking?.time}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Fee</span>
              <span className="font-medium text-green-600">₹{bookingStatus.booking?.consultation_fee}</span>
            </div>
          </div>
          <button onClick={handleReset} className="mt-4 btn-primary w-full">
            🔄 Start New Analysis
          </button>
        </div>
      )}

      {/* Step 4: Ambulance Dispatched */}
      {step === 4 && ambulanceStatus && (
        <div className="card-modern border-2 border-red-300">
          <div className="text-center">
            <div className="text-5xl mb-3 animate-pulse">🚑</div>
            <h2 className="text-2xl font-bold text-red-700">Ambulance Dispatched!</h2>
            <p className="text-gray-600">Emergency services are on their way to your location.</p>
          </div>
          <div className="mt-4 space-y-3">
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Request ID</span>
              <span className="font-medium">{ambulanceStatus.request_id}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Ambulance</span>
              <span className="font-medium">{ambulanceStatus.ambulance?.vehicle_number}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Driver</span>
              <span className="font-medium">{ambulanceStatus.ambulance?.driver_name}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">ETA</span>
              <span className="font-medium text-red-600">{ambulanceStatus.ambulance?.estimated_arrival}</span>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl flex justify-between">
              <span className="text-gray-500">Equipment</span>
              <span className="font-medium">{ambulanceStatus.ambulance?.equipment_level}</span>
            </div>
          </div>
          <button onClick={handleReset} className="mt-4 btn-primary w-full">
            🔄 Start New Analysis
          </button>
        </div>
      )}
    </div>
  );
};

export default AutomatedAgent;