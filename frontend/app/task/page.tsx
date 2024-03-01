'use client';

import useSWR, { mutate } from 'swr';
import React, { useState } from 'react';
import { Task } from '@/types/task';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function TasksPage() {
  const { data: tasks, error } = useSWR<Task[]>(
    '/api/task',
    fetcher,
  );
  const [newTask, setNewTask] = useState<Partial<Task>>({});
  const [editingTask, setEditingTask] =
    useState<Partial<Task> | null>(null);

  const handleDelete = async (id: string) => {
    await fetch(`/api/task?id=${id}`, { method: 'DELETE' });
    await mutate('/api/task'); // Re-fetch tasks
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/task', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTask),
    });
    setNewTask({});
    mutate('/api/task'); // Re-fetch tasks
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask || !editingTask.id) return;
    await fetch(`/api/task?id=${editingTask.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingTask),
    });
    setEditingTask(null);
    mutate('/api/task'); // Re-fetch tasks
  };

  if (error) return <div>Failed to load</div>;
  if (!tasks) return <div>Loading...</div>;

  return (
    <div>
      <h1>Task Details</h1>
      {tasks.map((task) => (
        <div key={task.id}>
          
            <p>id: {task.id}</p>
          
            <p>description: {task.description}</p>
          
            <p>dueDate: {task.dueDate}</p>
          
          <button onClick={() => setEditingTask(task)}>Edit</button>
          <button onClick={() => handleDelete(task.id)}>Delete</button>
        </div>
      ))}

      <div>
        {editingTask ? (
          <form onSubmit={handleUpdate}>
            <h2>Edit Task</h2>
            {/* Similar to the Add Task form, but with existing values and an update button */}

            
            <input
              type="text"
              placeholder="id"
              value={editingTask.id || ''}
              onChange={(e) =>
                setEditingTask({
                  ...editingTask,
                  id: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="description"
              value={editingTask.description || ''}
              onChange={(e) =>
                setEditingTask({
                  ...editingTask,
                  description: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="dueDate"
              value={editingTask.dueDate || ''}
              onChange={(e) =>
                setEditingTask({
                  ...editingTask,
                  dueDate: e.target.value,
                })
              }
            />
            
            <button type="submit">Update Task</button>
            <button onClick={() => setEditingTask(null)}>Cancel</button>
          </form>
        ) : (
          <form onSubmit={handleAdd}>
            <h2>Add a New Task</h2>
            
            <input
              type="text"
              placeholder="id"
              value={newTask.id || ''}
              onChange={(e) =>
                setNewTask({
                  ...newTask,
                  id: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="description"
              value={newTask.description || ''}
              onChange={(e) =>
                setNewTask({
                  ...newTask,
                  description: e.target.value,
                })
              }
            />
            
            <input
              type="text"
              placeholder="dueDate"
              value={newTask.dueDate || ''}
              onChange={(e) =>
                setNewTask({
                  ...newTask,
                  dueDate: e.target.value,
                })
              }
            />
            
            <button type="submit">Add Task</button>
          </form>
        )}
      </div>
    </div>
  );
}
