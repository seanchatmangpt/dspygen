'use client';

import useSWR, { mutate } from 'swr';
import React, { useState } from 'react';
import { Todo } from '@/types/todo';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function TodosPage() {
  const { data: todos, error } = useSWR<Todo[]>(
    '/api/todo',
    fetcher,
  );
  const [newTodo, setNewTodo] = useState<Partial<Todo>>({});
  const [editingTodo, setEditingTodo] =
    useState<Partial<Todo> | null>(null);

  const handleDelete = async (id: string) => {
    await fetch(`/api/todo?id=${id}`, { method: 'DELETE' });
    await mutate('/api/todo'); // Re-fetch todos
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/todo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTodo),
    });
    setNewTodo({});
    mutate('/api/todo'); // Re-fetch todos
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTodo || !editingTodo.id) return;
    await fetch(`/api/todo?id=${editingTodo.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingTodo),
    });
    setEditingTodo(null);
    mutate('/api/todo'); // Re-fetch todos
  };

  if (error) return <div>Failed to load</div>;
  if (!todos) return <div>Loading...</div>;

  return (
    <div>
      <h1>Todo Details</h1>
      {todos.map((todo) => (
        <div key={todo.id}>
          
            <p>id: {todo.id}</p>
          
            <p>description: {todo.description}</p>
          
            <p>dueDate: {todo.dueDate}</p>
          
          <button onClick={() => setEditingTodo(todo)}>Edit</button>
          <button onClick={() => handleDelete(todo.id)}>Delete</button>
        </div>
      ))}

      <div>
        {editingTodo ? (
          <form onSubmit={handleUpdate}>
            <h2>Edit Todo</h2>
            {/* Similar to the Add Todo form, but with existing values and an update button */}

            
            <input
              type="text"
              placeholder="id"
              value={editingTodo.id || ''}
              onChange={(e) =>
                setEditingTodo({
                  ...editingTodo,
                  id: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="description"
              value={editingTodo.description || ''}
              onChange={(e) =>
                setEditingTodo({
                  ...editingTodo,
                  description: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="dueDate"
              value={editingTodo.dueDate || ''}
              onChange={(e) =>
                setEditingTodo({
                  ...editingTodo,
                  dueDate: e.target.value,
                })
              }
            />
            
            <button type="submit">Update Todo</button>
            <button onClick={() => setEditingTodo(null)}>Cancel</button>
          </form>
        ) : (
          <form onSubmit={handleAdd}>
            <h2>Add a New Todo</h2>
            
            <input
              type="text"
              placeholder="id"
              value={newTodo.id || ''}
              onChange={(e) =>
                setNewTodo({
                  ...newTodo,
                  id: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="description"
              value={newTodo.description || ''}
              onChange={(e) =>
                setNewTodo({
                  ...newTodo,
                  description: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="dueDate"
              value={newTodo.dueDate || ''}
              onChange={(e) =>
                setNewTodo({
                  ...newTodo,
                  dueDate: e.target.value,
                })
              }
            />
            
            <button type="submit">Add Todo</button>
          </form>
        )}
      </div>
    </div>
  );
}
