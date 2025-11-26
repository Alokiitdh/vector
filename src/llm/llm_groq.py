from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv(override=True)

llm_groq = ChatGroq(
        groq_api_key= os.environ["GROQ_API_KEY"],
        model="openai/gpt-oss-120b",  # Can be replace with our preferred model
        temperature=0.1
    )

# result = llm.invoke("Tell me about Groq and its AI accelerators.")
# print(result)