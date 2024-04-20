# ======================================================================================================
# DEPENDENCIES

import os.path
from llama_index.core.embeddings import resolve_embed_model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)

# ======================================================================================================
# CONSTANTS

# Directory where files are located
INPUT_DIR = "./files"
# Supported files extensions
REQUIRED_EXTS = [
    ".pdf",
    ".doc",
    ".docx",
    # ".xls",
    # ".xlsx",
    # ^ ! TEST first before enabling
    ".csv",
    ".html"
]
# Index storage
PERSIST_DIR = "./storage"
# Model configuration
MODEL="llama3"
MODEL_EMBED="BAAI/bge-small-en-v1.5"
REQUEST_TIMEOUT=60.0
# Query value
QUERY_VALUE = "Given the data provided, find an operating scissors with a mirror finish, and show me the dimensions of it. Give me the filename and page number of the document where you found the info."

# ======================================================================================================
# MAIN

# 1 - Configure model
Settings.llm = Ollama(model=MODEL, request_timeout=REQUEST_TIMEOUT)
Settings.embed_model = resolve_embed_model(HuggingFaceEmbedding(
    model_name=MODEL_EMBED
))

# 2 - Load documents data
documents = SimpleDirectoryReader(
    input_dir=INPUT_DIR,
    required_exts=REQUIRED_EXTS,
    recursive=True,
).load_data()

# 3 - Creates index storage from documents data chunks
index = VectorStoreIndex.from_documents(
    documents,
)
index.storage_context.persist()

# 4a - Check if index storage already exists
if not os.path.exists(PERSIST_DIR):
    # 4a1 - Load the documents and create the index
    documents = SimpleDirectoryReader(INPUT_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # 4a2 - Store data to be used for later user
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # 4b - Load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# 5 - Runs custom query
query_engine = index.as_query_engine()
response = query_engine.query(QUERY_VALUE)

# 6 - Prints response
print(response)