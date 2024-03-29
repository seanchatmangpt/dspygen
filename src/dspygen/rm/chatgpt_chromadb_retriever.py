import hashlib

import dspy
import ijson
from pathlib import Path
from typing import List, Optional, Union

from dsp import dotdict
from loguru import logger

import chromadb
from chromadb.utils import embedding_functions
from pydantic import BaseModel, ValidationError
from dspygen.utils.file_tools import data_dir

# Configure loguru logger
# logger.add("chatgpt_chromadb_retriever.log", rotation="10 MB")

def calculate_file_checksum(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Pydantic models
class Author(BaseModel):
    role: str
    name: Optional[str] = None
    metadata: dict

class ContentPart(BaseModel):
    content_type: str
    parts: List[str] | None

class Message(BaseModel):
    id: str
    author: Author
    content: ContentPart
    status: str
    metadata: dict

class Data(BaseModel):
    id: str
    message: Message | None
    parent: str | None
    children: List[str]

class Conversation(BaseModel):
    title: str
    mapping: dict

class ChatGPTChromaDBRetriever:
    def __init__(self, json_file_path: str = data_dir("conversations.json"), collection_name: str = "chatgpt", persist_directory: str = data_dir()):
        self.json_file_path = json_file_path
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(name=self.collection_name, embedding_function=self.embedding_function)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.current_checksum = calculate_file_checksum(json_file_path)
        self.last_processed_checksum = self._load_last_processed_checksum()

        if self.current_checksum != self.last_processed_checksum:
            logger.info("Detected changes in the conversation history, processing...")
            self._process_and_store_conversations()
            self._save_last_processed_checksum()
        else:
            logger.info("No changes detected in the conversation history. Skipping processing.")

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
            for conversation in ijson.items(json_file, "item"):
                try:
                    validated_conversation = Conversation(**conversation)
                    for _, data in validated_conversation.mapping.items():
                        validated_data = Data(**data)

                        # Search if document already exists
                        search_results = self.collection.get(ids=[validated_data.id])
                        if len(search_results["ids"]) > 0:
                            logger.debug(f"Skipping already existing document with ID: {validated_data.id}")
                            continue

                        if validated_data.message:
                            document_text = ' '.join(part for part in validated_data.message.content.parts if part)
                            self.collection.add(documents=[document_text], metadatas=[{"id": validated_data.id}],
                                                ids=[validated_data.id])
                            logger.debug(f"Added document with ID: {validated_data.id}")

                except ValidationError as e:
                    logger.error(f"Validation error: {e}")

    def forward(
            self, query_or_queries: Union[str, List[str]], k: Optional[int] = None
    ) -> dspy.Prediction:
        """Search with ChromaDB for top passages for the provided query/queries.

        Args:
            query_or_queries (Union[str, List[str]]): The query or queries to search for.
            k (Optional[int], optional): The number of top passages to retrieve. Defaults to None, which will use the value in self.k.

        Returns:
            dspy.Prediction: An object containing the retrieved passages.
        """

        queries = (
            [query_or_queries]
            if isinstance(query_or_queries, str)
            else query_or_queries
        )
        queries = [q for q in queries if q]  # Filter empty queries
        embeddings = self.embedding_function(queries)

        k = self.k if k is None else k
        results = self.collection.query(query_embeddings=embeddings, n_results=k)

        passages = [dotdict({"long_text": result.document}) for result in results["results"][0]]
        return passages  # Assuming your dspy.Prediction expects this format

def main():
    retriever = ChatGPTChromaDBRetriever()
    query = "What is the impact of AI on society?"
    matched_conversations = retriever.search(query=query)
    for conversation in matched_conversations:
        logger.info(conversation)

if __name__ == "__main__":
    main()
