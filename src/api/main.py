from fastapi import FastAPI
from src.graph.main_graph import build_graph
from pydantic import BaseModel

# Initializing the graph
graph = build_graph()


# Initializing the API
app = FastAPI(
    title="VECTOR",
    description="Product Search Agent")

# defining the type of input
class InputQuery(BaseModel):
    user : str
    currency: str = "USD"

@app.post("/USER", tags=["User Input"])
def user_query(state: InputQuery):
    initial_state = {
        "user_query": state.user,
        "currency": state.currency,
        # optional; only if your search_agent uses it
        "messages": [],
    }
    response = graph.invoke(initial_state)
    return {
        "product_list": response.get("product_list"),
        "final_recommendation": response.get("final_recommendation"),
    }