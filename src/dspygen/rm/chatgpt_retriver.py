# Import necessary modules and functions
from pathlib import Path
from typing import Union, List, Optional

import chromadb
import dspy
from chromadb.utils import embedding_functions

from dspygen.utils.file_tools import data_dir


def get_collection(persist_directory: Path, collection_name: str):
    """Initialize or retrieve the collection from the ChromaDB client."""
    client = chromadb.PersistentClient(path=str(persist_directory))
    return client.get_or_create_collection(name=collection_name,
                                           embedding_function=embedding_functions.DefaultEmbeddingFunction())


def prepare_queries(query_or_queries: Union[str, List[str]]) -> List[str]:
    """Prepare and validate the queries."""
    return [query_or_queries] if isinstance(query_or_queries, str) else [q for q in query_or_queries if q]


def generate_embeddings(queries: List[str], embedding_function) -> List:
    """Generate embeddings for the queries."""
    return embedding_function(queries)


def query_collection(collection, embeddings: List, k: int, contains: Optional[str], role: str) -> list[str]:
    """Query the collection with the generated embeddings."""
    query_params = {
        "query_embeddings": embeddings,
        "n_results": k,
        "where": {"role": role}
    }
    if contains:
        query_params["where_document"] = {"$contains": contains}
    results = collection.query(**query_params)
    return results["documents"]


class ChatGPTRetriever(dspy.Retrieve):
    def __init__(self,
                 json_file_path: str = data_dir("conversations.json"),
                 collection_name: str = "chatgpt",
                 persist_directory: str = data_dir(),
                 k=5):
        """Initialize the ChatGPTRetriever."""
        super().__init__(k)
        self.json_file_path = json_file_path
        self.collection_name = collection_name
        self.k = k
        self.persist_directory = Path(persist_directory)

    def forward(self, query_or_queries: Union[str, List[str]], k: Optional[int] = None, contains: Optional[str] = None, role: str = "assistant") -> list[str]:
        """Search for top passages based on the provided query or queries."""
        collection = get_collection(self.persist_directory, self.collection_name)
        queries = prepare_queries(query_or_queries)
        embeddings = generate_embeddings(queries, embedding_functions.DefaultEmbeddingFunction())
        return query_collection(collection, embeddings, k or self.k, contains, role)


def main2():
    from dspygen.utils.dspy_tools import init_dspy
    from loguru import logger
    init_dspy(model="gpt-4")

    retriever = ChatGPTRetriever()
    query = "Revenue Operations Automation"
    matched_conversations = retriever.forward(query, k=100)
    # print(count_tokens(str(matched_conversations) + "\nI want a DSPy module that generates Python source code."))
    for conversation in matched_conversations:
        logger.info(conversation)

    from dspygen.modules.python_source_code_module import python_source_code_call
    logger.info(python_source_code_call(str(matched_conversations)))


def main():
    retriever = ChatGPTRetriever()
    query = "BookGen"

    matched_conversations = retriever.forward("The", k=10, contains="The")

    # Filter out response that less than 500 characters
    # matched_conversations = [conv for conv in matched_conversations if len(conv) > 500]

    for conversation in matched_conversations:
        print(conversation)


if __name__ == "__main__":
    main()
