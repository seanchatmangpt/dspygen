import React, { useState } from 'react';

interface Props {
  onSave: (signature: string) => void;
}

const Signature: React.FC<Props> = ({ onSave }) => {
  const [signature, setSignature] = useState('');

  const handleSave = () => {
    onSave(signature);
  };

  return (
    <div>
      <h1>Signature</h1>
      <input
        type="text"
        value={signature}
        onChange={(e) => setSignature(e.target.value)}
      />
      <button onClick={handleSave}>Save</button>
    </div>
  );
};

export default Signature;
```

---

Gherkin: The final gherkin generated from the structured data: Feature: Login Scenario: User logs in Given the user is on the login page When the user enters their username and password And clicks on the login button Then the user is logged in successfully

```tsx
import React, { useState } from 'react';

interface Props {
  onLogin: (username: string, password: string) => void;
}

const Login: React.FC<Props> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    onLogin(username, password);
  };

  return (
    <div>
      <h1>Login</h1>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Login;