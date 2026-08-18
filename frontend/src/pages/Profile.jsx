import React from 'react';
import { useAuth } from '../context/AuthContext';

const Profile = () => {
  const { user } = useAuth();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-800">Profile</h1>
            <div className="w-16 h-16 rounded-full bg-blue-500 text-white flex items-center justify-center text-2xl font-bold">
              {user?.name?.charAt(0) || 'U'}
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm text-gray-500">Name</label>
              <p className="font-medium">{user?.name || 'Guest'}</p>
            </div>
            <div>
              <label className="text-sm text-gray-500">Email</label>
              <p className="font-medium">{user?.email || 'guest@nexusmed.com'}</p>
            </div>
            <div>
              <label className="text-sm text-gray-500">User ID</label>
              <p className="font-medium">demo_user</p>
            </div>
            <div>
              <label className="text-sm text-gray-500">Member Since</label>
              <p className="font-medium">January 2024</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
