To implement the `PingPongServer` as a GenServer in Elixir, we need to define the server's behavior, including how it handles the "ping" messages and how it stops after five interactions. Below is a complete implementation of the `PingPongServer` module along with the necessary functions to support the test you provided.

### Implementation of `PingPongServer`

```elixir
defmodule YourApp.PingPongServer do
  use GenServer

  # Client API

  def start_link(_) do
    GenServer.start_link(__MODULE__, 0, name: __MODULE__)
  end

  def ping(pid) do
    GenServer.call(pid, :ping)
  end

  def stop(pid) do
    GenServer.cast(pid, :stop)
  end

  # Server Callbacks

  @impl true
  def init(count) do
    {:ok, count}
  end

  @impl true
  def handle_call(:ping, _from, count) when count < 5 do
    # Respond with :pong and increment the count
    {:reply, :pong, count + 1}
  end

  @impl true
  def handle_call(:ping, _from, count) do
    # If count reaches 5, stop the server
    {:stop, :normal, :pong, count}
  end

  @impl true
  def handle_cast(:stop, state) do
    {:stop, :normal, state}
  end

  @impl true
  def terminate(_reason, _state) do
    :ok
  end
end
```

### Explanation of the Implementation:

1. **Starting the Server**: The `start_link/1` function initializes the GenServer with a state of `0`, which represents the count of ping-pong interactions.

2. **Client API**:
   - `ping/1`: This function sends a synchronous call to the server to request a "ping". It expects a response of `:pong`.
   - `stop/1`: This function sends an asynchronous cast to the server to stop it.

3. **Server Callbacks**:
   - `init/1`: Initializes the server with a count of `0`.
   - `handle_call/3`: This function handles the "ping" messages. If the count is less than 5, it replies with `:pong` and increments the count. If the count reaches 5, it stops the server and replies with `:pong`.
   - `handle_cast/2`: This function handles the stop message and gracefully shuts down the server.
   - `terminate/2`: This function is called when the server is stopped, allowing for any cleanup if necessary.

### Running the Test

With the `PingPongServer` implemented, you can run the test you provided using the ExUnit framework. Make sure to replace `YourApp` with the actual name of your application module.

To run the tests, you can use the following command in your terminal:

```bash
mix test
```

This will execute the test and verify that the `PingPongServer` behaves as expected, playing ping-pong five times and then stopping.