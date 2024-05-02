from llama_index.core.query_engine import RetrieverQueryEngine
from constants import (
    QUERY_PROMPT,
)

def get_response(query_engine: RetrieverQueryEngine) -> str:
    print("> Gets response from query prompt")
    response = query_engine.query(
        str_or_query_bundle=QUERY_PROMPT
    )
    print("\n<<<< START RESPONSE >>>>\n")
    response.print_response_stream()
    print("\n<<<< END RESPONSE >>>>\n")
    return response.response_txt
