import React, { useState, useRef } from 'react';

const ReportUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

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
      setMessage('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setProgress(0);
    setError('');
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 95) {
            clearInterval(progressInterval);
            return 95;
          }
          return prev + 5;
        });
      }, 500);

      const response = await fetch('http://localhost:5000/api/reports/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      clearInterval(progressInterval);
      setProgress(100);
      setMessage('Report uploaded and processed successfully!');
      
      if (onUploadSuccess && response.ok) {
        const data = await response.json();
        onUploadSuccess(data);
      }

      setTimeout(() => {
        setFile(null);
        setProgress(0);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      }, 3000);

    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all">
        <div className="flex flex-col items-center">
          <div className="text-5xl mb-4">📄</div>
          <p className="text-lg font-medium text-gray-700">
            {file ? file.name : 'Drag and drop your report here'}
          </p>
          <p className="text-sm text-gray-500 mt-1">or click to browse</p>
          <input
            ref={fileInputRef}
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.jpg,.jpeg,.png,.tiff"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
        </div>
      </div>

      {file && (
        <div className="mt-4 p-3 bg-gray-50 rounded-lg flex items-center justify-between">
          <span className="font-medium text-gray-700">{file.name}</span>
          <span className="text-sm text-gray-500">{(file.size / (1024 * 1024)).toFixed(2)} MB</span>
          <button
            onClick={() => {
              setFile(null);
              if (fileInputRef.current) {
                fileInputRef.current.value = '';
              }
            }}
            className="text-red-500 hover:text-red-700 text-xl font-bold cursor-pointer"
          >
            ×
          </button>
        </div>
      )}

      {progress > 0 && progress < 100 && (
        <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
          <div className="bg-blue-600 h-2 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
        </div>
      )}

      {message && (
        <div className="mt-4 text-green-600 font-medium">{message}</div>
      )}

      {error && (
        <div className="mt-4 text-red-600 font-medium">{error}</div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="mt-4 w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {uploading ? 'Uploading...' : 'Upload Report'}
      </button>

      <p className="mt-2 text-sm text-gray-500 text-center">
        Supported formats: PDF, JPEG, PNG, TIFF (Max 50MB)
      </p>
    </div>
  );
};

export default ReportUpload;
