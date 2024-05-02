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

