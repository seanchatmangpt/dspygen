---
to: frontend/app/<%= name %>/page.tsx
---
'use client';

import useSWR, { mutate } from 'swr';
import React, { useState } from 'react';
import { <%= Name %> } from '@/types/<%= name %>';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function <%= Name %>sPage() {
  const { data: <%= name %>s, error } = useSWR<<%= Name %>[]>(
    '/api/<%= name %>',
    fetcher,
  );
  const [new<%= Name %>, setNew<%= Name %>] = useState<Partial<<%= Name %>>>({});
  const [editing<%= Name %>, setEditing<%= Name %>] =
    useState<Partial<<%= Name %>> | null>(null);

  const handleDelete = async (id: string) => {
    await fetch(`/api/<%= name %>?id=${id}`, { method: 'DELETE' });
    await mutate('/api/<%= name %>'); // Re-fetch <%= name %>s
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/<%= name %>', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(new<%= Name %>),
    });
    setNew<%= Name %>({});
    mutate('/api/<%= name %>'); // Re-fetch <%= name %>s
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editing<%= Name %> || !editing<%= Name %>.id) return;
    await fetch(`/api/<%= name %>?id=${editing<%= Name %>.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editing<%= Name %>),
    });
    setEditing<%= Name %>(null);
    mutate('/api/<%= name %>'); // Re-fetch <%= name %>s
  };

  if (error) return <div>Failed to load</div>;
  if (!<%= name %>s) return <div>Loading...</div>;

  return (
    <div>
      <h1><%= Name %> Details</h1>
      {<%= name %>s.map((<%= name %>) => (
        <div key={<%= name %>.id}>
          <% params.split(',').forEach(function(param) { %>
            <p><%= param %>: {<%= name %>.<%= param %>}</p>
          <% }); %>
          <button onClick={() => setEditing<%= Name %>(<%= name %>)}>Edit</button>
          <button onClick={() => handleDelete(<%= name %>.id)}>Delete</button>
        </div>
      ))}

      <div>
        {editing<%= Name %> ? (
          <form onSubmit={handleUpdate}>
            <h2>Edit <%= Name %></h2>
            {/* Similar to the Add <%= Name %> form, but with existing values and an update button */}

            <% params.split(',').forEach(function(param) { %>
            <input
              type="text"
              placeholder="<%= param %>"
              value={editing<%= Name %>.<%= param %> || ''}
              onChange={(e) =>
                setEditing<%= Name %>({
                  ...editing<%= Name %>,
                  <%= param %>: e.target.value,
                })
              }
            />
            <% }); %>
            <button type="submit">Update <%= Name %></button>
            <button onClick={() => setEditing<%= Name %>(null)}>Cancel</button>
          </form>
        ) : (
          <form onSubmit={handleAdd}>
            <h2>Add a New <%= Name %></h2>
            <% params.split(',').forEach(function(param) { %>
            <input
              type="text"
              placeholder="<%= param %>"
              value={new<%= Name %>.<%= param %> || ''}
              onChange={(e) =>
                setNew<%= Name %>({
                  ...new<%= Name %>,
                  <%= param %>: e.target.value,
                })
              }
            />
            <% }); %>
            <button type="submit">Add <%= Name %></button>
          </form>
        )}
      </div>
    </div>
  );
}
