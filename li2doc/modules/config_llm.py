from llama_index.core import (
    Settings,
)
from llama_index.core.embeddings import resolve_embed_model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from constants import (
    MODEL,
    MODEL_EMBED,
    REQUEST_TIMEOUT
)


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
    print(f" - model={MODEL}\n"
        f" - request_timeout={REQUEST_TIMEOUT}\n"
        f" - model_name={MODEL_EMBED}"
    )
    return None
