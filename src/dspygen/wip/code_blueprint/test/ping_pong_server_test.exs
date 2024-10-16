To create a test for a `PingPongServer` implemented as a GenServer in Elixir, we need to ensure that the server can handle a ping-pong interaction five times and then stop. Below is an example of how you might write such a test using Elixir's built-in testing framework, ExUnit.

Assuming you have a `PingPongServer` module that implements the GenServer behavior, here’s how you could structure your test:

```elixir
defmodule PingPongServerTest do
  use ExUnit.Case
  alias YourApp.PingPongServer

  setup do
    # Start the PingPongServer before each test
    {:ok, pid} = PingPongServer.start_link()
    {:ok, server_pid: pid}
  end

  test "plays ping-pong five times and stops", %{server_pid: server_pid} do
    # Send "ping" to the server and expect "pong" back
    for _ <- 1..5 do
      assert PingPongServer.ping(server_pid) == :pong
    end

    # Stop the server after the interactions
    PingPongServer.stop(server_pid)

    # Optionally, you can check if the server is stopped
    assert Process.alive?(server_pid) == false
  end
end
```

### Explanation:

1. **Setup Block**: The `setup` block starts the `PingPongServer` before each test. The PID of the server is passed to the test as part of the context.

2. **Test Block**: The test itself runs a loop five times, sending a "ping" message to the server and asserting that the response is "pong".

3. **Stopping the Server**: After the ping-pong interactions, the server is stopped using a hypothetical `stop/1` function in the `PingPongServer`. You might need to implement this function if it doesn't exist.

4. **Process Check**: Optionally, you can assert that the server process is no longer alive after stopping it.

### Assumptions:
- The `PingPongServer` has a `ping/1` function that sends a "ping" message and expects a "pong" response.
- The `PingPongServer` has a `stop/1` function to gracefully shut down the server.
- The module `YourApp.PingPong