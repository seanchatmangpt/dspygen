"""MCP server subcommand for dspygen CLI."""
import typer

app = typer.Typer(help="Run dspygen MCP server")

@app.command("serve")
def serve_mcp(
    transport: str = typer.Option("stdio", help="Transport: stdio or sse"),
    host: str = typer.Option("127.0.0.1", help="SSE host"),
    port: int = typer.Option(8765, help="SSE port"),
):
    """Start the dspygen MCP server."""
    if transport == "stdio":
        from dspygen.mcp.server import run_stdio
        run_stdio()
    else:
        import uvicorn

        from dspygen.mcp.server import create_sse_app
        uvicorn.run(create_sse_app(), host=host, port=port)
