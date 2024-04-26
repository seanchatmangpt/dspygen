import ijson

from dspygen.rm.chatgpt_chromadb_retriever import Conversation, Data
from dspygen.utils.file_tools import data_dir


def _process_and_store_conversations(match):
    with open(data_dir("conversations.json"), "rb") as json_file:
        for conversation in ijson.items(json_file, "item"):
            try:
                validated_conversation = Conversation(**conversation)
                for _, data in validated_conversation.mapping.items():
                    validated_data = Data(**data)
                    if validated_data.message:
                        document_text = ' '.join(part for part in validated_data.message.content.parts if part)
                        if match in document_text and validated_data.author.role == "assistant":
                            with open(match + ".txt", "a") as file:
                                file.write(document_text + "\n")
            except Exception as e:
                continue


def main():
    """Main function"""
    match = "Retriever"
    _process_and_store_conversations(match)


if __name__ == '__main__':
    main()

