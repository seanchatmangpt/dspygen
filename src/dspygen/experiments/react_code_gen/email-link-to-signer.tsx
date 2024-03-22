import React, { useState, useEffect } from 'react';

const EmailLinkToSigner = () => {
  const [document, setDocument] = useState(null);
  const [signer, setSigner] = useState(null);
  const [emailSent, setEmailSent] = useState(false);
  const [documentStatus, setDocumentStatus] = useState(null);

  useEffect(() => {
    // fetch document data
    // fetch signer data
  }, []);

  const handleSendEmail = () => {
    // send email to signer with link to document
    setEmailSent(true);
  };

  const handleDocumentAccess = () => {
    // update document status to "Sent"
    setDocumentStatus("Sent");
  };

  return (
    <div>
      <button onClick={handleSendEmail}>Send Email</button>
      {emailSent && (
        <div>
          <p>An email has been sent to {signer.name} with a link to the document.</p>
          <p>The signer should receive the email within 24 hours.</p>
          <p>The signer can access the document by clicking on the link in the email.</p>
          <button onClick={handleDocumentAccess}>Access Document</button>
        </div>
      )}
      {documentStatus === "Sent" && <p>The document status has been updated to "Sent".</p>}
    </div>
  );
};

export default EmailLinkToSigner;
```