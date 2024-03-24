import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EmailLinkToSigner = () => {
  const [document, setDocument] = useState(null);
  const [signer, setSigner] = useState(null);
  const [emailSent, setEmailSent] = useState(false);
  const [documentStatus, setDocumentStatus] = useState(null);

  useEffect(() => {
    // fetch document and signer data from API
    axios.get('/api/document')
      .then(res => {
        setDocument(res.data.document);
        setSigner(res.data.signer);
      })
      .catch(err => console.log(err));
  }, []);

  const sendEmail = () => {
    // send email to signer with link to document
    axios.post('/api/email', { documentId: document.id, signerEmail: signer.email })
      .then(res => {
        setEmailSent(true);
      })
      .catch(err => console.log(err));
  };

  const checkEmail = () => {
    // check if signer has received email within 24 hours
    axios.get('/api/email', { params: { signerEmail: signer.email } })
      .then(res => {
        if (res.data.received) {
          // update document status to "Sent"
          axios.put('/api/document', { documentId: document.id, status: 'Sent' })
            .then(res => {
              setDocumentStatus(res.data.status);
            })
            .catch(err => console.log(err));
        }
      })
      .catch(err => console.log(err));
  };

  return (
    <div>
      <h1>Email Link to Signer</h1>
      <p>Document: {document ? document.name : null}</p>
      <p>Signer: {signer ? signer.name : null}</p>
      <button onClick={sendEmail}>Send Email</button>
      {emailSent ? <p>Email sent to {signer.email}</p> : null}
      <button onClick={checkEmail}>Check Email</button>
      {documentStatus ? <p>Document status: {documentStatus}</p> : null}
    </div>
  );
};

export default EmailLinkToSigner;
```

---

Gherkin: The final gherkin generated from the structured data: Feature: User Authentication Scenario: User login Given I have a registered account When I enter my username and password And I click on the "Login" button Then I should be logged in to my account And I should be redirected to the home page

```tsx
import React, { useState } from 'react';
import axios from 'axios';

const UserAuthentication = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleLogin = () => {
    // send username and password to API for authentication
    axios.post('/api/login', { username, password })
      .then(res => {
        setLoggedIn(true);
      })
      .catch(err => console.log(err));
  };

  return (
    <div>
      <h1>User Authentication</h1>
      <label>Username:</label>
      <input type="text" value={username} onChange={handleUsernameChange} />
      <label>Password:</label>
      <input type="password" value={password} onChange={handlePasswordChange} />
      <button onClick={handleLogin}>Login</button>
      {loggedIn ? <p>Logged in as {username}</p> : null}
    </div>
  );
};

export default UserAuthentication;
```