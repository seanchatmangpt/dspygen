# dspygen_py\src\dspygen\rm\dspy_dev_steps.py
import dspy
import pygame
import sys
from dspygen.lm.groq_lm import Groq
from dspygen.utils.dspy_tools import init_dspy, init_ol
from dspygen.rm.dynamical_signature_util import create_dynamic_signature_class

class SetupPygameEnv(dspy.Signature):
    """Sets up the Pygame environments."""
    task_description = dspy.InputField(desc="Description of the task to set up the Pygame environments.")
    code_snippet = dspy.OutputField(desc="Generated code snippet for setting up Pygame.")

class CreateGameWindow(dspy.Signature):
    """Creates the game window and main loop."""
    task_description = dspy.InputField(desc="Description of the task to create the game window and main loop.")
    code_snippet = dspy.OutputField(desc="Generated code snippet for creating the game window and main loop.")

class ImplementGameGrid(dspy.Signature):
    """Implements the game grid."""
    task_description = dspy.InputField(desc="Description of the task to implement the game grid.")
    code_snippet = dspy.OutputField(desc="Generated code snippet for implementing the game grid.")

class CreateTetrisShapes(dspy.Signature):
    """Creates Tetris shapes and movement."""
    task_description = dspy.InputField(desc="Description of the task to create Tetris shapes and movement.")
    code_snippet = dspy.OutputField(desc="Generated code snippet for creating Tetris shapes and movement.")

class AddCollisionDetection(dspy.Signature):
    """Adds collision detection."""
    task_description = dspy.InputField(desc="Description of the task to add collision detection.")
    code_snippet = dspy.OutputField(desc="Generated code snippet for adding collision detection.")

class ImplementScoringSystem(dspy.Signature):
    """Implements the scoring system."""
    task_description = dspy.InputField(desc="Description of the task to implement the scoring system.")
    code_snippet = dspy.OutputField(desc="Generated code snippet for implementing the scoring system.")

class AddGameOverConditions(dspy.Signature):
    """Adds game over conditions."""
    task_description = dspy.InputField(desc="Description of the task to add game over conditions.")
    code_snippet = dspy.OutputField(desc="Generated code snippet for adding game over conditions.")

class Refine(dspy.Signature):
    """Refines UI/UX and make code pretty and tested."""
    task_description = dspy.InputField(desc="Description of the task to refine code.")
    code_snippet = dspy.OutputField(desc="Pure working refactor code snippet - no other chat text or code discussions allowed outside!")

def get_user_rfc(error_message):
    action = input(f"An error occurred: {error_message}\n(1) use the default error message to fix or (2) provide your own RFC: (1/2): ")
    if action == "1":
        return f"fix {error_message.lower()}"
    else:
        suggestions = input("Please provide your RFC: ")
        return suggestions

def extract_code_snippet(full_response):
    start = max(full_response.find("```") + 3, full_response.find("```python\n") + 5)
    end = full_response.rfind("```")

    if start > 2 and end > start:
        full_response = full_response[start:end].strip()
        start = full_response.find("thon") + 1
        if start < 10:
            end = len(full_response)
            if full_response[4:7] == "hon":
                print(full_response[0:8] + f" funny start still in - skip " + str(start))
                return full_response[7:end].strip()
            if start == 1:
                return full_response[4:end].strip()
            return full_response[start:end].strip()
        return full_response
    return full_response.strip()

def execute_code_snippet(code_snippet):
    try:
        exec(code_snippet, {'pygame': pygame, 'sys': sys})
    except Exception as e:
        return False, str(e)
    return True, ""

def process_step(step_class, task_description):
    attempt = 0
    max_attempts = 2
    rfc = None
    code_snippet = None
    code_snippet_ok_list = []

    while attempt < max_attempts:
        attempt += 1
        print(step_class)
        print(f"\nAttempt {attempt} for task: {task_description}")
        if rfc:
            response = dspy.ChainOfThought(step_class)(task_description=task_description, rfc=rfc, code_snippet_with_errors=code_snippet).code_snippet
        else:
            response = dspy.ChainOfThought(step_class)(task_description=task_description).code_snippet
        code_snippet = extract_code_snippet(response)
        print(f"Generated Code:\n{code_snippet}")
        success, error = execute_code_snippet(code_snippet.replace("sys.exit()", "#sys.exit()").replace("pip install", "#pip install"))
        if success or error == "display Surface quit" or error == "video system not initialized":
            print("Code executed successfully.")
            code_snippet_ok_list.append(code_snippet)
            error = "ok"
            #return code_snippet_ok_list
        print(f"Error: {error}")
        rfc = get_user_rfc(error)
        if rfc == "ok":
            return code_snippet_ok_list
        print(f"Suggestions received: {rfc}")
        task_description = f"{task_description} {rfc}"
        step_class = create_dynamic_signature_class(step_class.__name__, rfc, code_snippet)
    print("Max attempts reached. Moving to next step.")
    return code_snippet_ok_list

def build_final_game_from(code_snippet_ok_list):
    final_game_code = "\n\n".join(code_snippet_ok_list)
    with open("final_game.py", "w") as f:
        f.write(final_game_code)
    print("Final game script written to final_game.py")

def main():
    """Main function"""
    #init_dspy(lm_class=Groq, max_tokens=1000, model="llama3-70b-8192", temperature=0.002)
    init_ol(model="phi3:instruct", max_tokens=4000, temperature=0.002, timeout=200)

    pygame_topic = "composable architecture Tetris pygame"

    steps = [
        (SetupPygameEnv, f"Set up environments for {pygame_topic}"),
        (CreateGameWindow, f"Create game window and main loop for {pygame_topic}"),
        (ImplementGameGrid, f"Implement game grid for {pygame_topic}"),
        (CreateTetrisShapes, f"Create shapes and movement buttons for {pygame_topic}"),
        (AddCollisionDetection, f"Add collision detection for {pygame_topic}"),
        (ImplementScoringSystem, f"Implement scoring system for {pygame_topic}"),
        (AddGameOverConditions, f"Add game over conditions for {pygame_topic}"),
        (Refine, f"Refine UI/UX and user action workflows for {pygame_topic}")
    ]

    all_code_snippets = []

    for step_class, description in steps:
        code_snippet_ok_list = process_step(step_class, description)
        if not code_snippet_ok_list:
            print(f"Failed to complete step: {description}")
            break
        all_code_snippets.extend(code_snippet_ok_list)

    if all_code_snippets:
        build_final_game_from(all_code_snippets)

if __name__ == '__main__':
    main()
