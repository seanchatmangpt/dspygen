import React, { useState } from 'react';

const DragAndDropDocumentUpload = () => {
  const [document, setDocument] = useState(null);

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setDocument(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      style={{ width: '100%', height: '100%' }}
    >
      {document && <p>{document.name}</p>}
    </div>
  );
};

export default DragAndDropDocumentUpload;
```