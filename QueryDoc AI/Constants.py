import os 
from chromadb.config import Settings

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
