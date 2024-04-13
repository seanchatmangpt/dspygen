import random

from dspygen.modules.arch_module import arch_call
from dspygen.modules.elite_module import elite_call
from dspygen.rm.python_code_retriever import PythonCodeRetriever

def get_files_from_directory(directory, gitignore=None):
    """Retrieves code snippets from a specified directory using CodeRetriever.

    Args:
        directory (str): The path to the directory.
        gitignore (str, optional): The path to a .gitignore file. Defaults to None.
    """
    retriever = PythonCodeRetriever(include_signatures=True, include_docstrings=True, include_executable_code=True)
    result = retriever.forward(directory)
    return result  # Return the list of file contents

def get_abstract_saga(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_saga' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_saga')
    

def get_abstract_aggregate(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_aggregate' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_aggregate')
    

def get_abstract_read_model(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_read_model' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_read_model')
    

def get_abstract_view(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_view' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_view')
    

def get_abstract_task(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_task' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_task')
    

def get_abstract_policy(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_policy' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_policy')
    

def get_abstract_value_object(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_value_object' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_value_object')
    

def get_domain_exception(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/domain_exception' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/domain_exception')
    

def get_abstract_query(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_query' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_query')
    

def get_abstract_event(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_event' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_event')
    

def get_abstract_command(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/ddd/abstract_command' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/ddd/abstract_command')
    

def get_repositories(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/repositories' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/repositories')
    

def get_introduction(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/introduction' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/introduction')
    

def get_appendices(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/appendices' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/appendices')
    

def get_language_models(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/foundations/language-models' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/foundations/language-models')
    

def get_testing(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/testing' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/testing')
    

def get_architecture(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/architecture' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/architecture')
    

def get_infrastructure(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/implementation/infrastructure' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/implementation/infrastructure')
    

def get_best_practices(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/best-practices' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/books/socratic_tutor/src/best-practices')
    

def get_tutor_bot(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/tutor_bot' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/tutor_bot')
    

def get_configs(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/configs' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/configs')
    

def get_actors(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/actors' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/actors')
    

def get_critical_vision(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/data/critical_vision' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/data/critical_vision')
    

def get_business_skills(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/data/business_skills' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/data/business_skills')
    

def get_logical_thinking(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/data/logical_thinking' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/data/logical_thinking')
    

def get_models(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/models' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/models')


def get_domain_models():
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/models' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/models/domain_models')


def get_root_aggregates():
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/models' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/models/root_aggregates')


def get_value_objects():
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/models' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/models/value_objects')


def get_services(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/services' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/services')


def get_modules():
    """Retrieves code snippets from the '/Users/candacechatman/dev/soc/src/soc/services' directory."""
    return get_files_from_directory('/Users/candacechatman/dev/soc/src/soc/modules')


def main():
    import pyperclip
    pyperclip.copy(f"{get_modules()}")

def main3():
    print(get_domain_models())
    print(get_root_aggregates())
    print(get_value_objects())

    import pyperclip
    pyperclip.copy(f"{get_domain_models()} {get_root_aggregates()} {get_value_objects()}")


def main2():
    from loguru import logger
    import os
    from dspygen.utils.dspy_tools import init_dspy
    from dspygen.lm.groq_lm import Groq
    init_dspy(lm_class=Groq, model="mixtral-8x7b-32768")

    from dspygen.rm.chatgpt_chromadb_retriever import ChatGPTChromaDBRetriever
    from dspygen.modules.python_source_code_module import python_source_code_call
    import time

    # Initial setup for the retrieval query and the iteration count
    iteration_count = 5  # Define how many iterations you want to perform

    last_filename = None

    while True:
        retriever = ChatGPTChromaDBRetriever()
        query = "DeepSkill Socrates"

        matched_conversations = retriever.forward(query, k=20)

        # Pick 5 random conversations from the matched conversations
        matched_conversations = random.sample(matched_conversations, 5)

        # Assuming `get_root_aggregates` and `arch_call` are defined elsewhere and relevant
        # You might need to adjust these calls according to your actual functions and data structures
        prompt = f"{matched_conversations}"

        # Simulate `arch_call` and `elite_call` with your own mechanism to generate the prompt and process it
        # For demonstration, these functions should be defined to use the DSPy model for generating code
        aprompt = arch_call(prompt)

        # If there was a file generated in the last iteration, read its content and append it to the new prompt
        if last_filename and os.path.exists(last_filename):
            with open(last_filename, "r") as f:
                previous_code = f.read()
                # Update the prompt with information from the last iteration
                # aprompt += f"\n\n# Previous Iteration Code:\n{previous_code}"

        code = elite_call(challenge_description=str(aprompt), example_io=str(get_root_aggregates()))

        # Save the generated code to disk, using the current time as part of the filename
        filename = f"{str(time.time())}.py"
        with open(filename, "w") as f:
            f.write(code)
        logger.info(f"Generated code saved as {filename}")

        # Update the last filename for the next iteration
        last_filename = filename
        # Optional: Update the query or any other dynamic elements for the next iteration

    # logger.info("Process completed.")


if __name__ == '__main__':
    main()
