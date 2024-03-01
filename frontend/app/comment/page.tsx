'use client';

import useSWR, { mutate } from 'swr';
import React, { useState } from 'react';
import { Comment } from '@/types/comment';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function CommentsPage() {
  const { data: comments, error } = useSWR<Comment[]>('/api/comment', fetcher);
  const [newComment, setNewComment] = useState<Partial<Comment>>({});
  const [editingComment, setEditingComment] = useState<Partial<Comment> | null>(
    null,
  );

  const handleDelete = async (id: string) => {
    await fetch(`/api/comment?id=${id}`, { method: 'DELETE' });
    await mutate('/api/comment'); // Re-fetch comments
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/comment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newComment),
    });
    setNewComment({});
    mutate('/api/comment'); // Re-fetch comments
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingComment || !editingComment.id) return;
    await fetch(`/api/comment?id=${editingComment.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingComment),
    });
    setEditingComment(null);
    mutate('/api/comment'); // Re-fetch comments
  };

  if (error) return <div>Failed to load</div>;
  if (!comments) return <div>Loading...</div>;

  return (
    <div>
      <h1>Comment Details</h1>
      {comments.map((comment) => (
        <div key={comment.id}>
          <p>ID: {comment.id}</p>
          <p>Text: {comment.text}</p>
          <p>ContractId: {comment.contractId}</p>
          <button onClick={() => setEditingComment(comment)}>Edit</button>
          <button onClick={() => handleDelete(comment.id)}>Delete</button>
        </div>
      ))}

      <div>
        {editingComment ? (
          <form onSubmit={handleUpdate}>
            <h2>Edit Comment</h2>
            {/* Similar to the Add Comment form, but with existing values and an update button */}
            <input
              type="text"
              placeholder="Text"
              value={editingComment.text || ''}
              onChange={(e) =>
                setEditingComment({
                  ...editingComment,
                  text: e.target.value,
                })
              }
            />
            <input
              type="text"
              placeholder="ContractId"
              value={editingComment.contractId || ''}
              onChange={(e) =>
                setEditingComment({
                  ...editingComment,
                  contractId: e.target.value,
                })
              }
            />
            <button type="submit">Update Comment</button>
            <button onClick={() => setEditingComment(null)}>Cancel</button>
          </form>
        ) : (
          <form onSubmit={handleAdd}>
            <h2>Add a New Comment</h2>
            <input
              type="text"
              placeholder="Text"
              value={newComment.text || ''}
              onChange={(e) =>
                setNewComment({ ...newComment, text: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="ContractId"
              value={newComment.contractId || ''}
              onChange={(e) =>
                setNewComment({ ...newComment, contractId: e.target.value })
              }
            />
            <button type="submit">Add Comment</button>
          </form>
        )}
      </div>
    </div>
  );
}
