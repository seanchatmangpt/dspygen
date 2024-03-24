import React, { useState, useEffect } from 'react';
import { Document } from './Document';

export const DocumentManagement = () => {
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    // fetch documents from API
    // setDocuments(response.data);
  }, []);

  const handleUpload = (file: File) => {
    // upload file to API
    // setDocuments([...documents, response.data]);
  };

  const handleDownload = (document: Document) => {
    // download file from API
    // saveAs(response.data);
  };

  const handleDelete = (document: Document) => {
    // delete file from API
    // setDocuments(documents.filter((doc) => doc.id !== document.id));
  };

  return (
    <div>
      <h1>Document Management</h1>
      <button onClick={() => handleUpload(file)}>Upload Document</button>
      <ul>
        {documents.map((document) => (
          <li key={document.id}>
            <p>{document.name}</p>
            <button onClick={() => handleDownload(document)}>Download</button>
            <button onClick={() => handleDelete(document)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};
```

---

Gherkin: The final gherkin generated from the structured data: Feature: API for User Management Scenario: Admin can create a user Given the admin is logged in When the admin creates a user Then the user is successfully created Scenario: Admin can update a user Given the admin is logged in When the admin updates a user Then the user is successfully updated Scenario: Admin can delete a user Given the admin is logged in When the admin deletes a user Then the user is successfully deleted

```tsx
import React, { useState, useEffect } from 'react';
import { User } from './User';

export const UserManagement = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    // fetch users from API
    // setUsers(response.data);
  }, []);

  const handleCreate = (user: User) => {
    // create user in API
    // setUsers([...users, response.data]);
  };

  const handleUpdate = (user: User) => {
    // update user in API
    // setUsers(users.map((u) => (u.id === user.id ? response.data : u)));
  };

  const handleDelete = (user: User) => {
    // delete user from API
    // setUsers(users.filter((u) => u.id !== user.id));
  };

  return (
    <div>
      <h1>User Management</h1>
      <button onClick={() => handleCreate(user)}>Create User</button>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <p>{user.name}</p>
            <button onClick={() => handleUpdate(user)}>Update</button>
            <button onClick={() => handleDelete(user)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};
```