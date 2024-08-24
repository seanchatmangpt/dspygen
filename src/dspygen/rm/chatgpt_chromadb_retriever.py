import hashlib
import dspy
import ijson
from pathlib import Path
from typing import List, Optional, Union, Any

from loguru import logger
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from munch import Munch
from pydantic import BaseModel, ValidationError, Field

from dspygen.modules.python_source_code_module import python_source_code_call
from dspygen.utils.file_tools import data_dir, count_tokens

#from llama_index.embeddings.huggingface import HuggingFaceEmbedding ## pip install llama-index-embeddings-huggingface


# Configure loguru logger
#logger.add("chatgpt_chromadb_retriever.log", rotation="10 MB", level="ERROR")


def calculate_file_checksum(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    print("Chromadb path: ", file_path)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
            print(chunk)
    return hash_md5.hexdigest()


# Pydantic models
class Author(BaseModel):
    role: str
    name: Optional[str] = None
    metadata: dict


class ContentPart(BaseModel):
    content_type: str
    parts: Optional[List[Union[str, dict]]] = None  # Allow parts to be either strings or dicts


class Message(BaseModel):
    id: str
    author: Author
    content: ContentPart
    status: str
    metadata: dict


class Data(BaseModel):
    id: str
    message: Optional[Message] = None  # Allow message to be None
    parent: Optional[str] = None
    children: List[str]


class Conversation(BaseModel):
    title: str
    mapping: dict



#default_embed_fn_hf = embedding_functions.HuggingFaceEmbeddingFunction ( #HuggingFaceEmbedding(
#    api_key="",
#    model_name="BAAI/bge-small-en-v1.5",
#)

default_embed_fn = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="llama3",
)


