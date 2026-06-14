# Import necessary dspy_modules and functions
from pathlib import Path
from typing import Union, List, Optional, Any

import chromadb
import dspy
from chromadb.api.models.Collection import Collection
from loguru import logger

from dspygen.rm.chatgpt_chromadb_retriever import default_embed_fn
from dspygen.utils.file_tools import data_dir


def get_collection(persist_directory: Path, collection_name: str, embed_fn: Any = default_embed_fn) -> Collection:
    """Initialize or retrieve the collection from the ChromaDB PersistentClient.

    Args:
        persist_directory: Directory where ChromaDB persists its data.
        collection_name: Name of the collection to get or create.
        embed_fn: ChromaDB-compatible embedding function.

    Returns:
        The named ChromaDB collection.

    Raises:
        chromadb.errors.ChromaError: If the client cannot connect or the
            collection cannot be created.
    """
    try:
        client = chromadb.PersistentClient(path=str(persist_directory))
        return client.get_or_create_collection(
            name=collection_name,
            embedding_function=embed_fn,
        )
    except Exception as exc:
        logger.error(f"ChromaDB connection error for path={persist_directory!r}: {exc}")
        raise


def prepare_queries(query_or_queries: Union[str, List[str]]) -> List[str]:
    """Prepare and validate the queries."""
    return [query_or_queries] if isinstance(query_or_queries, str) else [q for q in query_or_queries if q]


def generate_embeddings(queries: List[str], embedding_function: Any) -> List:
    """Generate embeddings for the queries."""
    return embedding_function(queries)


def query_collection(
    collection: Collection,
    embeddings: List,
    k: int,
    contains: Optional[str],
    role: str,
    include: Optional[List[str]] = None,
) -> list[str]:
    """Query the collection with the generated embeddings.

    Args:
        collection: ChromaDB collection to query.
        embeddings: Pre-computed query embeddings.
        k: Number of results to return (n_results).
        contains: Optional substring filter applied via ``where_document``.
        role: Metadata filter for the ``role`` field.
        include: Fields to include in results (defaults to ``["documents"]``).

    Returns:
        List of matching document strings.
    """
    if include is None:
        include = ["documents"]

    query_params: dict[str, Any] = {
        "query_embeddings": embeddings,
        "n_results": k,
        "where": {"role": role},
        "include": include,
    }
    if contains:
        query_params["where_document"] = {"$contains": contains}

    results = collection.query(**query_params)
    return results["documents"]


class ChromaRetriever(dspy.Retrieve):
    def __init__(
        self,
        collection_name: str,
        persist_directory: Union[str, Path] = data_dir(),
        embed_fn: Any = default_embed_fn,
        k: int = 5,
    ) -> None:
        """Initialize the ChromaRetriever.

        Args:
            collection_name: Name of the ChromaDB collection to query.
            persist_directory: Directory where ChromaDB data is stored.
            embed_fn: ChromaDB-compatible embedding function.
            k: Default number of results to return.
        """
        super().__init__(k)
        self.collection_name = collection_name
        self.k = k
        self.persist_directory = Path(persist_directory)
        self.embedding_function = embed_fn

    def forward(
        self,
        query_or_queries: Union[str, List[str]],
        k: Optional[int] = None,
        contains: Optional[str] = None,
        role: str = "assistant",
    ) -> list[str]:
        """Search for top passages based on the provided query or queries.

        Args:
            query_or_queries: One or more query strings.
            k: Number of results to return; falls back to ``self.k``.
            contains: Optional substring filter on retrieved documents.
            role: Metadata ``role`` filter (default ``"assistant"``).

        Returns:
            List of matching document strings.
        """
        collection = get_collection(self.persist_directory, self.collection_name, self.embedding_function)
        queries = prepare_queries(query_or_queries)
        embeddings = generate_embeddings(queries, self.embedding_function)
        return query_collection(collection, embeddings, k or self.k, contains, role)


def main2() -> None:
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy(model="gpt-4")

    retriever = ChromaRetriever("chatgpt")
    query = "Revenue Operations Automation"
    matched_conversations = retriever.forward(query, k=100)
    for conversation in matched_conversations:
        logger.info(conversation)

    from dspygen.modules.python_source_code_module import python_source_code_call
    logger.info(python_source_code_call(str(matched_conversations)))


def main() -> None:
    from dspygen.utils.dspy_tools import init_ol
    init_ol(max_tokens=4000)
    retriever = ChromaRetriever("chatgpt")
    query = "MIPRO"

    matched_conversations = retriever.forward(query, k=10, contains=query)

    for conversation in matched_conversations:
        print(conversation)


if __name__ == "__main__":
    main()
