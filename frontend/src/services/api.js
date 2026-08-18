import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const login = (user_id, password) => 
  api.post('/auth/login', { user_id, password });

export const register = (userData) => 
  api.post('/auth/register', userData);

export const getProfile = () => 
  api.get('/auth/profile');

export const updateProfile = (data) => 
  api.put('/auth/profile', data);

// Symptom endpoints
export const analyzeSymptoms = (symptoms) => 
  api.post('/symptoms/analyze', { symptoms });

export const checkEmergency = (symptoms) => 
  api.post('/symptoms/emergency', { symptoms });

export const getCommonSymptoms = () => 
  api.get('/symptoms/common');

// Medicine endpoints
export const searchMedicines = (query) => 
  api.get('/medicines/search', { params: { q: query } });

export const getMedicineDetails = (id) => 
  api.get(`/medicines/${id}`);

export const checkInteractions = (medicines) => 
  api.post('/medicines/interactions', { medicines });

// Report endpoints
export const uploadReport = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/reports/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getReports = () => 
  api.get('/reports/history');

export const getReport = (id) => 
  api.get(`/reports/${id}`);

// Hospital endpoints
export const searchHospitals = (lat, lng, radius, specialty) => 
  api.get('/hospitals/search', { params: { lat, lng, radius, specialty } });

export const getHospitalDetails = (id) => 
  api.get(`/hospitals/${id}`);

export const getAvailableBeds = (lat, lng, radius) => 
  api.get('/hospitals/beds', { params: { lat, lng, radius } });

// Ambulance endpoints
export const trackAmbulances = (lat, lng, radius) => 
  api.get('/ambulances/track', { params: { lat, lng, radius } });

export const requestAmbulance = (data) => 
  api.post('/ambulances/request', data);

// Community endpoints
export const getAwarenessContent = (topic) => 
  api.get('/community/awareness', { params: { topic } });

export const getAlerts = (lat, lng) => 
  api.get('/community/alerts', { params: { lat, lng } });

export const createAlert = (data) => 
  api.post('/community/alerts', data);

// Dashboard endpoints
export const getHealthStats = () => 
  api.get('/dashboard/stats');

export const getRecentReports = () => 
  api.get('/dashboard/recent-reports');

export const getUpcomingAppointments = () => 
  api.get('/dashboard/appointments');

export const getEmergencyStatus = () => 
  api.get('/dashboard/emergency-status');

// Emergency endpoints
export const requestEmergencyHelp = (location) => 
  api.post('/emergency/request', location);

export default api;