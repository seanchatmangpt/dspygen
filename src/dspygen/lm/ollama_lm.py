import os
import dspy
from dsp import LM
from dspygen.utils.dspy_tools import init_dspy
from dspy import OllamaLocal as OllamaClient

# Default model for Ollama
llama3_inst = "llama3:8b-instruct-q5_1"  #max_tokens: int = 8000,

mistral_inst = "mistral:instruct"        #max_tokens: int = 30000,

default_ollama_model = llama3_inst

class Ollama(LM):
    def __init__(self, model=default_ollama_model, **kwargs):
        super().__init__(model)
        
        # Print which model is being used
        print("Ollama model used today: " + model)
        self.provider = "default"
        self.history = []

        # Initialize the Ollama client with the API key
        self.client = OllamaClient(model=model, timeout_s = 300)

    def basic_request(self, prompt, **kwargs):
        # Request a chat completion with the given prompt and model
        chat_completion = self.client.request(prompt, **kwargs)
        
        # Check for choices and extract the content from 'message'
        if 'choices' in chat_completion:
            # Return the 'content' of the first choice
            return [choice['message']['content'] for choice in chat_completion['choices']]
        else:
            raise ValueError("Expected 'choices' key not found in response")

    def __call__(self, prompt, **kwargs):
        return self.basic_request(prompt, **kwargs)
    

# Main function to initialize dspy with Ollama and run a prediction
def main():
    # Initialize dspy with the Ollama class and specified model
    init_dspy(Ollama, model=default_ollama_model, max_tokens=8000)
    
    # Generate prediction for a specific prompt
    pred = dspy.Predict("prompt -> code")(prompt="Fast API CRUD endpoint for fire alarm global IoT network")
    
    # Print the generated code
    print(pred.code)

# Entry point of the script
if __name__ == '__main__':
    main()
