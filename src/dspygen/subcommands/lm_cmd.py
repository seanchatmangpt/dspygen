"""lm"""
import typer


app = typer.Typer(help="Generate Language Models")


lm_template = """
class GPT3(LM):
    def __init__(
        self,
        model: str = "",
        api_key: Optional[str] = None,
        api_provider: str,
        api_base: Optional[str] = None,
        model_type: Literal["chat", "text"] = None,
        **kwargs,
    ):
        super().__init__(model)
        self.provider = api_provider

        default_model_type = (
            "chat"
            else "text"
        )
        self.model_type = model_type if model_type else default_model_type

        if api_key:
            openai.api_key = api_key

        if api_base:
            if OPENAI_LEGACY:
                openai.api_base = api_base
            else:       
                openai.base_url = api_base

        self.kwargs = {
            "temperature": 0.0,
            "max_tokens": 150,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "n": 1,
            **kwargs,
        }  # TODO: add kwargs above for </s>

        if api_provider != "azure":
            self.kwargs["model"] = model
        self.history: list[dict[str, Any]] = [
"""


@app.command(name="new")
def new_lm():
    """Generates a new language model."""
    typer.echo("Uses jinja and dspy module to create a language model.")
    