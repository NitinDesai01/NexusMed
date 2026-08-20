import React, { useState } from 'react';

const Reports = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [reports, setReports] = useState([]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/tiff'];
      if (!validTypes.includes(selectedFile.type)) {
        setError('Please upload a PDF, JPEG, PNG, or TIFF file');
        setFile(null);
        return;
      }
      if (selectedFile.size > 50 * 1024 * 1024) {
        setError('File size must be less than 50MB');
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');
    setResult(null);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please login first');
      setUploading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:5000/api/reports/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
        setReports([data, ...reports]);
        setFile(null);
      } else {
        setError(data.error || 'Upload failed');
      }
    } catch (error) {
      setError('Failed to connect to backend');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-3d p-8">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold text-white">📄 Medical Reports</h1>
          <p className="text-white/40 mt-1">Upload and manage your medical reports</p>
        </div>
      </div>

      {/* Upload Section */}
      <div className="glass-3d p-8">
        <div className="border-2 border-dashed border-white/20 rounded-2xl p-12 text-center hover:border-blue-500/50 transition-all">
          <div className="text-6xl mb-4">📄</div>
          <p className="text-white/60">
            {file ? file.name : 'Drag and drop your report here'}
          </p>
          <p className="text-white/30 text-sm mt-1">or click to browse</p>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.jpg,.jpeg,.png,.tiff"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            style={{ position: 'absolute' }}
          />
        </div>

        {file && (
          <div className="glass-light p-4 rounded-2xl mt-4 flex items-center justify-between">
            <span className="text-white">{file.name}</span>
            <span className="text-white/40 text-sm">{(file.size / (1024 * 1024)).toFixed(2)} MB</span>
            <button
              onClick={() => setFile(null)}
              className="text-red-400 hover:text-red-300"
            >
              ✕
            </button>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400">
            ❌ {error}
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="btn-3d w-full mt-4"
        >
          {uploading ? '⏳ Uploading...' : '📤 Upload Report'}
        </button>

        <p className="text-white/30 text-xs text-center mt-4">
          Supported formats: PDF, JPEG, PNG, TIFF (Max 50MB)
        </p>
      </div>

      {/* Reports List */}
      {reports.length > 0 && (
        <div className="glass-3d p-8">
          <h2 className="text-xl font-bold text-white mb-4">📋 Your Reports</h2>
          <div className="space-y-3">
            {reports.map((report, index) => (
              <div key={index} className="glass-light p-4 rounded-2xl">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white font-medium">Report #{index + 1}</p>
                    <p className="text-white/40 text-sm">Uploaded: {new Date().toLocaleDateString()}</p>
                  </div>
                  <span className="badge-3d badge-3d-success">✅ Processed</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;