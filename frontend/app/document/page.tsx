'use client';

import useSWR, { mutate } from 'swr';
import React, { useState } from 'react';
import { Document } from '@/types/document';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function DocumentsPage() {
  const { data: documents, error } = useSWR<Document[]>(
    '/api/document',
    fetcher,
  );
  const [newDocument, setNewDocument] = useState<Partial<Document>>({});
  const [editingDocument, setEditingDocument] =
    useState<Partial<Document> | null>(null);

  const handleDelete = async (id: string) => {
    await fetch(`/api/document?id=${id}`, { method: 'DELETE' });
    await mutate('/api/document'); // Re-fetch documents
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/document', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newDocument),
    });
    setNewDocument({});
    mutate('/api/document'); // Re-fetch documents
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingDocument || !editingDocument.id) return;
    await fetch(`/api/document?id=${editingDocument.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingDocument),
    });
    setEditingDocument(null);
    mutate('/api/document'); // Re-fetch documents
  };

  if (error) return <div>Failed to load</div>;
  if (!documents) return <div>Loading...</div>;

  return (
    <div>
      <h1>Document Details</h1>
      {documents.map((document) => (
        <div key={document.id}>
          
            <p>id: {document.id}</p>
          
            <p>name: {document.name}</p>
          
            <p>type: {document.type}</p>
          
            <p>size: {document.size}</p>
          
            <p>contractId: {document.contractId}</p>
          
          <button onClick={() => setEditingDocument(document)}>Edit</button>
          <button onClick={() => handleDelete(document.id)}>Delete</button>
        </div>
      ))}

      <div>
        {editingDocument ? (
          <form onSubmit={handleUpdate}>
            <h2>Edit Document</h2>
            {/* Similar to the Add Document form, but with existing values and an update button */}

            
            <input
              type="text"
              placeholder="id"
              value={editingDocument.id || ''}
              onChange={(e) =>
                setEditingDocument({
                  ...editingDocument,
                  id: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="name"
              value={editingDocument.name || ''}
              onChange={(e) =>
                setEditingDocument({
                  ...editingDocument,
                  name: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="type"
              value={editingDocument.type || ''}
              onChange={(e) =>
                setEditingDocument({
                  ...editingDocument,
                  type: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="size"
              value={editingDocument.size || ''}
              onChange={(e) =>
                setEditingDocument({
                  ...editingDocument,
                  size: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="contractId"
              value={editingDocument.contractId || ''}
              onChange={(e) =>
                setEditingDocument({
                  ...editingDocument,
                  contractId: e.target.value,
                })
              }
            />
            
            <button type="submit">Update Document</button>
            <button onClick={() => setEditingDocument(null)}>Cancel</button>
          </form>
        ) : (
          <form onSubmit={handleAdd}>
            <h2>Add a New Document</h2>
            
            <input
              type="text"
              placeholder="id"
              value={newDocument.id || ''}
              onChange={(e) =>
                setNewDocument({
                  ...newDocument,
                  id: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="name"
              value={newDocument.name || ''}
              onChange={(e) =>
                setNewDocument({
                  ...newDocument,
                  name: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="type"
              value={newDocument.type || ''}
              onChange={(e) =>
                setNewDocument({
                  ...newDocument,
                  type: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="size"
              value={newDocument.size || ''}
              onChange={(e) =>
                setNewDocument({
                  ...newDocument,
                  size: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="contractId"
              value={newDocument.contractId || ''}
              onChange={(e) =>
                setNewDocument({
                  ...newDocument,
                  contractId: e.target.value,
                })
              }
            />
            
            <button type="submit">Add Document</button>
          </form>
        )}
      </div>
    </div>
  );
}
