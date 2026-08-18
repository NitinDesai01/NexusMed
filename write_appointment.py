import os

content = '''import React, { useState, useEffect } from "react";

const Appointment = () => {
  const [symptoms, setSymptoms] = useState("");
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [analysis, setAnalysis] = useState(null);
  const [recommendedDoctors, setRecommendedDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState(null);

  const [formData, setFormData] = useState({
    patient_name: "",
    patient_phone: "",
    patient_email: "",
    date: "",
    time: ""
  });

  const [availableSlots, setAvailableSlots] = useState([]);
  const [myAppointments, setMyAppointments] = useState([]);

  useEffect(() => {
    fetchMyAppointments();
  }, []);

  const fetchMyAppointments = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await fetch("http://localhost:5000/api/appointments/my-appointments", {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await response.json();
      if (response.ok) {
        setMyAppointments(data.appointments || []);
      }
    } catch (error) {
      console.error("Error fetching appointments:", error);
    }
  };

  const handleFindDoctor = async (e) => {
    e.preventDefault();
    if (!symptoms.trim()) {
      setError("Please describe your symptoms");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");
    setRecommendedDoctors([]);
    setSelectedDoctor(null);

    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please login first");
      setLoading(false);
      return;
    }

    try {
      console.log("Sending symptoms:", symptoms);
      console.log("Token:", token);

      const response = await fetch("http://localhost:5000/api/appointments/find-doctor", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ symptoms: symptoms })
      });

      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Response data:", data);

      if (response.ok) {
        setAnalysis(data.analysis);
        setRecommendedDoctors(data.recommended_doctors || []);
        setStep(2);
        if (data.recommended_doctors && data.recommended_doctors.length > 0) {
          setSuccess(`✅ Found ${data.recommended_doctors.length} doctors for your condition`);
        } else {
          setError("No doctors found. Try describing your symptoms differently.");
        }
      } else {
        setError(data.error || "Failed to find doctors");
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setError("Failed to connect to backend. Make sure it's running.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectDoctor = (doctor) => {
    setSelectedDoctor(doctor);
    setStep(3);
    setFormData({ ...formData, date: "", time: "" });
    setAvailableSlots([]);
  };

  const handleDateChange = async (date) => {
    setFormData({ ...formData, date, time: "" });

    if (selectedDoctor && date) {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(
          `http://localhost:5000/api/appointments/available-slots/${selectedDoctor.id}?date=${date}`,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        const data = await response.json();
        if (response.ok) {
          setAvailableSlots(data.available_slots || []);
        }
      } catch (error) {
        console.error("Error fetching slots:", error);
      }
    }
  };

  const handleBookAppointment = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please login first");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/appointments/book", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
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
        setSuccess(data.message || "✅ Appointment booked successfully!");
        setStep(1);
        setSymptoms("");
        setSelectedDoctor(null);
        setRecommendedDoctors([]);
        setFormData({ patient_name: "", patient_phone: "", patient_email: "", date: "", time: "" });
        fetchMyAppointments();
      } else {
        setError(data.error || "Booking failed");
      }
    } catch (error) {
      setError("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  const cancelAppointment = async (bookingId) => {
    if (!window.confirm("Are you sure you want to cancel this appointment?")) return;

    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await fetch(`http://localhost:5000/api/appointments/cancel/${bookingId}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.ok) {
        fetchMyAppointments();
        setSuccess("✅ Appointment cancelled successfully");
      }
    } catch (error) {
      console.error("Error cancelling appointment:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🤖 AI Appointment Agent</h1>
        <p className="text-gray-600 mb-6">
          Describe your symptoms and our AI will find and book the right doctor for you
        </p>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
            ❌ {error}
          </div>
        )}

        {success && (
          <div className="bg-green-50 border border-green-200 text-green-700 p-4 rounded-lg mb-6">
            {success}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            {step === 1 && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4">🩺 Step 1: Describe Your Condition</h2>
                <p className="text-gray-600 text-sm mb-4">
                  Tell us about your symptoms or condition. Our AI will find the best doctor for you.
                </p>
                <form onSubmit={handleFindDoctor}>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Describe your symptoms or condition:
                    </label>
                    <textarea
                      value={symptoms}
                      onChange={(e) => setSymptoms(e.target.value)}
                      placeholder="e.g., I have chest pain and shortness of breath"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 resize-none"
                      rows="4"
                    />
                  </div>
                  <div className="flex gap-2 flex-wrap mb-4">
                    <button
                      type="button"
                      onClick={() => setSymptoms("I have chest pain and shortness of breath")}
                      className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm hover:bg-gray-200"
                    >
                      Chest Pain
                    </button>
                    <button
                      type="button"
                      onClick={() => setSymptoms("I have severe headache and dizziness")}
                      className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm hover:bg-gray-200"
                    >
                      Headache
                    </button>
                    <button
                      type="button"
                      onClick={() => setSymptoms("I have knee pain and swelling")}
                      className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm hover:bg-gray-200"
                    >
                      Knee Pain
                    </button>
                    <button
                      type="button"
                      onClick={() => setSymptoms("I have skin rash and itching")}
                      className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm hover:bg-gray-200"
                    >
                      Skin Rash
                    </button>
                    <button
                      type="button"
                      onClick={() => setSymptoms("I have anxiety and trouble sleeping")}
                      className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm hover:bg-gray-200"
                    >
                      Anxiety
                    </button>
                  </div>
                  <button
                    type="submit"
                    disabled={loading || !symptoms.trim()}
                    className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                  >
                    {loading ? "🤖 AI is analyzing..." : "🤖 Find Doctor"}
                  </button>
                </form>
              </div>
            )}

            {step === 2 && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-2">👨‍⚕️ Step 2: Recommended Doctors</h2>
                {analysis && (
                  <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm text-blue-800">
                      <strong>AI Analysis:</strong> Based on "{analysis.symptoms}", we identified
                      <strong> {analysis.identified_specialization}</strong> as the best match
                    </p>
                  </div>
                )}

                {recommendedDoctors.length === 0 ? (
                  <div className="p-4 bg-yellow-50 rounded-lg">
                    <p className="text-yellow-700">No doctors found. Please try describing your symptoms differently.</p>
                    <button
                      onClick={() => { setStep(1); setRecommendedDoctors([]); }}
                      className="mt-2 text-blue-600 hover:text-blue-800"
                    >
                      ← Go back
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {recommendedDoctors.map((doctor, index) => (
                      <div
                        key={doctor.id}
                        className={`p-4 rounded-lg cursor-pointer border-2 transition-all ${
                          selectedDoctor?.id === doctor.id
                            ? "border-blue-500 bg-blue-50"
                            : "border-gray-200 hover:border-blue-300 bg-gray-50"
                        }`}
                        onClick={() => handleSelectDoctor(doctor)}
                      >
                        <div className="flex justify-between items-start">
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-semibold text-gray-800">{doctor.name}</span>
                              {index === 0 && (
                                <span className="px-2 py-0.5 bg-yellow-500 text-white text-xs font-bold rounded-full">
                                  ⭐ Best Match
                                </span>
                              )}
                            </div>
                            <p className="text-blue-600">{doctor.specialization}</p>
                            <p className="text-sm text-gray-500">{doctor.hospital}</p>
                            <p className="text-sm text-gray-600 mt-1">
                              ⭐ {doctor.rating} • {doctor.experience} years
                            </p>
                            <p className="text-sm font-semibold mt-1">₹{doctor.consultation_fee}</p>
                          </div>
                          <button
                            onClick={() => handleSelectDoctor(doctor)}
                            className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
                          >
                            Select
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {step === 3 && selectedDoctor && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4">📋 Step 3: Book Appointment</h2>

                <div className="mb-4 p-3 bg-green-50 rounded-lg">
                  <p className="font-semibold text-green-800">Selected Doctor: {selectedDoctor.name}</p>
                  <p className="text-sm text-gray-600">
                    {selectedDoctor.specialization} • {selectedDoctor.hospital}
                  </p>
                  <p className="text-sm font-semibold mt-1">₹{selectedDoctor.consultation_fee}</p>
                  <button
                    onClick={() => { setStep(2); setSelectedDoctor(null); }}
                    className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                  >
                    ← Change doctor
                  </button>
                </div>

                <form onSubmit={handleBookAppointment}>
                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Patient Name *</label>
                    <input
                      type="text"
                      required
                      value={formData.patient_name}
                      onChange={(e) => setFormData({ ...formData, patient_name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="Enter your full name"
                    />
                  </div>

                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
                    <input
                      type="tel"
                      required
                      value={formData.patient_phone}
                      onChange={(e) => setFormData({ ...formData, patient_phone: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="Enter your phone number"
                    />
                  </div>

                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input
                      type="email"
                      value={formData.patient_email}
                      onChange={(e) => setFormData({ ...formData, patient_email: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="Enter your email"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div className="mb-3">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date *</label>
                      <input
                        type="date"
                        required
                        min={new Date().toISOString().split("T")[0]}
                        value={formData.date}
                        onChange={(e) => handleDateChange(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>

                    <div className="mb-3">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Time *</label>
                      <select
                        required
                        value={formData.time}
                        onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      >
                        <option value="">Select time</option>
                        {availableSlots.map((slot) => (
                          <option key={slot} value={slot}>{slot}</option>
                        ))}
                      </select>
                      {availableSlots.length === 0 && formData.date && (
                        <p className="text-xs text-yellow-600 mt-1">No available slots for this date</p>
                      )}
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={loading || !formData.time}
                    className="w-full py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
                  >
                    {loading ? "⏳ Booking..." : "✅ Confirm & Book"}
                  </button>
                </form>
              </div>
            )}
          </div>

          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-md p-4">
              <h2 className="font-semibold text-lg text-gray-800 mb-4">📋 My Appointments</h2>

              {myAppointments.length === 0 ? (
                <p className="text-gray-500 text-sm text-center py-4">No appointments yet</p>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {myAppointments.map((appointment) => (
                    <div key={appointment.booking_id} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-semibold text-gray-800">{appointment.doctor_name}</p>
                          <p className="text-sm text-blue-600">{appointment.specialization}</p>
                          <p className="text-xs text-gray-500">{appointment.hospital}</p>
                          <p className="text-sm font-medium mt-1">
                            📅 {appointment.date} at {appointment.time}
                          </p>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          appointment.status === "confirmed" ? "bg-green-100 text-green-700" :
                          appointment.status === "cancelled" ? "bg-red-100 text-red-700" :
                          "bg-yellow-100 text-yellow-700"
                        }`}>
                          {appointment.status}
                        </span>
                      </div>
                      {appointment.status === "confirmed" && (
                        <button
                          onClick={() => cancelAppointment(appointment.booking_id)}
                          className="mt-2 text-sm text-red-600 hover:text-red-800"
                        >
                          Cancel Appointment
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Appointment;'''

# Write the file
filepath = "frontend/src/pages/Appointment.jsx"
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ File written to {filepath}")
