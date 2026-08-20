import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { AppProvider } from './context/AppContext';
import Navbar from './components/Navbar/Navbar';
import Sidebar from './components/Sidebar/Sidebar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Symptoms from './pages/Symptoms';
import Reports from './pages/Reports';
import Medicines from './pages/Medicines';
import Hospitals from './pages/Hospitals';
import Emergency from './pages/Emergency';
import Profile from './pages/Profile';
import Appointment from './pages/Appointment';
import Community from './pages/Community';
import './index.css';

function App() {
  return (
    <AuthProvider>
      <AppProvider>
        <Router>
          <div className="app-container">
            <Navbar />
            <div className="flex">
              <Sidebar />
              <div className="page-content">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/symptoms" element={<Symptoms />} />
                  <Route path="/reports" element={<Reports />} />
                  <Route path="/medicines" element={<Medicines />} />
                  <Route path="/hospitals" element={<Hospitals />} />
                  <Route path="/emergency" element={<Emergency />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/appointment" element={<Appointment />} />
                  <Route path="/community" element={<Community />} />
                  <Route path="*" element={<Navigate to="/" />} />
                </Routes>
              </div>
            </div>
          </div>
        </Router>
      </AppProvider>
    </AuthProvider>
  );
}

export default App;