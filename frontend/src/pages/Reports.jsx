import React, { useState } from 'react';
import ReportUpload from '../components/ReportUpload/ReportUpload';

const Reports = () => {
  const [reports, setReports] = useState([]);

  const handleUploadSuccess = (newReport) => {
    setReports([newReport, ...reports]);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Medical Reports</h1>
        <p className="text-gray-600 mb-8">
          Upload and manage your medical reports. Our AI will analyze and extract insights from your reports.
        </p>

        <ReportUpload onUploadSuccess={handleUploadSuccess} />

        <div className="mt-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Your Reports</h2>
          
          {reports.length === 0 ? (
            <div className="bg-gray-50 rounded-lg p-8 text-center">
              <p className="text-gray-500">No reports uploaded yet</p>
            </div>
          ) : (
            <div className="space-y-4">
              {reports.map((report, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-800">Report #{index + 1}</h3>
                      <p className="text-sm text-gray-500">Uploaded: {new Date().toLocaleDateString()}</p>
                    </div>
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">✅ Processed</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports;
