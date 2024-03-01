'use client';

import useSWR from 'swr';
import React from 'react';

// @ts-ignore
const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function Page({ params }: { params: { id: string } }) {
  const { data, error, isLoading } = useSWR(
    `/api/task?id=${params.id}`,
    fetcher,
  );

  if (error) return <div>failed to load</div>;
  if (isLoading) return <div>loading...</div>;

  console.log('data', data);

  return (
    <div>
      <h1>Task Details</h1>
         
            <p>id: {data.id}</p>
          
            <p>description: {data.description}</p>
          
            <p>dueDate: {data.dueDate}</p>
          
    </div>
  );
}
