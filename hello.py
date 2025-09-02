import os
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
import PyPDF2

embeddings = OllamaEmbeddings(model="all-minilm:33m")
current_directory = os.path.dirname(os.path.abspath(__file__))
vector_directory = os.path.join(current_directory, "db", "chroma_db_physics")

def pdf_text_loader(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

def store_in_vector_store(docs):
    # Initialize Chroma and store the documents
    vector_store = Chroma.from_documents(
        collection_name="physics", 
        documents=docs, 
        embedding=embeddings, 
        persist_directory=vector_directory
    )
    vector_store.persist()  # Save the vectors to disk
    print("Documents have been stored in the vector store.")

def create_chunks(texts):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.create_documents(texts)


if __name__ == "__main__":
    pdf_text = pdf_text_loader("physics_notes.pdf")
    docs = create_chunks(pdf_text)
    store_in_vector_store(docs)