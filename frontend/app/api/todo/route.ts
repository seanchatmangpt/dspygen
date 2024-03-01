import { Todo } from '@/types/todo';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const url = id
    ? `http://localhost:3333/todos/${id}`
    : 'http://localhost:3333/todos';

  console.log('GET', id);

  const res = await fetch(url);
  // Use the Todo type for the response
  const todo: Todo | Todo[] = await res.json();

  console.log(todo);

  return new Response(JSON.stringify(todo), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST(request: Request): Promise<Response> {
  const todoData = await request.json();

  const res = await fetch('http://localhost:3333/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(todoData),
  });

  const newTodo: Todo = await res.json();

  console.log(newTodo);

  return new Response(JSON.stringify(newTodo), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function PUT(request: Request): Promise<Response> {
  const todoData = await request.json();
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(JSON.stringify({ error: 'Todo ID is required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch(`http://localhost:3333/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(todoData),
  });

  const updatedTodo: Todo = await res.json();

  console.log(updatedTodo);

  return new Response(JSON.stringify(updatedTodo), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function DELETE(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(
      JSON.stringify({ error: 'Todo ID is required for deletion' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  await fetch(`http://localhost:3333/todos/${id}`, {
    method: 'DELETE',
  });

  return new Response(
    JSON.stringify({ message: 'Todo deleted successfully' }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  );
}