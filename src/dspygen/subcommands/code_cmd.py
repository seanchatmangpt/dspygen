# """code"""
# import typer
# from loguru import logger
#
# from dspygen.dspy_modules.python_source_code_module import python_source_code_call
# from dspygen.rm.chatgpt_chromadb_retriever import ChatGPTChromaDBRetriever
# from dspygen.utils.dspy_tools import init_dspy
# from dspygen.lm.groq_lm import Groq
#
# app = typer.Typer(help="Code subcommands.")
#
#
# @app.command(name="create")
# def _create(todo: str = typer.Argument(..., help="What to do?")):
#     """create"""
#     init_dspy()
#     code = python_source_code_call(todo)
#     typer.echo(code)
#
#
# def main():
#     init_dspy(model="gpt-4")
#
#     retriever = ChatGPTChromaDBRetriever()
#     query = "Revenue Operations Automation"
#     matched_conversations = retriever.forward(query, k=10)
#     # print(count_tokens(str(matched_conversations) + "\nI want a DSPy module that generates Python source code."))
#     for conversation in matched_conversations:
#         logger.info(conversation)
#
#     logger.info(python_source_code_call(str(matched_conversations)))
#
#
# if __name__ == '__main__':
#     main()
