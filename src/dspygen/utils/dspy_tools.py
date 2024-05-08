import dspy


def init_dspy(lm_class=dspy.OpenAI, max_tokens: int = 800, model: str = "gpt-3.5-turbo-instruct", lm_instance=None):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance)
        return lm_instance
    else:
        lm = lm_class( max_tokens=max_tokens, model=model)
        dspy.settings.configure(lm=lm)
        return lm


def init_ol(lm_class=dspy.OllamaLocal, model: str = "phi3:instruct", max_tokens: int = 800, lm_instance=None):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance)
        return lm_instance
    else:
        lm = lm_class(model=model, max_tokens=max_tokens)
        dspy.settings.configure(lm=lm)
        return lm
