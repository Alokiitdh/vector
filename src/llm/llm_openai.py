from langchain_openai import ChatOpenAI

llm_openai = ChatOpenAI(
    model = "gpt-4.1",
    temperature= 0.1
)