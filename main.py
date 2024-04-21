# ======================================================================================================
# DEPENDENCIES

import asyncio
import os.path
import nest_asyncio

nest_asyncio.apply()

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.core.embeddings import resolve_embed_model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
# from openai import AsyncOpenAI

# ======================================================================================================
# CONSTANTS

# Directory where files are located
INPUT_DIR = "./files"
# Supported files extensions
REQUIRED_EXTS = [
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".csv",
    ".html"
]
# Index storage
PERSIST_DIR = "./storage"
# Model configuration
MODEL="llama3"
MODEL_EMBED="BAAI/bge-large-en-v1.5"
REQUEST_TIMEOUT=60.0
# Queries values
SIMILARITY_TOP_K=3
RESPONSE_MODE="tree_summarize"
QUERY_PROMPT="Given the data provided, please sumarize the content. Show the summary, and sign with: 🐸"

# ======================================================================================================
# SCRIPT
def config_llm() -> None:
    print("> Configure the LLM")
    Settings.llm = Ollama(
        model=MODEL,
        request_timeout=REQUEST_TIMEOUT
    )
    Settings.embed_model = resolve_embed_model(
        HuggingFaceEmbedding(
            model_name=MODEL_EMBED
        )
    )

    # gets API Key from environment variable OPENAI_API_KEY
    # client = AsyncOpenAI(
    #     base_url="http://localhost:3928/v1/",
    #     api_key="sk-xxx"
    # )
    print(f" - model={MODEL}\n"
        f" - request_timeout={REQUEST_TIMEOUT}\n"
        f" - model_name={MODEL_EMBED}"
    )

def load_documents() -> SimpleDirectoryReader:
    print("> Load documents data")
    documents = SimpleDirectoryReader(
        input_dir=INPUT_DIR,
        required_exts=REQUIRED_EXTS,
        recursive=True,
    ).load_data()
    print(f"input_dir={INPUT_DIR}\n"
        f"required_exts={REQUIRED_EXTS}"
    )
    for d in documents:
        print(f"file found: {d.metadata["file_name"]}")
    return documents

def create_index(documents: SimpleDirectoryReader) -> VectorStoreIndex:
    print("> Check if index storage already exists")
    if not os.path.exists(PERSIST_DIR):
        # print("> Load the documents and create the index")
        # documents = SimpleDirectoryReader(INPUT_DIR).load_data()
        print("> Creates index storage from documents data chunks")
        index = VectorStoreIndex.from_documents(documents)
        print("> Store data to be used for later use")
        index.storage_context.persist(
            persist_dir=PERSIST_DIR
        )
    else:
        print("> Load the existing index")
        storage_context = StorageContext.from_defaults(
            persist_dir=PERSIST_DIR
        )
        index = load_index_from_storage(storage_context)
    return index

def get_query_engine(index: VectorStoreIndex) -> VectorStoreIndex.BaseQueryEngine:
    print("> Runs query with custom vars")
    query_engine = index.as_query_engine(
        similarity_top_k=SIMILARITY_TOP_K,
        response_mode=RESPONSE_MODE
    )
    return query_engine

def get_response(query_engine: VectorStoreIndex.BaseQueryEngine) -> str:
    print("> Gets response from query prompt")
    response = query_engine.query(QUERY_PROMPT)
    print("\n\n\n")

    return response

# MAIN
# -------------------------------------------------------------------------------------------------------
async def main() -> None:
    # 1 - Configure model
    print("\n~~ 🔧 CONFIGURE MODEL ~~")
    config_llm()
    # 2 - Load files
    print("\n~~ 💿 LOAD FILES ~~")
    documents = load_documents()
    # 3 - Create index
    print("\n~~ 📝 CREATE INDEX ~~")
    index = create_index(documents)
    # 4 - Runs query with custom vars
    print("\n~~ ⌛️ RUN QUERY ~~")
    query_engine = get_query_engine(index)
    # 5 - Gets response from query prompt
    print("\n~~ 💬 GET RESPONSE ~~")
    response = get_response(query_engine)
    print(response)
    return None

asyncio.run(main())
