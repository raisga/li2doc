from llama_index.core import (
    VectorStoreIndex,
    get_response_synthesizer,
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from constants import (
    SIMILARITY_TOP_K,
    RESPONSE_MODE,
)

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
