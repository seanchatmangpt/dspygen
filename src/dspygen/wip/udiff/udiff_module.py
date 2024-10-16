import dspy
from dspy import InputField, OutputField

elixir_example = dspy.Example(
    source_code="""1: defmodule DataProcessor do
2:   def process(data) do
3:     data
4:     |> Enum.map(&transform/1)
5:     |> Enum.filter(&filter/1)
6:     |> Enum.reduce(%{}, &aggregate/2)
7:   end
8:
9:   defp transform(%{value: value} = item) do
10:    %{item | value: value * 2}
11:  end
12:
13:  defp filter(%{value: value}) do
14:    rem(value, 3) == 0
15:  end
16:
17:  defp aggregate(item, acc) do
18:    Map.update(acc, item.category, [item], &[item | &1])
19:  end
20: end""",
    edit_instructions="Modify the `process` function to perform the `filter` operation before the `transform` to improve efficiency.",
    hunk_header="@@ -3,5 +3,5 @@",
    changed_lines="""```diff
3:     data
-4:     |> Enum.map(&transform/1)
-5:     |> Enum.filter(&filter/1)
+4:     |> Enum.filter(&filter/1)
+5:     |> Enum.map(&transform/1)
6:     |> Enum.reduce(%{}, &aggregate/2)
```"""
).with_inputs("source_code", "edit_instructions")

typescript_example = dspy.Example(
    source_code="""1: class Graph {
2:     private adjacencyList: Map<string, string[]> = new Map();
3:
4:     addVertex(vertex: string): void {
5:         if (!this.adjacencyList.has(vertex)) {
6:             this.adjacencyList.set(vertex, []);
7:         }
8:     }
9:
10:    addEdge(v1: string, v2: string): void {
11:        this.adjacencyList.get(v1)?.push(v2);
12:        this.adjacencyList.get(v2)?.push(v1);
13:    }
14:
15:    removeVertex(vertex: string): void {
16:        this.adjacencyList.get(vertex)?.forEach(adjacentVertex => {
17:            this.removeEdge(vertex, adjacentVertex);
18:        });
19:        this.adjacencyList.delete(vertex);
20:    }
21:
22:    removeEdge(v1: string, v2: string): void {
23:        this.adjacencyList.set(v1, this.adjacencyList.get(v1)?.filter(v => v !== v2) || []);
24:        this.adjacencyList.set(v2, this.adjacencyList.get(v2)?.filter(v => v !== v1) || []);
25:    }
26:
27:    depthFirstTraversal(start: string): void {
28:        const stack = [start];
29:        const visited = new Set<string>();
30:
31:        while (stack.length > 0) {
32:            const vertex = stack.pop();
33:            if (vertex && !visited.has(vertex)) {
34:                console.log(vertex);
35:                visited.add(vertex);
36:                stack.push(...(this.adjacencyList.get(vertex) || []));
37:            }
38:        }
39:    }
40: }""",
    edit_instructions="Optimize the `depthFirstTraversal` method to avoid revisiting vertices by ensuring adjacent vertices are added to the stack only if they haven't been visited yet.",
    hunk_header="@@ -35,2 +35,3 @@",
    changed_lines="""```diff
35:                visited.add(vertex);
-36:                stack.push(...(this.adjacencyList.get(vertex) || []));
+36:                const neighbors = this.adjacencyList.get(vertex) || [];
+37:                stack.push(...neighbors.filter(v => !visited.has(v)));
```"""
).with_inputs("source_code", "edit_instructions")

python_example = dspy.Example(
    source_code="""1: import threading
2: import time
3:
4: class ResourcePool:
5:     def __init__(self, max_resources):
6:         self.max_resources = max_resources
7:         self.available_resources = max_resources
8:         self.lock = threading.Lock()
9:
10:    def acquire(self):
11:        with self.lock:
12:            while self.available_resources <= 0:
13:                self.lock.wait()
14:            self.available_resources -= 1
15:
16:    def release(self):
17:        with self.lock:
18:            self.available_resources += 1
19:            self.lock.notify()
20:
21: def worker(pool, worker_id):
22:     print(f"Worker {worker_id} attempting to acquire resource")
23:     pool.acquire()
24:     print(f"Worker {worker_id} acquired resource")
25:     time.sleep(1)  # Simulate work
26:     pool.release()
27:     print(f"Worker {worker_id} released resource")
28:
29: if __name__ == "__main__":
30:     pool = ResourcePool(3)
31:     threads = []
32:     for i in range(5):
33:         t = threading.Thread(target=worker, args=(pool, i))
34:         threads.append(t)
35:         t.start()
36:     for t in threads:
37:         t.join()""",
    edit_instructions="Fix the synchronization issue in the `acquire` and `release` methods by replacing `self.lock.wait()` and `self.lock.notify()` with appropriate condition variables.",
    hunk_header="@@ -10,10 +10,12 @@",
    changed_lines="""```diff
10:    def acquire(self):
11:        with self.lock:
12:            while self.available_resources <= 0:
-13:                self.lock.wait()
+13:                self.condition.wait()
14:            self.available_resources -= 1
15:
16:    def release(self):
17:        with self.lock:
18:            self.available_resources += 1
-19:            self.lock.notify()
+19:            self.condition.notify_all()
```"""
).with_inputs("source_code", "edit_instructions")


class UDiffChangeGenerator(dspy.Signature):
    """
    Generates the diff content (hunk_content) between the hunk lines for a unified diff (UDiff)
    based on the given source code, and edit instructions.
    """
    source_code = InputField(
        desc="The original source code to be edited."
    )
    edit_instructions = InputField(
        desc="The instructions describing the changes to be made to the source code."
    )
    hunk_header = OutputField(
        desc="The hunk header indicating the lines to be changed.",
        prefix="@@ -"
    )
    changed_lines = OutputField(
        desc="The changed lines with the same amount of changes as the line numbers."
    )


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol, init_dspy
    # init_ol()

    from dspy import ChainOfThought

    # Assuming UDiffChangeGenerator is defined as per your initial code

    # Initialize DSPy (if needed)
    init_dspy()

    # Use the ChainOfThought to process the example
    result = dspy.Predict(UDiffChangeGenerator).forward(
        source_code=python_example.source_code,
        edit_instructions=python_example.edit_instructions
    )

    # Output the results
    print("Hunk Header:", result.hunk_header)
    print("Changed Lines:", result.changed_lines)


if __name__ == '__main__':
    main()

