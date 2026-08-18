import React from 'react';

const StatsCard = ({ title, value, color, icon }) => {
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    red: 'bg-red-500',
    yellow: 'bg-yellow-500',
    indigo: 'bg-indigo-500',
    pink: 'bg-pink-500',
  };

  const bgColor = colorClasses[color] || 'bg-blue-500';

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
        </div>
        <div className={`w-12 h-12 ${bgColor} rounded-lg flex items-center justify-center text-white text-2xl`}>
          {icon}
        </div>
      </div>
    </div>
  );
};

export default StatsCard;
