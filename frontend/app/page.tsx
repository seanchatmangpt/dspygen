'use client';
import Editor from '@monaco-editor/react';
import { useEffect, useState } from 'react';
import { LiveProvider, LiveError, LivePreview } from 'react-live';

function CodeEditor({ code, onChange }) {
  return (
    <Editor
      height="300px" // Adjust as needed
      width="50%"
      defaultLanguage="javascript"
      defaultValue="// Write your component code here"
      value={code}
      onChange={onChange}
      theme="vs-dark"
    />
  );
}

export default function Page() {
  const [code, setCode] = useState('<div>Hello World</div>');
  const [error, setError] = useState('');
  const [data, setData] = useState('<div>Loading...</div>');
  const [story, setStory] = useState(''); // New state for form input

  // Update fetchCode to use story state
  useEffect(() => {
    const fetchCode = async () => {
      try {
        const response = await fetch('http://127.0.0.1:888/jsx/', {
          // Ensure this URL is correct and accessible
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            story: `${story} return only the html tags. NO TYPESCRIPT!!!`, // Use state value
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setCode(data.code || data); // Adjust depending on response structure
        setData(data.code || data); // Adjust depending on response structure
      } catch (err) {
        setError(err.message);
        console.error('Fetching error:', err);
      }
    };

    if (story) {
      fetchCode();
    }
  }, [story]); // Depend on story state

  return (
    <main className="flex min-h-screen flex-col p-6">
      <form
        onSubmit={(e) => {
          e.preventDefault(); // Prevent actual form submission
          setStory(e.target.elements.story.value); // Update story state, triggering useEffect
        }}
      >
        <input
          type="text"
          name="story"
          defaultValue={story}
          className="input input-bordered w-full max-w-xs"
        />
        <button type="submit" className="btn btn-primary">
          Update Story
        </button>
      </form>
      <div className="mt-4 flex flex-1">
        <div className="flex-1">
          <CodeEditor code={code} onChange={(newCode) => setData(newCode)} />
        </div>
        <div className="flex-1">
          <LiveProvider code={data}>
            <LiveError />
            <LivePreview className="rounded-lg border border-gray-200 p-4 shadow" />
          </LiveProvider>
        </div>
      </div>
    </main>
  );
}
