import React, { useState } from 'react';

interface DocumentUploadProps {
  onUpload: (file: File) => void;
  onCancel: () => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUpload, onCancel }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = e.target.files;
    if (fileList) {
      const filesArray = Array.from(fileList);
      setFiles(filesArray);
    }
  };

  const handleUpload = () => {
    files.forEach((file) => {
      if (file.type !== 'application/pdf') {
        setError('Invalid file format');
      } else if (file.size > 1000000) {
        setError('File size too large');
      } else {
        onUpload(file);
      }
    });
  };

  return (
    <div>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={onCancel}>Cancel</button>
      {error && <p>{error}</p>}
    </div>
  );
};

export default DocumentUpload;
```