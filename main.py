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
    get_response_synthesizer,
    Settings
)
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
# from openai import AsyncOpenAI
from fpdf import FPDF

# ======================================================================================================
# CONSTANTS

# Output doc filename
DOC_FILENAME = "output.pdf"
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
MODEL="llama2"
MODEL_EMBED="BAAI/bge-large-en-v1.5"
REQUEST_TIMEOUT=60.0
# Queries values
SIMILARITY_TOP_K=2
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
    return None

def load_documents() -> SimpleDirectoryReader:
    print("> Load documents data")
    documents = SimpleDirectoryReader(
        input_dir=INPUT_DIR,
        required_exts=REQUIRED_EXTS,
        recursive=True,
    ).load_data()
    print(f" - input_dir={INPUT_DIR}\n"
        f" - required_exts={REQUIRED_EXTS}"
    )
    for d in documents:
        print(f" - file found: {d.metadata["file_name"]}")
    return documents

def create_index(documents: SimpleDirectoryReader) -> VectorStoreIndex:
    print("> Check if index storage already exists")
    if not os.path.exists(PERSIST_DIR):
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

def get_query_engine(index: VectorStoreIndex) -> RetrieverQueryEngine:
    print("> Configure retriever")
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=SIMILARITY_TOP_K,
    )
    print(f" - similarity_top_k={SIMILARITY_TOP_K}")
    print("> Configure response synthesizer")
    response_synthesizer = get_response_synthesizer(
        streaming=True,
        response_mode=RESPONSE_MODE,
    )
    print(f" - response_mode={RESPONSE_MODE}")
    print("> Assemble query engine ")
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )
    return query_engine

def get_response(query_engine: RetrieverQueryEngine) -> str:
    print("> Gets response from query prompt")
    response = query_engine.query(
        str_or_query_bundle=QUERY_PROMPT
    )
    print("\n<<<< START RESPONSE >>>>\n")
    response.print_response_stream()
    print("\n<<<< END RESPONSE >>>>\n")
    return response.response_txt

def generate_doc(response: str) -> None:
    print("> Generate document from response")
    format_response = response.encode('latin-1', 'replace').decode('latin-1')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(text=format_response)
    pdf.output(DOC_FILENAME)
    return None

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
    # 6 - Generate document from response
    print("\n~~ 💾 GENERATE DOC ~~")
    generate_doc(response)
    return None

asyncio.run(main())
