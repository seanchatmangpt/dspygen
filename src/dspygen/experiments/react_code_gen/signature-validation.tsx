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
      <button onClick={validateSignature}>Validate Signature</button>
      {isValid !== null && (
        <p>{isValid ? 'The signature is valid' : 'The signature is invalid'}</p>
      )}
    </div>
  );
};

export default SignatureValidation;
```