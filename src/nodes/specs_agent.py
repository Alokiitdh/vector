from src.graph.state import AgentState, ProductSpecs
from src.llm.llm_groq import llm_groq
from langchain_core.messages import SystemMessage


# We are using langchain wrapper for structured output.
llm_product_spec = llm_groq.with_structured_output(ProductSpecs)

def specs_agent(state: AgentState):
    """Extracting the User expecatations from the query"""
    user_query = state['user_query']
    system_prompt = SystemMessage(content="you are an expert specification extraction agent from user query." \
    "you have to extract the following:" \
    "1. Category" \
    "2. max_price" \
    "3. min_price" \
    "4. brand_preferences" \
    "5. use cases" \
    "6. Key requirements")
    response = llm_product_spec.invoke([system_prompt, user_query])
    state["product_specs"] = response
    
    return state["product_specs"]

if __name__ == "__main__":
    test_state: AgentState = {
        "user_query": "I want a lightweight laptop under $1200 for programming. Prefer Dell or Lenovo."
    }

    result = specs_agent(test_state)

    print("Structured Output:\n", result)


    