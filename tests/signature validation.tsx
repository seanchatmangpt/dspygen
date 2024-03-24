import React, { useState, useEffect } from 'react';

interface SignatureValidationProps {
  document: Document;
}

const SignatureValidation: React.FC<SignatureValidationProps> = ({ document }) => {
  const [signature, setSignature] = useState<Signature | null>(null);
  const [isValid, setIsValid] = useState<boolean | null>(null);

  useEffect(() => {
    setSignature(document.signature);
  }, [document]);

  const validateSignature = () => {
    if (signature) {
      setIsValid(signature.isValid);
    }
  };

  return (
    <div>
      <h1>Signature Validation</h1>
      <p>Document: {document.name}</p>
      <p>Signature: {signature ? signature.name : 'No signature found'}</p>
      <button onClick={validateSignature}>Validate Signature</button>
      {isValid !== null && <p>Signature is {isValid ? 'valid' : 'invalid'}</p>}
    </div>
  );
};

export default SignatureValidation;
```