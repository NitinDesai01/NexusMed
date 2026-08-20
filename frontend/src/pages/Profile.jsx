import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const Profile = () => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    blood_group: '',
    allergies: '',
    chronic_conditions: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || '',
        email: user.email || '',
        phone: user.phone || '',
        date_of_birth: user.date_of_birth || '',
        gender: user.gender || '',
        blood_group: user.blood_group || '',
        allergies: user.allergies || '',
        chronic_conditions: user.chronic_conditions || ''
      });
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/auth/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
        setMessage('✅ Profile updated successfully');
      } else {
        setError(data.error || 'Update failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-3d p-8">
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-500 text-white flex items-center justify-center text-3xl font-bold shadow-lg shadow-purple-500/20">
            {formData.name?.charAt(0) || 'U'}
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white">Profile</h1>
            <p className="text-white/40">Manage your personal health information</p>
          </div>
        </div>
      </div>

      {/* Profile Form */}
      <div className="glass-3d p-8">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-white/60 text-sm font-medium mb-1">Full Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="input-3d"
              />
            </div>
            <div>
              <label className="block text-white/60 text-sm font-medium mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="input-3d"
              />
            </div>
            <div>
              <label className="block text-white/60 text-sm font-medium mb-1">Phone</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="input-3d"
              />
            </div>
            <div>
              <label className="block text-white/60 text-sm font-medium mb-1">Date of Birth</label>
              <input
                type="date"
                name="date_of_birth"
                value={formData.date_of_birth}
                onChange={handleChange}
                className="input-3d"
              />
            </div>
            <div>
              <label className="block text-white/60 text-sm font-medium mb-1">Gender</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="input-3d"
              >
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="non-binary">Non-binary</option>
                <option value="prefer-not-to-say">Prefer not to say</option>
              </select>
            </div>
            <div>
              <label className="block text-white/60 text-sm font-medium mb-1">Blood Group</label>
              <select
                name="blood_group"
                value={formData.blood_group}
                onChange={handleChange}
                className="input-3d"
              >
                <option value="">Select blood group</option>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-white/60 text-sm font-medium mb-1">Allergies</label>
              <input
                type="text"
                name="allergies"
                value={formData.allergies}
                onChange={handleChange}
                placeholder="e.g., Peanuts, Penicillin"
                className="input-3d"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-white/60 text-sm font-medium mb-1">Chronic Conditions</label>
              <input
                type="text"
                name="chronic_conditions"
                value={formData.chronic_conditions}
                onChange={handleChange}
                placeholder="e.g., Diabetes, Hypertension"
                className="input-3d"
              />
            </div>
          </div>

          {message && (
            <div className="mt-4 p-4 rounded-2xl bg-green-500/10 border border-green-500/20 text-green-400">
              {message}
            </div>
          )}

          {error && (
            <div className="mt-4 p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400">
              ❌ {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn-3d w-full mt-6"
          >
            {loading ? '⏳ Saving...' : '💾 Save Changes'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Profile;