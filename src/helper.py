
from langchain.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings

# load the pdf or the data
def extract_pdf_files(data_path):
    loader=DirectoryLoader(
        data_path,glob="*.pdf",loader_cls=PyPDFLoader
    )
    
    documents=loader.load()
    return documents


def filter_extracted_data(docs):
    
    filtered_docs=[]
    for doc in docs:
        src=doc.metadata.get('source')
        filtered_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={'source':src}
            )
        )
    
    return filtered_docs

def text_splitter(data):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    chunked_text=text_splitter.split_documents(data)
    return chunked_text

def download_embedding_model():
    """
    Download the model and return the hugging face embedddings
    """
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    embeddings=HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings

