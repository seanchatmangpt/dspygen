import dspy


def init_dspy(lm_class=dspy.OpenAI, max_tokens: int = 500, model: str = "gpt-3.5-turbo-instruct"):
    lm = lm_class(max_tokens=max_tokens, model=model)
    dspy.settings.configure(lm=lm)
