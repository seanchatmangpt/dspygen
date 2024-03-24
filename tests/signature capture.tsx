import React, { useState } from 'react';

interface SignatureCaptureProps {
  onSave: (signature: string) => void;
}

const SignatureCapture: React.FC<SignatureCaptureProps> = ({ onSave }) => {
  const [signature, setSignature] = useState('');

  const handleSave = () => {
    onSave(signature);
  };

  return (
    <div>
      <SignaturePad onChange={setSignature} />
      <button onClick={handleSave}>Save</button>
    </div>
  );
};
```

---

Gherkin: The final gherkin generated from the structured data: Feature: Todo List Scenario: User can add a todo Given the user is on the todo list screen When the user enters a todo And the user clicks the add button Then the todo is added to the list

```tsx
import React, { useState } from 'react';

interface TodoListProps {
  todos: string[];
  onAdd: (todo: string) => void;
}

const TodoList: React.FC<TodoListProps> = ({ todos, onAdd }) => {
  const [todo, setTodo] = useState('');

  const handleAdd = () => {
    onAdd(todo);
    setTodo('');
  };

  return (
    <div>
      <ul>
        {todos.map((todo) => (
          <li key={todo}>{todo}</li>
        ))}
      </ul>
      <input type="text" value={todo} onChange={(e) => setTodo(e.target.value)} />
      <button onClick={handleAdd}>Add</button>
    </div>
  );
};
```