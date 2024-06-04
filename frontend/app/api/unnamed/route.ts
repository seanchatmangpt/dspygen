import { Unnamed } from '@/types/unnamed';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const url = id
    ? `http://localhost:3333/unnameds/${id}`
    : 'http://localhost:3333/unnameds';

  console.log('GET', id);

  const res = await fetch(url);
  // Use the Unnamed type for the response
  const unnamed: Unnamed | Unnamed[] = await res.json();

  console.log(unnamed);

  return new Response(JSON.stringify(unnamed), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST(request: Request): Promise<Response> {
  const unnamedData = await request.json();

  const res = await fetch('http://localhost:3333/unnameds', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(unnamedData),
  });

  const newUnnamed: Unnamed = await res.json();

  console.log(newUnnamed);

  return new Response(JSON.stringify(newUnnamed), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function PUT(request: Request): Promise<Response> {
  const unnamedData = await request.json();
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(JSON.stringify({ error: 'Unnamed ID is required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch(`http://localhost:3333/unnameds/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(unnamedData),
  });

  const updatedUnnamed: Unnamed = await res.json();

  console.log(updatedUnnamed);

  return new Response(JSON.stringify(updatedUnnamed), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function DELETE(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(
      JSON.stringify({ error: 'Unnamed ID is required for deletion' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  await fetch(`http://localhost:3333/unnameds/${id}`, {
    method: 'DELETE',
  });

  return new Response(
    JSON.stringify({ message: 'Unnamed deleted successfully' }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  );
}
}