from langchain_community.vectorstores import SQLiteVec
from langchain_huggingface import HuggingFaceEmbeddings

import sqlite3
import sqlite_vec

import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vec.db')

# Initialize the embeddings
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cuda'}    
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Create Vector store database 
db = sqlite3.connect(db_path, check_same_thread=False) # No thread check since expecting one user

db.row_factory = sqlite3.Row
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

# TODO add a timestamp
# Initalize the vectorstore
vector_store = SQLiteVec(
    table="chunks", db_file=db_path, embedding=hf,
    connection=db
)

def clear_db():

    print("\n\nClearing the database . . . \n")

    # Get the names of all the tables in the database
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Delete rows from each table
    for table in tables:
        table_name = table[0]
        # Skip system tables or any table you don't want to clear
        if table_name != "sqlite_sequence" and not '_vec_info' in table_name and not '_vec_vector_chunks00' in table_name: 
            cursor.execute(f"DELETE FROM {table_name};")

    # Commit changes
    db.commit()
