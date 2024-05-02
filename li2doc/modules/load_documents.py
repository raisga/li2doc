from llama_index.core import (
    SimpleDirectoryReader,
)
from constants import (
    INPUT_DIR,
    REQUIRED_EXTS,
)

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
