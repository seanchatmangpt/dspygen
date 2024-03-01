import { Document } from '@/types/document';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const url = id
    ? `http://localhost:3333/documents/${id}`
    : 'http://localhost:3333/documents';

  const res = await fetch(url);

  // Use the Document type for the response
  const document: Document | Document[] = await res.json();

  console.log(document);

  return new Response(JSON.stringify(document), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST(request: Request): Promise<Response> {
  const documentData = await request.json();

  const res = await fetch('http://localhost:3333/documents', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(documentData),
  });

  const newDocument: Document = await res.json();

  console.log(newDocument);

  return new Response(JSON.stringify(newDocument), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function PUT(request: Request): Promise<Response> {
  const documentData = await request.json();
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(JSON.stringify({ error: 'Document ID is required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch(`http://localhost:3333/documents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(documentData),
  });

  const updatedDocument: Document = await res.json();

  console.log(updatedDocument);

  return new Response(JSON.stringify(updatedDocument), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function DELETE(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(
      JSON.stringify({ error: 'Document ID is required for deletion' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  await fetch(`http://localhost:3333/documents/${id}`, {
    method: 'DELETE',
  });

  return new Response(
    JSON.stringify({ message: 'Document deleted successfully' }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  );
}
