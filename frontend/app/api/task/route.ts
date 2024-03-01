import { Task } from '@/types/task';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const url = id
    ? `http://localhost:3333/task/${id}`
    : 'http://localhost:3333/task';

  const res = await fetch(url);
  // Use the Task type for the response

  const task: Task | Task[] = await res.json();

  console.log(task);

  return new Response(JSON.stringify(task), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST(request: Request): Promise<Response> {
  const taskData = await request.json();

  const res = await fetch('http://localhost:3333/task', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData),
  });

  const newTask: Task = await res.json();

  console.log(newTask);

  return new Response(JSON.stringify(newTask), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function PUT(request: Request): Promise<Response> {
  const taskData = await request.json();
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(JSON.stringify({ error: 'Task ID is required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch(`http://localhost:3333/task/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData),
  });

  const updatedTask: Task = await res.json();

  console.log(updatedTask);

  return new Response(JSON.stringify(updatedTask), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function DELETE(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(
      JSON.stringify({ error: 'Task ID is required for deletion' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  await fetch(`http://localhost:3333/task/${id}`, {
    method: 'DELETE',
  });

  return new Response(
    JSON.stringify({ message: 'Task deleted successfully' }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  );
}
