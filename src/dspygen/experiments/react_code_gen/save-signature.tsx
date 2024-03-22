import React, { useState } from 'react';

const SaveSignature = () => {
  const [signature, setSignature] = useState('');

  const handleSave = () => {
    // save signature logic
    setSignature('saved');
  };

  return (
    <div>
      <h1>Signature Page</h1>
      <button onClick={handleSave}>Save</button>
      <p>{signature}</p>
    </div>
  );
};

export default SaveSignature;
```