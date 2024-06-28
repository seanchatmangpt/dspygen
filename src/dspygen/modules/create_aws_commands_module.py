import dspy
import subprocess
from dspygen.utils.dspy_tools import init_ol


class CreateAWSCLICommandChainSignature(dspy.Signature):
    """
    Create a massively complex AWS CLI command chain to set up the most advanced system in the style of an
    AWS System Architect.
    """
    system_requirements = dspy.InputField(desc="The high-level requirements of the system to be set up.")
    command_chain = dspy.OutputField(desc="The AWS CLI command chain to set up the system.")


class CreateAWSCLICommandChainModule(dspy.Module):
    """CreateAWSCLICommandChainModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, system_requirements):
        pred = dspy.ChainOfThought(CreateAWSCLICommandChainSignature)
        self.output = pred(system_requirements=system_requirements)
        # print(str(self.output))
        return self.output


def create_aws_cli_command_chain(system_requirements) -> str:
    create_command_chain = CreateAWSCLICommandChainModule()
    command_chain: str = create_command_chain.forward(system_requirements=system_requirements).command_chain
    return command_chain


def execute_command_chain(command_chain: str):
    try:
        subprocess.run(command_chain, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command chain '{command_chain}' failed with exit code {e.returncode}")
        raise SystemExit


def main():
    init_ol(model="qwen2:7b-instruct", timeout=30)

    system_requirements = """
    1. Set up a Kubernetes cluster using EKS.
    2. Deploy Dapr runtime on the cluster.
    3. Configure IAM roles and policies.
    4. Set up S3 buckets for state store.
    5. Configure RDS database for pub/sub.
    6. Set up secure communication with SSL.
    """

    command_chain = create_aws_cli_command_chain(system_requirements=system_requirements)

    from dspygen.utils.markdown_tools import print_markdown
    print_markdown(command_chain)

    from dspygen.utils.markdown_tools import extract_triple_backticks
    cmds = extract_triple_backticks(command_chain)

    print(cmds)

    # execute_command_chain(command_chain)


if __name__ == "__main__":
    main()
