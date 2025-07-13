import os 
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFMinerLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# ----------------------------------------------------------
# Author: Ved Prakash Meena
# GitHub: https://github.com/Vedmeena21
# Description: Generative AI-powered PDF Q&A App
# ----------------------------------------------------------

CHROMA_SETTINGS = Settings (
    chroma_db_impl = 'duckdb+parquet' ,
    persist_directory = "db" ,
    anonymized_telemetry = False 
)

def main():
    # Use the full absolute path to the PDF file
    pdf_path = r"db\pdffortrain.pdf"
    
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print("File not found:", pdf_path)
        return

    # Load the PDF document
    loader = PDFMinerLoader(pdf_path)
    documents = loader.load()

    # Split the document into manageable text chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Create embeddings for the text chunks
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(texts, embeddings, persist_directory="db")

    # Persist the database to disk
    db.persist()
    print("Processing complete.")

if __name__ == "__main__":
    main()