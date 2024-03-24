import React, { useState, useEffect } from 'react';

interface Props {
  expirationDate: Date;
  link: string;
}

const LinkExpiration: React.FC<Props> = ({ expirationDate, link }) => {
  const [isExpired, setIsExpired] = useState(false);

  useEffect(() => {
    const currentDate = new Date();
    if (currentDate > expirationDate) {
      setIsExpired(true);
    }
  }, [expirationDate]);

  return (
    <div>
      {isExpired ? (
        <p>The link has expired</p>
      ) : (
        <a href={link} target="_blank" rel="noopener noreferrer">
          {link}
        </a>
      )}
    </div>
  );
};

export default LinkExpiration;
```