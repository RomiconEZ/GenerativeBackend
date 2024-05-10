from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

#EMBEDDING_MODEL_NAME = "sentence-transformers/multi-qa-mpnet-base-dot-v1" # альтернатива
EMBEDDING_MODEL_NAME = 'intfloat/multilingual-e5-large-instruct'


def init_vector_db(filename: str):
    global EMBEDDING_MODEL_NAME
    # Инициализация и загрузка документов
    current_path = Path(__file__).parent.parent
    loaders = [PyPDFLoader(str(current_path / f"RAG_Document/{filename}.pdf"))]

    docs = []
    for file in loaders:
        docs.extend(file.load())  # Загрузка текста из PDF-файлов

    # Разбиение текста на части
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=300)
    docs = text_splitter.split_documents(docs)

    # Создание векторного представления текста
    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )
    vectorstore = Chroma.from_documents(
        docs, embedding_function, persist_directory=f"./chroma_db_{filename}"
    )

    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )
    vector_db = Chroma(
        persist_directory=f"./chroma_db_{filename}", embedding_function=embedding_function
    )

    return vector_db, vectorstore
