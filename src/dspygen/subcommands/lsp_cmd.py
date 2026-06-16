"""LSP server subcommand for dspygen CLI."""
import typer

app = typer.Typer(help="Run dspygen Language Server")

@app.command("serve")
def serve_lsp(
    transport: str = typer.Option("stdio", help="Transport: stdio or tcp"),
    host: str = typer.Option("127.0.0.1", help="TCP host"),
    port: int = typer.Option(2087, help="TCP port"),
):
    """Start the dspygen LSP server."""
    from dspygen.lsp.server import run_stdio, run_tcp
    if transport == "stdio":
        run_stdio()
    else:
        run_tcp(host=host, port=port)
