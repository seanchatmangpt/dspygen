import React, { useState } from "react";

interface DocumentUploadProps {
  onUpload: (file: File) => void;
  onCancel: () => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUpload,
  onCancel,
}) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setSelectedFiles((prevFiles) => [...prevFiles, ...files]);
    }
  };

  const handleUpload = () => {
    selectedFiles.forEach((file) => onUpload(file));
  };

  const handleCancel = () => {
    setSelectedFiles([]);
    onCancel();
  };

  return (
    <div>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={handleCancel}>Cancel</button>
    </div>
  );
};
```