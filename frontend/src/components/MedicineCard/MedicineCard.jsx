import React from 'react';

const MedicineCard = ({ medicine, selected, onSelect }) => {
  return (
    <div 
      className={`bg-white rounded-lg shadow-md p-4 cursor-pointer transition-all duration-200 border-2 ${selected ? 'border-blue-500 bg-blue-50' : 'border-transparent'}`}
      onClick={onSelect}
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-semibold text-gray-800">{medicine.name}</h3>
        <button className={`w-8 h-8 rounded-full ${selected ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-600'} flex items-center justify-center hover:bg-blue-500 hover:text-white transition-colors`}>
          {selected ? '✓' : '+'}
        </button>
      </div>
      
      {medicine.generic_name && (
        <p className="text-sm text-gray-500 mb-2">Generic: {medicine.generic_name}</p>
      )}
      
      {medicine.category && (
        <span className="inline-block px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs mb-2">{medicine.category}</span>
      )}
      
      {medicine.manufacturer && (
        <p className="text-sm text-gray-600 mb-2">{medicine.manufacturer}</p>
      )}
      
      {medicine.price && (
        <p className="text-sm font-medium text-gray-800">₹{medicine.price}</p>
      )}
    </div>
  );
};

export default MedicineCard;
