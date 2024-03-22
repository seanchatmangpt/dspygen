import React, { useState, useEffect } from 'react';

interface Props {
  link: string;
  expirationDate: Date;
}

const LinkExpiration: React.FC<Props> = ({ link, expirationDate }) => {
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
        <p>The link is no longer accessible.</p>
      ) : (
        <a href={link}>Link</a>
      )}
    </div>
  );
};

export default LinkExpiration;
```