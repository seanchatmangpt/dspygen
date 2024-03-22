import React, { useState, useEffect } from 'react';

interface Props {
  name: string;
  email: string;
}

const SigningLinkGenerator: React.FC<Props> = ({ name, email }) => {
  const [link, setLink] = useState<string>('');
  const [error, setError] = useState<string>('');

  const generateLink = () => {
    if (!name || !email) {
      setError('Please enter a valid name and email');
      return;
    }

    const link = `https://signinglink.com/${name}/${email}`;
    setLink(link);
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setLink('');
    }, 86400000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
      <button onClick={generateLink}>Generate Link</button>
      {error && <p>{error}</p>}
      {link && <a href={link}>Click here to sign</a>}
    </div>
  );
};

export default SigningLinkGenerator;
```