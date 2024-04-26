from loguru import logger

from dspygen.modules.python_source_code_module import python_source_code_call
from dspygen.rm.chatgpt_chromadb_retriever import ChatGPTChromaDBRetriever
from dspygen.utils.dspy_tools import init_dspy
from dspygen.lm.groq_lm import Groq


def main():
    init_dspy(lm_class=Groq, model="mixtral-8x7b-32768")

    retriever = ChatGPTChromaDBRetriever()
    query = "Revenue Operations Automation"
    matched_conversations = retriever.forward(query, k=10)
    # print(count_tokens(str(matched_conversations) + "\nI want a DSPy module that generates Python source code."))
    for conversation in matched_conversations:
        logger.info(conversation)

    logger.info(python_source_code_call(str(matched_conversations)))


if __name__ == '__main__':
    main()
