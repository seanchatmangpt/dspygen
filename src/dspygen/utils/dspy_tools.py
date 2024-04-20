import dspy

llama3_inst = "llama3:8b-instruct-q5_1"  #max_tokens: int = 8000,

mistral_inst = "mistral:instruct"        #max_tokens: int = 30000,

def init_dspy(lm=dspy.OllamaLocal(model=llama3_inst, timeout_s = 300), max_tokens: int = 8000, lm_instance=None):

#def init_dspy_(lm_class=dspy.OpenAI, max_tokens: int = 500, model: str = "gpt-3.5-turbo-instruct", lm_instance=None):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance)
    else:
        lm = dspy.OllamaLocal(model="llama3:8b-instruct-q5_1", max_tokens=8000, timeout_s=480)
       # lm = lm_class(max_tokens=max_tokens, model=model)
        dspy.settings.configure(lm=lm)
