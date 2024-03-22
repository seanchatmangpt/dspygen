import React, { useState } from 'react';

interface SignaturePlacementProps {
  document: Document;
}

const SignaturePlacement: React.FC<SignaturePlacementProps> = ({ document }) => {
  const [signature, setSignature] = useState<Signature | null>(null);

  const handleSignatureFieldClick = (event: React.MouseEvent<HTMLDivElement>) => {
    const signatureField = event.currentTarget;
    const signature = document.getSignature(signatureField.id);
    setSignature(signature);
  };

  return (
    <div>
      <Document document={document} />
      <SignatureField onClick={handleSignatureFieldClick} />
      {signature && <SignaturePreview signature={signature} />}
    </div>
  );
};

export default SignaturePlacement;
```