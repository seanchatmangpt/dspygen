import json
import os
import zipfile
from pathlib import Path

import ijson

from dspygen.rm.chatgpt_chromadb_retriever import Conversation, Author, ContentPart, Message, Data

from dspygen.utils.file_tools import data_dir

logs_dir = data_dir() / f"chatgpt_logs"


def unzip_recent():
    """Main function"""
    # Open most recent zip file in downloads folder
    # Replace this with your downloads directory path
    downloads_dir = Path.home() / "Downloads"

    # Find all zip files in the downloads directory
    zip_files = list(downloads_dir.glob("*.zip"))

    # Sort the zip files by modification time, latest first
    zip_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # Get the most recent zip file
    latest_zip = zip_files[0]
    print(f"Most recent ZIP file: {latest_zip}")

    # Create a directory to extract the contents
    extract_dir = data_dir() / f"chatgpt_logs"
    extract_dir.mkdir(exist_ok=True)

    # Extract the contents of the zip file
    with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"Extracted contents to: {extract_dir}")


def main():
    # Load the conversation data
    json_file_path = logs_dir / "conversations.json"

    with open(json_file_path, "rb") as f:
        for convo in ijson.items(f, "item"):
            conversation = Conversation(**convo)
            print(conversation.title)
            for key, value in conversation.mapping.items():
                print(f"{key}: {value}")
            print()




if __name__ == '__main__':
    # unzip_recent()
    main()
