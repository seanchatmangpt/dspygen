import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Document {
  id: string;
  name: string;
  url: string;
}

const DocumentManagement: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    setLoading(true);
    axios
      .get('/api/documents')
      .then((res) => {
        setDocuments(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const uploadDocument = (file: File) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    axios
      .post('/api/documents', formData)
      .then((res) => {
        setDocuments([...documents, res.data]);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  const downloadDocument = (id: string) => {
    setLoading(true);
    axios
      .get(`/api/documents/${id}`)
      .then((res) => {
        const link = document.createElement('a');
        link.href = res.data.url;
        link.download = res.data.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  const deleteDocument = (id: string) => {
    setLoading(true);
    axios
      .delete(`/api/documents/${id}`)
      .then(() => {
        setDocuments(documents.filter((doc) => doc.id !== id));
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      <input type="file" onChange={(e) => uploadDocument(e.target.files[0])} />
      <ul>
        {documents.map((doc) => (
          <li key={doc.id}>
            <p>{doc.name}</p>
            <button onClick={() => downloadDocument(doc.id)}>Download</button>
            <button onClick={() => deleteDocument(doc.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DocumentManagement;