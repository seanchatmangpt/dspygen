import dspy

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader
import re


def clean_text(text):
    return re.sub('<.*?>|\xa0+|\s+|\{\'.*?\.xhtml\'\}|\'.*?\.xhtml\'', ' ', text).strip()


def extract_texts_from_epub(file_name):
    book = epub.read_epub(file_name)
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

    def chapter_to_str(chapter):
        soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
        text = [para.get_text() for para in soup.find_all('p')]
        return clean_text(' '.join(text))

    texts = {}
    for item in items:
        texts[item.get_name()] = chapter_to_str(item)
    return texts


def read_text_from_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ''
    return clean_text(text)


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return clean_text(file.read())


def read_docx_file(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return clean_text('\n'.join(full_text))


def read_any(file_path):
    if file_path.endswith('.epub'):
        return extract_texts_from_epub(file_path)
    elif file_path.endswith('.pdf'):
        return read_text_from_pdf(file_path)
    elif file_path.endswith('.txt') or file_path.endswith('.md'):
        return read_text_file(file_path)
    elif file_path.endswith('.docx'):
        return read_docx_file(file_path)
    else:
        # Treat unknown file types as plaintext
        try:
            return read_text_file(file_path)
        except Exception as e:
            raise ValueError(f"Failed to process {file_path}: {e}")


class DocRetriever(dspy.Retrieve):
    def __init__(self, path, **kwargs):
        # Read the file from any acceptable text file type
        super().__init__()
        self.path = path

    def read_chunks(self, chunk_chars):
        text = read_any(self.path)
        return [text[i:i + chunk_chars] for i in range(0, len(text), chunk_chars)]

    def forward(self, chunk_chars=None, **kwargs) -> str | list[str]:
        if chunk_chars:
            return self.read_chunks(chunk_chars)

        return read_any(self.path)


def main():
    drt = DocRetriever(path="/Users/candacechatman/Downloads/consulting-contract.pdf")
    print(drt.forward())

    # from dspygen.utils.file_tools import tmp_file

    # with tmp_file("Hello, world!") as tmp_path:
    #     rm = DocRetriever(path=tmp_path)
    #     print(rm.forward())


if __name__ == '__main__':
    main()
