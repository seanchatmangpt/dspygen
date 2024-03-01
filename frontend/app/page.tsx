'use client';
import Editor from '@monaco-editor/react';
import { useEffect, useState } from 'react';
import { LiveProvider, LiveError, LivePreview } from 'react-live';
import 'regenerator-runtime/runtime';

import SpeechRecognition, {
  useSpeechRecognition,
} from 'react-speech-recognition';

function CodeEditor({ code, onChange }) {
  return (
    <Editor
      height="50vh" // Adjust as needed
      width="50vh"
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

  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

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
            story,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setCode(data.code || data); // Adjust depending on response structure
        setData(data.code || data); // Adjust depending on response structure
      } catch (err) {
        // @ts-ignore
        setError(err.message);
        console.error('Fetching error:', err);
      }
    };

    if (story) {
      fetchCode();
    }
  }, [story]); // Depend on story state

  useEffect(() => {
    setStory(transcript);
  }, [transcript]);

  return (
    <main className="flex min-h-screen flex-row p-6">
      <p className="mb-4">Microphone: {listening ? 'on' : 'off'}</p>
      <button
        className="mr-4 rounded-lg bg-blue-500 px-4 py-2 text-white shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        onClick={SpeechRecognition.startListening}
      >
        Start
      </button>
      <button
        className="rounded-lg bg-red-500 px-4 py-2 text-white shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
        onClick={SpeechRecognition.stopListening}
      >
        Stop
      </button>
      <button
        className="rounded-lg bg-gray-300 px-4 py-2 text-gray-700 shadow-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-opacity-50"
        onClick={resetTranscript}
      >
        Reset
      </button>
      <button className="rounded-lg bg-green-500 px-4 py-2 text-white shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
        Send Transcript
      </button>
      <p className="mt-4">{transcript}</p>
      <form
        onSubmit={(e) => {
          e.preventDefault(); // Prevent actual form submission
          // @ts-ignore
          setStory(e.target.elements.story.value); // Update story state, triggering useEffect
        }}
      >
        <input
          type="text"
          name="story"
          defaultValue={story}
          value={story}
          className="input input-bordered w-full max-w-xs"
        />
        <button type="submit" className="btn btn-primary">
          Update Story
        </button>
      </form>
      <div className="flex-1">
        <CodeEditor code={code} onChange={(newCode) => setData(newCode)} />
      </div>
      <div className="flex-1">
        <LiveProvider code={data}>
          <LiveError />
          <LivePreview className="rounded-lg border border-gray-200 p-4 shadow" />
        </LiveProvider>
      </div>
    </main>
  );
}
