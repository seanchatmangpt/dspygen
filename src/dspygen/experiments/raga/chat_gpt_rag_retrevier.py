# # main file
# from dspygen.rm.chatgpt_chromadb_retriever import Conversation, Data
# from pydantic import ValidationError
# from ragatouille import RAGPretrainedModel
# from pathlib import Path
# from typing import List, Optional, Union
# import hashlib
# import ijson
# from loguru import logger
#
# # Configure loguru logger
# logger.add("chatgpt_rag_retriever.log", rotation="10 MB", level="ERROR")
#
#
# # Helper function to calculate file checksum
# def calculate_file_checksum(file_path: str) -> str:
#     hash_md5 = hashlib.md5()
#     with open(file_path, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()
#
#
# class ChatGPTRAGRetriever:
#     def __init__(self,
#                  json_file_path: str = "/Users/sac/dev/dspygen/data/chatgpt_logs/conversations.json",
#                  index_name: str = "chatgpt_rag",
#                  persist_directory: str = ".rag_indexes",
#                  k: int = 5):
#         """Initialize the ChatGPTRAGRetriever with RAG indexing."""
#         self.json_file_path = Path(json_file_path)
#         self.index_name = index_name
#         self.k = k
#         self.persist_directory = Path(persist_directory)
#         self.index_path = self.persist_directory / self.index_name
#
#         self.persist_directory.mkdir(parents=True, exist_ok=True)
#         self.current_checksum = calculate_file_checksum(str(self.json_file_path))
#         self.last_processed_checksum = self._load_last_processed_checksum()
#
#         # Initialize a set to keep track of existing document IDs
#         self.existing_document_ids = set()
#
#         # Check if the index already exists and load it
#         if self.index_path.exists():
#             logger.info(f"Loading existing RAG index: {self.index_name}")
#             self.RAG = RAGPretrainedModel.from_index(str(self.index_path))
#         else:
#             logger.info(f"Creating a new RAG index: {self.index_name}")
#             self.RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
#             self._process_and_store_conversations()
#
#         # If the checksum has changed, update the index with new data
#         if self.current_checksum != self.last_processed_checksum:
#             logger.info("Detected changes in the conversation history, processing...")
#             self._process_and_store_conversations()
#             self._save_last_processed_checksum()
#
#     def _load_last_processed_checksum(self) -> Optional[str]:
#         checksum_file = self.persist_directory / "last_checksum.txt"
#         try:
#             return checksum_file.read_text().strip()
#         except FileNotFoundError:
#             return None
#
#     def _save_last_processed_checksum(self):
#         checksum_file = self.persist_directory / "last_checksum.txt"
#         checksum_file.write_text(self.current_checksum)
#
#     def _process_and_store_conversations(self):
#         my_documents = []
#         document_ids = []
#         document_metadatas = []
#
#         with open(self.json_file_path, "rb") as json_file:
#             for conversation in ijson.items(json_file, "item"):
#                 try:
#                     validated_conversation = Conversation(**conversation)
#                     for _, data in validated_conversation.mapping.items():
#                         validated_data = Data(**data)
#
#                         # Skip documents already indexed
#                         if validated_data.id in self.existing_document_ids:
#                             logger.info(f"Skipping existing document with ID: {validated_data.id}")
#                             continue
#
#                         if validated_data.message:
#                             document_text = ' '.join(part for part in validated_data.message.content.parts if part)
#                             my_documents.append(document_text)
#                             document_ids.append(validated_data.id)
#                             document_metadatas.append({
#                                 "id": validated_data.id,
#                                 "role": validated_data.message.author.role,
#                                 "title": validated_conversation.title
#                             })
#                             self.existing_document_ids.add(validated_data.id)
#
#                 except ValidationError as e:
#                     logger.error(f"Validation error: {e}")
#
#         if my_documents:
#             logger.info(f"Adding {len(my_documents)} new documents to the index.")
#             self.RAG.index(
#                 collection=my_documents,
#                 document_ids=document_ids,
#                 document_metadatas=document_metadatas,
#                 index_name=self.index_name,
#                 overwrite_index=False,
#                 split_documents=False,
#                 max_document_length=8190,
#                 use_faiss=True
#             )
#         # if my_documents:
#         #     logger.info(f"Adding {len(my_documents)} new documents to the index.")
#         #     self.RAG.add_to_index(
#         #         new_collection=my_documents,
#         #         new_document_ids=document_ids,
#         #         new_document_metadatas=document_metadatas,
#         #         index_name=self.index_name
#         #     )
#
#     def forward(self, query_or_queries: Union[str, List[str]], k: Optional[int] = None) -> list[dict]:
#         k = self.k if k is None else k
#
#         queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries
#         return self.RAG.search(queries, k=k)
#
#
# def main():
#     retriever = ChatGPTRAGRetriever()
#     query = "Retriever"
#     matched_results = retriever.forward(query, k=10)
#     for result in matched_results:
#         logger.info(result)
#
#
# if __name__ == "__main__":
#     main()
