from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

llm_openai = ChatOpenAI(
    model = "gpt-4.1",
    temperature= 0.1,
    api_key=os.getenv("OPENAI_API_KEY")

)

