import { Contract } from '@/types/contract';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const url = id
    ? `http://localhost:3333/contracts/${id}`
    : 'http://localhost:3333/contracts';

  console.log('GET', id);

  const res = await fetch(url);
  // Use the Contract type for the response
  const contract: Contract | Contract[] = await res.json();

  console.log(contract);

  return new Response(JSON.stringify(contract), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST(request: Request): Promise<Response> {
  const contractData = await request.json();

  const res = await fetch('http://localhost:3333/contracts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contractData),
  });

  const newContract: Contract = await res.json();

  console.log(newContract);

  return new Response(JSON.stringify(newContract), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function PUT(request: Request): Promise<Response> {
  const contractData = await request.json();
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(JSON.stringify({ error: 'Contract ID is required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch(`http://localhost:3333/contracts/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contractData),
  });

  const updatedContract: Contract = await res.json();

  console.log(updatedContract);

  return new Response(JSON.stringify(updatedContract), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function DELETE(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response(
      JSON.stringify({ error: 'Contract ID is required for deletion' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  await fetch(`http://localhost:3333/contracts/${id}`, {
    method: 'DELETE',
  });

  return new Response(
    JSON.stringify({ message: 'Contract deleted successfully' }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  );
}
