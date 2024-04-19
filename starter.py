import os.path
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.ollama import Ollama
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)

PERSIST_DIR = "./storage"
FILES_DIR = "./files"

MODEL_NAME = "mistral"
MODEL_EMBED = "local:BAAI/bge-small-en-v1.5"
QUERY_VALUE = "Who is Prince?"

documents = SimpleDirectoryReader(FILES_DIR).load_data()

Settings.embed_model = resolve_embed_model(MODEL_EMBED)
Settings.llm = Ollama(model=MODEL_NAME, request_timeout=30.0)

index = VectorStoreIndex.from_documents(
    documents,
)
index.storage_context.persist()

# check if storage already exists
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader(FILES_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query(QUERY_VALUE)
print(response)