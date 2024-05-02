import asyncio
import nest_asyncio
nest_asyncio.apply()

from modules.config_llm import config_llm
from modules.create_index import create_index
from modules.generate_doc import generate_doc
from modules.get_query_engine import get_query_engine
from modules.get_response import get_response
from modules.load_documents import load_documents

async def app() -> None:
    print("\n~~ 🔧 CONFIGURE MODEL ~~")
    config_llm()
    print("\n~~ 💿 LOAD FILES ~~")
    documents = load_documents()
    print("\n~~ 📝 CREATE INDEX ~~")
    index = create_index(documents)
    print("\n~~ ⌛️ RUN QUERY ~~")
    query_engine = get_query_engine(index)
    print("\n~~ 💬 GET RESPONSE ~~")
    response = get_response(query_engine)
    print("\n~~ 💾 GENERATE DOC ~~")
    generate_doc(response)
    return None

asyncio.run(app())
