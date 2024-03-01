---
to: frontend/app/api/<%= name %>/route.ts
---
import { <%= Name %> } from '@/types/<%= name %>';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const url = id
    ? `http://localhost:3333/<%= name %>s/${id}`
    : 'http://localhost:3333/<%= name %>s';

  console.log('GET', id);

  const res = await fetch(url);
  // Use the <%= Name %> type for the response
  const <%= name %>: <%= Name %> | <%= Name %>[] = await res.json();

  console.log(<%= name %>);

  return new Response(JSON.stringify(<%= name %>), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST(request: Request): Promise<Response> {
  const <%= name %>Data = await request.json();

  const res = await fetch('http://localhost:3333/<%= name %>s', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(<%= name %>Data),
  });

  const new<%= Name %>: <%= Name %> = await res.json();

  console.log(new<%= Name %>);

  return new Response(JSON.stringify(new<%= Name %>), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function PUT(request: Request): Promise<Response> {
  const <%= name %>Data = await request.json();
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(JSON.stringify({ error: '<%= Name %> ID is required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch(`http://localhost:3333/<%= name %>s/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(<%= name %>Data),
  });

  const updated<%= Name %>: <%= Name %> = await res.json();

  console.log(updated<%= Name %>);

  return new Response(JSON.stringify(updated<%= Name %>), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function DELETE(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(
      JSON.stringify({ error: '<%= Name %> ID is required for deletion' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  await fetch(`http://localhost:3333/<%= name %>s/${id}`, {
    method: 'DELETE',
  });

  return new Response(
    JSON.stringify({ message: '<%= Name %> deleted successfully' }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  );
}
}