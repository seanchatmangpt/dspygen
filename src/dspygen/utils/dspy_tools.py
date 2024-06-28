import dspy


class OpenAIModels:
    gpt3 = ""


def init_dspy(model: str = "gpt-3.5-turbo-instruct", lm_class=dspy.OpenAI, max_tokens: int = 800, lm_instance=None, api_key=None):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance)
        return lm_instance
    else:
        lm = lm_class(max_tokens=max_tokens, model=model, api_key=api_key)
        dspy.settings.configure(lm=lm)
        return lm


class OllamaModels:
    phi = "phi3:instruct"
    qwen = "qwen2:7b-instruct"
    deepseek = "deepseek-coder-v2"
    llama = "llama3"
    mixtral = "mixtral:8x22b"


def init_ol(model: str = OllamaModels.qwen, base_url="http://0.0.0.0:11434", max_tokens: int = 800, lm_instance=None, lm_class=dspy.OllamaLocal, timeout=10):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance)
        return lm_instance
    else:
        lm = lm_class(model=model, base_url=base_url, max_tokens=max_tokens, timeout_s=timeout)
        dspy.settings.configure(lm=lm)
        return lm
