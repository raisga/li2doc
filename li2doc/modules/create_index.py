import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from constants import (
    PERSIST_DIR,
)

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