# wizard.py
import os
from pathlib import Path
import subprocess
from loguru import logger
from dspygen.rm.chatgpt_codemaster_retriever import ChatGPTChromaDBRetriever
from dspygen.rm.code_retriever import CodeRetriever
from dspygen.rm.structured_code_desc_saver import save_code_snippet
from datetime import datetime
import glob

# Configure logging
logger.add("wizard.log", rotation="10 MB", level="ERROR")

def run_code_in_directory(directory):
    for file_name in os.listdir(directory):
        file_path = directory / file_name
        if file_name.endswith('.py'):
            try:
                subprocess.run(['python', file_path], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Error running {file_name}: {e}")

def list_conversation_titles(retriever: ChatGPTChromaDBRetriever):
    titles = set()
    results = retriever.collection.get(limit=2000)  # Adjust limit if necessary
    for result in results['metadatas']:
        if 'title' in result:
            titles.add(result['title'])
    return sorted(list(titles))  # Sort the titles for easier selection

def get_all_snippets_for_title(retriever: ChatGPTChromaDBRetriever, selected_title, doc_id=None):
    query = f"specific code for `{selected_title}`"
    if doc_id:
        query = f"id== `{doc_id}`"
    #query = "```python import pygame import unittest def draw_grid  pygame.quit()\n```"

    print(query)
    matched_conversations = retriever.forward(query, k=10)  # Increase k to fetch more results if necessary
    
    snippets = []
    for conversation in matched_conversations:
        if 'description'in conversation :# or '6edb8608-f262-4772-89b5-7c3a414a4755' in conversation or doc_id in conversation or 'description' in conversation:
            code_path = conversation['code']
            title = conversation.get('title', '')
            description = conversation.get('description', '')
            doc_id = conversation.get('id', '')
            snippets.append((doc_id, code_path, description))
            #if doc_id == "116889e2-b2df-4d35-b49e-d5d7fe1bb481": #_cfd132a356d562d5ac20971df9587ea3"
            print("____", title, "code: ", code_path)
            print(doc_id, description)
    return snippets

def get_all_snippets_from_temp_code(retriever, selected_title):
    temp_code_directory = Path(f"data/temp_code/{selected_title}")
    files = glob.glob(f"{temp_code_directory}/**/*.py", recursive=True)
    
    snippets = []
    for file_path in files:
        doc_id = Path(file_path).stem
        description = "Loaded from: " + str(temp_code_directory)
        snippets.append((doc_id, file_path, description))
        #get_all_snippets_for_title(retriever, selected_title=selected_title, doc_id=doc_id)
    return snippets

def main():
    # Workflow steps and states - might be frozen into a Coder Inhabitant-System after best practice settled
    print("Create (OpenAI - ChatGPT / local soon...) Code-Creating conversations and note the title(s) to focus on new code / create a new repo.")
    print("Get to code to a most final state for real testing or deploy levels.")
    print("Download the conversation.zip / JSON by the download button once you recieve the mail and place the file into data/chatgpt_logs/. ")
    print("A TBD DSPyGen inhabitants will get triggered and will run the code_master_retriever workflow for full STP processing")
    print("This dspygen/rm/wizard.py should help you first set all needed things up / create if missing - use/improve all the exiting DSPyGEN tools too.")

    retriever = ChatGPTChromaDBRetriever(check_for_updates=True)

    get_all_snippets_for_title(retriever=retriever, selected_title="", doc_id="116889e2-b2df-4d35-b49e-d5d7fe1bb481") # -> 3516c571-c26e-44f9-a125-3b8105e2be07

    # ask or autodetect for run this once new conv is in the data/...
    # retriever._process_and_store_conversations() 
    print("Filled the vector DB AND the temp_code folder with last conversation.JSON time_stamp (TBD) ")

    # List all conversation titles
    titles = list_conversation_titles(retriever)
    print("Available conversation titles from vectorDB:")
    for idx, title in enumerate(titles):
        print(f"{idx + 1}. {title}")

    # get_all_titles_from_temp_code TBD

    # Let user select a title
    selected_idx = int(input("Select a conversation title by number: ")) - 1
    selected_title = titles[selected_idx]

    while True:
        snippets = list()
        exec_it = input("Get all code snippets for the selected conversation? (yes/no): ").strip().lower()
        if exec_it == 'yes' or exec_it == 'y':
            snippets += get_all_snippets_for_title(retriever, selected_title)
            #print(chromadb_snippets)
        exec_it = input("Get all code snippets from temp_code (DB) ? (yes/no): ").strip().lower()
        if exec_it == 'yes' or exec_it == 'y':
            snippets += get_all_snippets_from_temp_code(retriever, selected_title)
            #print(temp_code_snippets)
 
        if not snippets:
            print("No code snippets found in the selected conversation for selected title:", selected_title)
            continue  # Allow user to re-select

        temp_code_directory = Path(f"data/temp_code/{selected_title}")
        print(">>>>>>>>>>")
        print("Available code snippets from:", temp_code_directory)
        for idx, (doc_id, code, description) in enumerate(snippets):
            print(f"{idx + 1}. {doc_id} - {description}")

        # Let user select a snippet
        selected_snippet_idx = int(input("Select a code snippet by number: ")) - 1
        selected_doc_id, selected_code_path, selected_description = snippets[selected_snippet_idx]

        # Load the code content from the file at code_path
        # only from directory
        with open(selected_code_path, 'r') as file:
            code = file.read()

        save_code_snippet(temp_code_directory, selected_doc_id, code, selected_description)
        print("Code or Dir ", temp_code_directory)
        #code_retriever = CodeRetriever(temp_code_directory) #, gitignore)
        #result = code_retriever.forward()
        #run_code_in_directory(result)
        # Run the code to test
        exec_it = input("Run it? (yes/no): ").strip().lower()
        if exec_it == 'yes' or exec_it == 'y':
            run_code_in_directory(temp_code_directory)

        exec_it = input("Save it? (yes/no): ").strip().lower()
        if exec_it == 'yes':
            print("selected_code_path -Ret from:", selected_code_path)
            temp_code_directory = Path(f"data/temp_code/{selected_title}/repo")
            temp_code_directory.mkdir(parents=True, exist_ok=True)
            code_path = save_code_snippet(temp_code_directory, selected_doc_id, selected_code_path, selected_description)


        print("Call Code-Retriever from ChromaDB", temp_code_directory)
        exec_it = input("Go ? (yes/no): ").strip().lower()
        if exec_it == 'yes':
            print("file code: ", code_path)
            code_retriever = CodeRetriever(temp_code_directory) #, gitignore)
            result = code_retriever.forward("*.py")
            for code in result.passages:
                print("got forward code: ", code)
                exec_it = input("Run the code? (yes/no): ").strip().lower()
                if exec_it == 'yes':
                    run_code_in_directory(code)
                    exec_it = input("Save it? (yes/no): ").strip().lower()
                    if exec_it == 'yes':
                        print("selected_code_path -Ret from:", selected_code_path)
                        temp_code_directory = Path(f"data/temp_code/{selected_title}/repo")
                        temp_code_directory.mkdir(parents=True, exist_ok=True)
            
     
        while True:
            # Directory structure can be defined here or input by the user
            directory_structure = input("Enter the directory structure path for the new repo: ")
            powershell_script = retriever.generate_powershell_script([str(temp_code_directory / f"{selected_doc_id}.py")], directory_structure)
            print(f"Powershell Script:\n{powershell_script}")

            refine = input("Do you need to refine the code? (yes/no): ").strip().lower()
            if refine == 'yes':
                # DSPYGEN module use - not a prompt
                refined_code = "DSPYGEN module use - not a prompt"
                print("Refined Code:\n", refined_code)

                # Save the refined code snippet
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                refined_file_path = temp_code_directory / f"refined_{timestamp}.py"
                save_code_snippet(temp_code_directory, refined_file_path.stem, refined_code, "Refined code")

                # Run the refined code to test

                run_code_in_directory(temp_code_directory)
            else:
                break

        done = input("Are you done with this title? (yes/no): ").strip().lower()
        if done == 'yes':
            break

    print("Your project setup is complete. All code has been generated and refined.")

if __name__ == "__main__":
    main()
