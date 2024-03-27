import os

from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from dspygen.utils.file_tools import data_dir


# from utils.chroma_memstore import ChromaMemStore


# def get_mem_store():
#     return ChromaMemStore(mem_store_path)


def get_session():
    DATABASE_URL = f"sqlite:///{data_dir('dev.db')}"

    engine = create_engine(DATABASE_URL)

    SQLModel.metadata.create_all(engine)

    return Session(engine)
