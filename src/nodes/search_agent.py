# Search Agent .py

from src.graph.state import AgentState, Product
from src.llm.llm_openai import llm_openai
from langchain_core.messages import SystemMessage, HumanMessage
from src.tools.exa_tool import exa_tool
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

tools =[exa_tool]
llm_search_tool = llm_openai.bind_tools(tools)
llm_structured_output = llm_openai.with_structured_output(Product)

# For structured Output i am using the  Full Proof strategy. Using one more node to parse the output into the desired format.
def product_list(state: AgentState):
    """Parsing the product list into structured format"""
    messages = state["messages"]
    response = llm_structured_output.invoke(messages)
    return {"product_list": response}

# It will be a react agent that uses exa tool to search products based on specifications
def search_agent(state: AgentState):

    state["step"] = "product_search"
    spec = state["product_specs"]
    msg = state.get("messages", [])
    if not msg:
        system_prompt = SystemMessage(content=
        "You are a web search agent that helps find products based on user specifications." \
        "You have exa websearch as a tool to find the relevent 5 products" \
        "Use tools only when necessary. When you have enough info, stop calling tools." \
        "NOTE: Once you have identified a shortlist of products that satisfy the specifications, stop calling tools, summarize the best options in natural language, and do not request further tool calls."
                                    )
    
        human_message = HumanMessage(content=(
            f"Category: {spec['category']}\n"
            f"Max price: {spec['max_price']}\n"
            f"Min price: {spec['min_price']}\n"
            f"Brand preferences: {', '.join(spec['brand_preferences'])}\n"
            f"Use cases: {', '.join(spec['use_cases'])}\n"
            f"Key requirements: {', '.join(spec['key_requirements'])}"
        ))

        msg = [system_prompt, human_message]

    # using previous messages and new instructions
    
    response = llm_search_tool.invoke(msg)

    return {"messages": msg + [response]}

def route_after_search(state:AgentState):
    """It will decide wheather to call tools again or proceed to product listing"""
    dest = tools_condition(state)
    if dest == "__end__":
        return "product_list"
    return dest

graph = StateGraph(AgentState)

graph.add_node("search_agent", search_agent)
graph.add_node("tools", ToolNode(tools = tools))
graph.add_node("product_list", product_list)

graph.add_edge(START, "search_agent")

graph.add_conditional_edges(
    "search_agent",
     route_after_search,
      {
          "tools":"tools",
          "product_list": "product_list"
      },
        )
graph.add_edge("tools", "search_agent")
graph.add_edge("product_list", END)

app = graph.compile()


if __name__ == "__main__":
    test_state: AgentState = {
        "user_query": "Lightweight laptop for programming under $1200",
        "product_specs": {
            "brand_preferences": ["Dell", "Lenovo"],
            "category": "laptop",
            "key_requirements": ["lightweight"],
            "max_price": 1200,
            "min_price": 0,
            "use_cases": ["programming"],
        },
        "messages":[]
    }


    result = app.invoke(test_state)

    print("Structured Output:\n", result["product_list"])


# from IPython.display import Image


# png_bytes = app.get_graph().draw_mermaid_png()

# # Save to file
# with open("search_agent.png", "wb") as f:
#     f.write(png_bytes)

# print("Saved as graph.png")