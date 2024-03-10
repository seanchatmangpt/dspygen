import subprocess

from dspygen.experiments.gen_python_primitive import gen_bool, gen_list
from dspygen.modules.checker_module import checker_call
from dspygen.modules.cli_bot_module import cli_bot_call
from dspygen.utils.dspy_tools import init_dspy


def main():
    init_dspy()
#
#     # cmd_list = gen_list("10 cli commands to generate a docusign clone with RoR")
#
#     # print(cmd_list)
#
    project_name = "docusign_clone"

    model_list = ['Document', 'User', 'Signature']

    rails_cmds = [f'rails new {project_name}',
                  f'cd {project_name}',
                  'bundle install',
                  'rails generate scaffold Document name:string content:text',
                  'rails generate scaffold User name:string email:string',
                  'rails generate scaffold Signature user:references document:references',
                  'rake db:migrate',
                  'rails server',
                  'git init', 'git add .', 'git commit -m "Initial commit"']

    for model in model_list:
        f"rails generate scaffold {model} name:string"
#
#
    # print(f"{command} command to be run with CLI")
#
#     # Use subprocess to call the command
    for cmd in rails_cmds:
        print(cmd)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result)
#
#         # Print the output of the command
        print("Command output:")
        print(result.stdout)
#
#         # Print any errors, if they occurred
        if result.stderr:
            print("Errors:")
            print(result.stderr)


# def main():
#     init_dspy()
    # Define the command you want to execute
    # prompt = "Create RoR project" # input("Enter prompt for CLI bot: ")
    # prompt = "Bash "
    # command = cli_bot_call("install rails in one bash command on osx without brew")
    # print(command)

    # answer = gen_bool(f"Will this command delete a drive? {command}\nAnswer:")

if __name__ == '__main__':
    main()
