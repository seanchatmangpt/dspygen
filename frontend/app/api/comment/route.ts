import { Comment } from '@/types/comment';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const url = id
    ? `http://localhost:3333/comments/${id}`
    : 'http://localhost:3333/comments';

  console.log('GET', id);

  const res = await fetch(url);
  // Use the Comment type for the response
  const comment: Comment | Comment[] = await res.json();

  console.log(comment);

  return new Response(JSON.stringify(comment), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST(request: Request): Promise<Response> {
  const commentData = await request.json();

  const res = await fetch('http://localhost:3333/comments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(commentData),
  });

  const newComment: Comment = await res.json();

  console.log(newComment);

  return new Response(JSON.stringify(newComment), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function PUT(request: Request): Promise<Response> {
  const commentData = await request.json();
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(JSON.stringify({ error: 'Comment ID is required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch(`http://localhost:3333/comments/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(commentData),
  });

  const updatedComment: Comment = await res.json();

  console.log(updatedComment);

  return new Response(JSON.stringify(updatedComment), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function DELETE(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(
      JSON.stringify({ error: 'Comment ID is required for deletion' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  await fetch(`http://localhost:3333/comments/${id}`, {
    method: 'DELETE',
  });

  return new Response(
    JSON.stringify({ message: 'Comment deleted successfully' }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  );
}