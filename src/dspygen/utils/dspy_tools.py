import dspy


def init_dspy(model: str = "gpt-3.5-turbo-instruct", lm_class=dspy.OpenAI, max_tokens: int = 800, lm_instance=None, api_key=None, temperature=0.6):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance)
        return lm_instance
    else:
        lm = lm_class(max_tokens=max_tokens, model=model, api_key=api_key, temperature=temperature)
        dspy.settings.configure(lm=lm)
        return lm


def init_ol(model: str = "qwen2:7b-instruct", base_url="http://localhost:11434", max_tokens: int = 800, lm_instance=None, lm_class=dspy.OllamaLocal, timeout=100, temperature=0.6):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance)
        return lm_instance
    else:
        lm = lm_class(model=model, base_url=base_url, max_tokens=max_tokens, timeout_s=timeout, temperature=temperature)
        dspy.settings.configure(lm=lm)
        return lm
