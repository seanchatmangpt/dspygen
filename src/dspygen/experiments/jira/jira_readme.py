from dspygen.dsl.dsl_pipeline_executor import execute_pipeline


def main():
    """Main function"""

    context = execute_pipeline("readme_generator.yaml",
                               {"user_input": "AI Swarm for Jira, Confluence, Slack, Google Workspace"})

    print(context)


if __name__ == '__main__':
    main()
