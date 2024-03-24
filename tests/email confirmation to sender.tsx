import React, { useState, useEffect } from 'react';

interface EmailConfirmationProps {
  sender: string;
  email: string;
}

const EmailConfirmation: React.FC<EmailConfirmationProps> = ({
  sender,
  email,
}) => {
  const [confirmation, setConfirmation] = useState(false);

  useEffect(() => {
    if (email) {
      setConfirmation(true);
    }
  }, [email]);

  return (
    <div>
      <h1>Email Confirmation</h1>
      <p>
        {sender} has sent an email to {email}
      </p>
      {confirmation && <p>You have received a confirmation email</p>}
    </div>
  );
};

export default EmailConfirmation;