import React, { useState, useEffect } from 'react';

const Appointment = () => {
  const [symptoms, setSymptoms] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    patient_name: '',
    patient_phone: '',
    patient_email: '',
    date: '',
    time: ''
  });
  const [availableSlots, setAvailableSlots] = useState([]);
  const [myAppointments, setMyAppointments] = useState([]);

  useEffect(() => {
    fetchMyAppointments();
  }, []);

  const fetchMyAppointments = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch('http://localhost:5000/api/appointments/my-appointments', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await response.json();
      if (response.ok) {
        setMyAppointments(data.appointments || []);
      }
    } catch (error) {
      console.error('Error fetching appointments:', error);
    }
  };

  const handleFindDoctor = async (e) => {
    e.preventDefault();
    if (!symptoms.trim()) {
      setError('Please describe your symptoms');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');
    setDoctors([]);
    setSelectedDoctor(null);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/appointments/find-doctor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ symptoms: symptoms })
      });

      const data = await response.json();

      if (response.ok && data.recommended_doctors?.length > 0) {
        setAnalysis(data.analysis);
        setDoctors(data.recommended_doctors);
        setStep(2);
        setSuccess(`✅ Found ${data.recommended_doctors.length} doctor(s)`);
        setError('');
      } else {
        setError(data.error || 'No doctors found. Try different symptoms.');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectDoctor = (doctor) => {
    setSelectedDoctor(doctor);
    setStep(3);
    setFormData({ ...formData, date: '', time: '' });
    setAvailableSlots([]);
  };

  const handleDateChange = async (date) => {
    setFormData({ ...formData, date, time: '' });

    if (selectedDoctor && date) {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch(
          `http://localhost:5000/api/appointments/available-slots/${selectedDoctor.id}?date=${date}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        const data = await response.json();
        if (response.ok) {
          setAvailableSlots(data.available_slots || []);
        }
      } catch (error) {
        console.error('Error fetching slots:', error);
      }
    }
  };

  const handleBookAppointment = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/appointments/book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          doctor_id: selectedDoctor.id,
          patient_name: formData.patient_name,
          patient_phone: formData.patient_phone,
          patient_email: formData.patient_email,
          date: formData.date,
          time: formData.time,
          symptoms: symptoms
        })
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess('✅ Appointment booked successfully!');
        setStep(1);
        setSymptoms('');
        setSelectedDoctor(null);
        setDoctors([]);
        setFormData({ patient_name: '', patient_phone: '', patient_email: '', date: '', time: '' });
        fetchMyAppointments();
      } else {
        setError(data.error || 'Booking failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const cancelAppointment = async (bookingId) => {
    if (!window.confirm('Cancel this appointment?')) return;

    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch(`http://localhost:5000/api/appointments/cancel/${bookingId}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.ok) {
        fetchMyAppointments();
        setSuccess('✅ Appointment cancelled');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="card-modern">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">🤖 AI Appointment Agent</h1>
            <p className="text-gray-500 text-sm">Describe your symptoms and our AI will find the right doctor</p>
          </div>
          <div className="bg-gray-100 px-4 py-2 rounded-xl text-gray-600 text-sm font-medium">
            Step {step}/3
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">❌ {error}</div>
      )}

      {success && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-xl text-green-700">{success}</div>
      )}

      {/* Step 1: Describe Symptoms */}
      {step === 1 && (
        <div className="card-modern">
          <h2 className="text-lg font-bold text-gray-800 mb-2">🩺 Describe Your Condition</h2>
          <p className="text-gray-500 text-sm mb-4">Tell us about your symptoms. Our AI will find the best doctor.</p>
          <form onSubmit={handleFindDoctor}>
            <textarea
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="e.g., I have chest pain and shortness of breath"
              className="textarea-field"
              rows="3"
            />
            <div className="flex flex-wrap gap-2 mt-3 mb-4">
              {['Chest Pain', 'Headache', 'Knee Pain', 'Skin Rash', 'Anxiety'].map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => setSymptoms(`I have ${tag.toLowerCase()}`)}
                  className="tag tag-blue"
                >
                  {tag}
                </button>
              ))}
            </div>
            <button type="submit" disabled={loading || !symptoms.trim()} className="btn-3d w-full">
              {loading ? '⏳ Analyzing...' : '🤖 Find Doctor'}
            </button>
          </form>
        </div>
      )}

      {/* Step 2: Recommended Doctors */}
      {step === 2 && (
        <div className="card-modern">
          <h2 className="text-lg font-bold text-gray-800 mb-3">👨‍⚕️ Recommended Doctors</h2>
          {analysis && (
            <div className="bg-blue-50 p-3 rounded-xl text-sm text-blue-700 mb-4">
              <strong>AI Analysis:</strong> Based on "{analysis.symptoms}", we identified <strong>{analysis.identified_specialization}</strong>
            </div>
          )}
          <div className="space-y-3">
            {doctors.map((doctor, index) => (
              <div
                key={doctor.id}
                className={`p-4 rounded-xl cursor-pointer border-2 transition-all ${
                  selectedDoctor?.id === doctor.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                }`}
                onClick={() => handleSelectDoctor(doctor)}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-gray-800 text-lg">{doctor.name}</span>
                      {index === 0 && <span className="badge badge-success text-xs">⭐ Best Match</span>}
                    </div>
                    <p className="text-blue-600 font-medium">{doctor.specialization}</p>
                    <p className="text-sm text-gray-500">{doctor.hospital}</p>
                    <div className="flex items-center gap-4 mt-1 text-sm">
                      <span className="text-gray-600">⭐ {doctor.rating}</span>
                      <span className="text-gray-600">{doctor.experience} years</span>
                      <span className="font-semibold text-green-600">₹{doctor.consultation_fee}</span>
                    </div>
                  </div>
                  <button onClick={() => handleSelectDoctor(doctor)} className="btn-3d text-sm py-2 px-4">
                    Select
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Step 3: Book Appointment */}
      {step === 3 && selectedDoctor && (
        <div className="card-modern">
          <h2 className="text-lg font-bold text-gray-800 mb-3">📋 Book Appointment</h2>
          <div className="bg-green-50 p-4 rounded-xl mb-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-green-800 text-lg">{selectedDoctor.name}</p>
                <p className="text-sm text-gray-600">{selectedDoctor.specialization} • {selectedDoctor.hospital}</p>
                <p className="text-sm font-semibold text-green-700 mt-1">₹{selectedDoctor.consultation_fee}</p>
              </div>
              <button onClick={() => { setStep(2); setSelectedDoctor(null); }} className="text-sm text-blue-600 hover:text-blue-800">
                ← Change
              </button>
            </div>
          </div>

          <form onSubmit={handleBookAppointment}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Patient Name *</label>
                <input
                  type="text"
                  required
                  value={formData.patient_name}
                  onChange={(e) => setFormData({ ...formData, patient_name: e.target.value })}
                  className="input-field"
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
                <input
                  type="tel"
                  required
                  value={formData.patient_phone}
                  onChange={(e) => setFormData({ ...formData, patient_phone: e.target.value })}
                  className="input-field"
                  placeholder="Enter your phone number"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.patient_email}
                  onChange={(e) => setFormData({ ...formData, patient_email: e.target.value })}
                  className="input-field"
                  placeholder="Enter your email"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date *</label>
                <input
                  type="date"
                  required
                  min={new Date().toISOString().split('T')[0]}
                  value={formData.date}
                  onChange={(e) => handleDateChange(e.target.value)}
                  className="input-field"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Time *</label>
                <select
                  required
                  value={formData.time}
                  onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                  className="select-field"
                >
                  <option value="">Select time</option>
                  {availableSlots.map((slot) => (
                    <option key={slot} value={slot}>{slot}</option>
                  ))}
                </select>
                {availableSlots.length === 0 && formData.date && (
                  <p className="text-xs text-yellow-600 mt-1">No slots available for this date</p>
                )}
              </div>
            </div>
            <button type="submit" disabled={loading || !formData.time} className="btn-3d-success w-full mt-4">
              {loading ? '⏳ Booking...' : '✅ Confirm & Book'}
            </button>
          </form>
        </div>
      )}

      {/* My Appointments */}
      <div className="card-modern">
        <h2 className="text-lg font-bold text-gray-800 mb-3">📋 My Appointments</h2>
        {myAppointments.length === 0 ? (
          <p className="text-gray-500 text-sm text-center py-4">No appointments yet</p>
        ) : (
          <div className="space-y-3">
            {myAppointments.map((appointment) => (
              <div key={appointment.booking_id} className="bg-gray-50 p-4 rounded-xl">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-gray-800">{appointment.doctor_name}</p>
                    <p className="text-sm text-blue-600">{appointment.specialization}</p>
                    <p className="text-xs text-gray-500">{appointment.hospital}</p>
                    <p className="text-sm font-medium mt-1">📅 {appointment.date} at {appointment.time}</p>
                  </div>
                  <span className={`badge ${appointment.status === 'confirmed' ? 'badge-success' : 'badge-danger'}`}>
                    {appointment.status}
                  </span>
                </div>
                {appointment.status === 'confirmed' && (
                  <button onClick={() => cancelAppointment(appointment.booking_id)} className="text-sm text-red-600 hover:text-red-800 mt-2">
                    Cancel Appointment
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Appointment;