class ChatGPTChromaDBRetriever(dspy.Retrieve):
    def __init__(
        self,
        json_file_path: str = data_dir() / "chatgpt_logs" / "conversations.json",
        collection_name: str = "chatgpt",
        persist_directory: str = data_dir(),
        check_for_updates: bool = True,
        embed_fn=default_embed_fn,
        k=5,
    ):
        """Initialize the ChatGPTChromaDBRetriever."""
        super().__init__(k)
        self.json_file_path = json_file_path
        self.collection_name = collection_name
        self.k = k
        self.persist_directory = Path(persist_directory)
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.embedding_function = embed_fn
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
        )
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        if not check_for_updates:
            return

        self.current_checksum = calculate_file_checksum(json_file_path)
        self.last_processed_checksum = self._load_last_processed_checksum()

        if self.current_checksum != self.last_processed_checksum:
            logger.info("Detected changes in the conversation history, processing...")
            self._process_and_store_conversations()
            self._save_last_processed_checksum()

    def _load_last_processed_checksum(self) -> Optional[str]:
        checksum_file = self.persist_directory / "last_checksum.txt"
        try:
            return checksum_file.read_text().strip()
        except FileNotFoundError:
            return None

    def _save_last_processed_checksum(self):
        checksum_file = self.persist_directory / "last_checksum.txt"
        checksum_file.write_text(self.current_checksum)

    def _process_and_store_conversations(self):
        with open(self.json_file_path, "rb") as json_file:
            count = -1
            while True:
                try:
                    for conversation in ijson.items(json_file, "item"):
                        count += 1
                        print(f"Processing conversation #{count} {conversation['title']}")
                        try:
                            validated_conversation = Conversation(**conversation)
                            for _, data in validated_conversation.mapping.items():
                                validated_data = Data(**data)

                                # Search if document already exists
                                search_results = self.collection.get(ids=[validated_data.id])
                                if len(search_results["ids"]) > 0:
                                    logger.info(f"Skipping already existing document #{count} with ID: {validated_data.id}")
                                    continue

                                if validated_data.message and validated_data.message.content.parts:
                                    # Filter and process text parts only
                                    document_text = ' '.join(
                                        part for part in validated_data.message.content.parts if isinstance(part, str)
                                    )

                                    if len(document_text) < 200:
                                        continue

                                    self.collection.add(
                                        documents=[document_text],
                                        metadatas=[{"id": validated_data.id}],
                                        ids=[validated_data.id],
                                    )
                                    logger.debug(f"Added document with ID: {validated_data.id}")

                        except ValidationError as e:
                            logger.error(f"Validation error: {e}")
                    break
                except ijson.JSONError as e:
                    logger.error(f"JSON parsing error: {e}")
                    break  # Exit the loop if we encounter a JSON parsing error

    def _update_collection_metadata(self):
        with open(self.json_file_path, "rb") as json_file:
            while True:
                try:
                    for conversation in ijson.items(json_file, "item"):
                        try:
                            validated_conversation = Conversation(**conversation)
                            for _, data in validated_conversation.mapping.items():
                                validated_data = Data(**data)

                                if validated_data.message and validated_data.message.content.parts:
                                    # Filter and process text parts only
                                    document_text = ' '.join(
                                        part for part in validated_data.message.content.parts if isinstance(part, str)
                                    )

                                    meta = Munch()
                                    meta.id = validated_data.id
                                    meta.role = validated_data.message.author.role
                                    meta.title = validated_conversation.title

                                    self.collection.update(metadatas=[meta], ids=[validated_data.id])
                                    logger.debug(f"Updated document with ID: {validated_data.id}")

                        except ValidationError as e:
                            logger.error(f"Validation error: {e}")
                    break
                except ijson.JSONError as e:
                    logger.error(f"JSON parsing error: {e}")
                    break  # Exit the loop if we encounter a JSON parsing error

    def forward(
        self,
        query_or_queries: Union[str, List[str]],
        k: Optional[int] = None,
        contains: Optional[str] = None,
        role: str = "assistant",
    ) -> list[str]:
        """Search with ChromaDB for top passages for the provided query/queries.

        Args:
            query_or_queries (Union[str, List[str]]): The query or queries to search for.
            k (Optional[int], optional): The number of top passages to retrieve. Defaults to None, which will use the value in self.k.
            contains (Optional[str], optional): The string that the retrieved passages must contain. Defaults to None.
            role: The role of the author of the message. Defaults to "assistant".

        Returns:
            dspy.Prediction: An object containing the retrieved passages.
        """

        queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries
        queries = [q for q in queries if q]  # Filter empty queries

        # Check if queries is empty after filtering
        if not queries:
            logger.error("No valid queries provided")
            return []

        try:
            embeddings = self.embedding_function(queries)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []

        # Ensure embeddings are not empty
        if not embeddings or not embeddings[0]:
            logger.error("No embeddings generated")
            return []

        k = self.k if k is None else k

        try:
            if contains is not None:
                results = self.collection.query(
                    query_embeddings=embeddings,
                    n_results=k,
                    where={"role": role},
                    where_document={"$contains": contains},
                )
            else:
                results = self.collection.query(
                    query_embeddings=embeddings,
                    where={"role": role},
                    n_results=k,
                )
        except Exception as e:
            logger.error(f"Error querying the collection: {e}")
            return []

        return results.get("documents", [[]])[0]


def main():
    from dspygen.utils.dspy_tools import init_ol

    init_ol(model="phi3:medium", max_tokens=5000, timeout=500)

    retriever = ChatGPTChromaDBRetriever(check_for_updates=False)
    # retriever._update_collection_metadata()

    query = "AGI Thin Air"
    matched_conversations = retriever.forward(query, k=10, contains="OSIRIS")
    # print(count_tokens(str(matched_conversations) + "\nI want a DSPy module that generates Python source code."))
    for conversation in matched_conversations:
        logger.info(conversation)

    logger.info(python_source_code_call(str(matched_conversations)))


def main2():
    """Updating metadata of the collection"""
    retriever = ChatGPTChromaDBRetriever(check_for_updates=False)
    retriever._update_collection_metadata()


if __name__ == "__main__":
    main()
