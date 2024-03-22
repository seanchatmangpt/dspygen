import React, { useState } from 'react';

interface SignatureCaptureProps {
  onSave: (signature: string) => void;
}

const SignatureCapture: React.FC<SignatureCaptureProps> = ({ onSave }) => {
  const [signature, setSignature] = useState('');

  const handleSave = () => {
    onSave(signature);
  };

  return (
    <div>
      <h1>Signature Capture</h1>
      <div>
        <h2>Instructions</h2>
        <p>Sign your name in the box below.</p>
      </div>
      <div>
        <h2>Signature</h2>
        <div>
          <input
            type="text"
            value={signature}
            onChange={(e) => setSignature(e.target.value)}
          />
        </div>
      </div>
      <div>
        <button onClick={handleSave}>Save</button>
      </div>
    </div>
  );
};

export default SignatureCapture;
```