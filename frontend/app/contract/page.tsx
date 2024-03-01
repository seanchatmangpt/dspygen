// pages/contractsPage.tsx
'use client';

import useSWR, { mutate } from 'swr';
import React, { useState } from 'react';
import { Contract } from '@/types/contract';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function ContractsPage() {
  const { data: contracts, error } = useSWR<Contract[]>(
    '/api/contract',
    fetcher,
  );
  const [newContract, setNewContract] = useState<Partial<Contract>>({});
  const [editingContract, setEditingContract] =
    useState<Partial<Contract> | null>(null);

  const handleDelete = async (id: string) => {
    await fetch(`/api/contract?id=${id}`, { method: 'DELETE' });
    await mutate('/api/contract'); // Re-fetch contracts
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/contract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newContract),
    });
    setNewContract({});
    mutate('/api/contract'); // Re-fetch contracts
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingContract || !editingContract.id) return;
    await fetch(`/api/contract?id=${editingContract.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingContract),
    });
    setEditingContract(null);
    mutate('/api/contract'); // Re-fetch contracts
  };

  if (error) return <div>Failed to load</div>;
  if (!contracts) return <div>Loading...</div>;

  return (
    <div>
      <h1>Contract Details</h1>
      {contracts.map((contract) => (
        <div key={contract.id}>
          <p>ID: {contract.id}</p>
          <p>Title: {contract.title}</p>
          <p>Client: {contract.client}</p>
          <p>Status: {contract.status}</p>
          <button onClick={() => setEditingContract(contract)}>Edit</button>
          <button onClick={() => handleDelete(contract.id)}>Delete</button>
        </div>
      ))}

      <div>
        {editingContract ? (
          <form onSubmit={handleUpdate}>
            <h2>Edit Contract</h2>
            {/* Similar to the Add Contract form, but with existing values and an update button */}
            <input
              type="text"
              placeholder="Title"
              value={editingContract.title || ''}
              onChange={(e) =>
                setEditingContract({
                  ...editingContract,
                  title: e.target.value,
                })
              }
            />
            <input
              type="text"
              placeholder="Client"
              value={editingContract.client || ''}
              onChange={(e) =>
                setEditingContract({
                  ...editingContract,
                  client: e.target.value,
                })
              }
            />
            <input
              type="text"
              placeholder="Status"
              value={editingContract.status || ''}
              onChange={(e) =>
                setEditingContract({
                  ...editingContract,
                  status: e.target.value,
                })
              }
            />
            <button type="submit">Update Contract</button>
            <button onClick={() => setEditingContract(null)}>Cancel</button>
          </form>
        ) : (
          <form onSubmit={handleAdd}>
            <h2>Add a New Contract</h2>
            <input
              type="text"
              placeholder="Title"
              value={newContract.title || ''}
              onChange={(e) =>
                setNewContract({ ...newContract, title: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Client"
              value={newContract.client || ''}
              onChange={(e) =>
                setNewContract({ ...newContract, client: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Status"
              value={newContract.status || ''}
              onChange={(e) =>
                setNewContract({ ...newContract, status: e.target.value })
              }
            />
            <button type="submit">Add Contract</button>
          </form>
        )}
      </div>
    </div>
  );
}
