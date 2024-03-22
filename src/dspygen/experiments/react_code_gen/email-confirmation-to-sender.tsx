import React, { useState, useEffect } from 'react';

interface EmailConfirmationProps {
  sender: string;
  email: string;
}

const EmailConfirmation: React.FC<EmailConfirmationProps> = ({ sender, email }) => {
  const [confirmation, setConfirmation] = useState(false);

  useEffect(() => {
    if (email) {
      setConfirmation(true);
    }
  }, [email]);

  return (
    <div>
      {confirmation ? (
        <p>{`Email successfully delivered to ${sender}.`}</p>
      ) : (
        <p>{`Email failed to deliver to ${sender}.`}</p>
      )}
    </div>
  );
};

export default EmailConfirmation;
```