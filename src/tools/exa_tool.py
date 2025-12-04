from exa_py import Exa
import os
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv(override=True)

exa = Exa(os.getenv("EXA_API_KEY"))

@tool("exa_search")
def exa_tool(query:str):
    """
    The function helps in searching the web
    """
    result = exa.search_and_contents(
    query=query,
    context = True,
    type = "auto",
    user_location = "IN",
    num_results = 5,
    )
    return result


