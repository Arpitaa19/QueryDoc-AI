import os 
from chromadb.config import Settings

# ----------------------------------------------------------
# Author: Arpita
# GitHub: https://github.com/Arpitaa19/QueryDoc-AI
# Description: Generative AI-powered PDF Q&A App
# ----------------------------------------------------------

CHROMA_SETTINGS = Settings (
    chroma_db_impl = 'duckdb+parquet' ,
    persist_directory = "db" ,
    anonymized_telemetry = False 
)
