import React, { useState } from 'react';

const SigningLinkGenerator = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [link, setLink] = useState('');
  const [error, setError] = useState('');

  const generateLink = () => {
    if (!name || !email) {
      setError('Please enter a valid name and email');
      return;
    }

    const uniqueLink = `https://signinglink.com/${name}/${email}`;
    setLink(uniqueLink);
    setError('');
  };

  return (
    <div>
      <h1>Signing Link Generator</h1>
      <label>Name:</label>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      <label>Email:</label>
      <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
      <button onClick={generateLink}>Generate Link</button>
      {error && <p>{error}</p>}
      {link && <p>{link}</p>}
    </div>
  );
};
```

---

Gherkin: The final gherkin generated from the structured data: Feature: User Authentication As a user I want to be able to log in and log out So that I can access my account and keep my information secure Scenario: Successfully log in Given I am on the login page When I enter my username and password And click on the "Log In" button Then I am redirected to my account page And I am able to view my personal information Scenario: Incorrect login credentials Given I am on the login page When I enter incorrect username or password And click on the "Log In" button Then an error message is displayed And I am unable to access my account Scenario: Log out of account Given I am logged in to my account When I click on the "Log Out" button Then I am redirected to the login page And I am no longer able to view my personal information

```tsx
import React, { useState } from 'react';

const UserAuthentication = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [error, setError] = useState('');

  const login = () => {
    if (username === 'username' && password === 'password') {
      setLoggedIn(true);
      setError('');
    } else {
      setError('Incorrect username or password');
    }
  };

  const logout = () => {
    setLoggedIn(false);
  };

  return (
    <div>
      {!loggedIn ? (
        <div>
          <h1>Login</h1>
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button onClick={login}>Log In</button>
          {error && <p>{error}</p>}
        </div>
      ) : (
        <div>
          <h1>Account Page</h1>
          <p>Welcome, {username}!</p>
          <button onClick={logout}>Log Out</button>
        </div>
      )}
    </div>
  );
};
```