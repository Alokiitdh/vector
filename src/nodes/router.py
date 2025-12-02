# src/nodes/router.py
from src.graph.state import AgentState

def router_node(state: AgentState) -> AgentState:
    """
    Actual node in the graph.

    It can be a pure pass-through node (no-op),
    or you can set flags / logging here if you want.
    But it MUST return a dict (the updated state).
    """
    # Example: you might track that routing happened
    # state["step"] = state.get("step", "routing")
    return state

def router_steps(state: AgentState)-> AgentState:
    """
    Decides the next node based on the current state
    """
    print("ROUTER STEP:", state.get("step"),
          "has_specs:", bool(state.get("product_specs")),
          "has_products:", bool(state.get("product_list")),
          "has_final:", bool(state.get("final_recommendation")))
    
    #step 1: Extracting the Specs from the suer query
    if "product_specs" not in state:
        return "specs_agent"
    
    #step 2: Now we have the product specifications, we have to proceed to the search agent
    if "product_list" not in state:
        return "search_agent"
    
    #step 3: Now we have the procucts list, lets combine and give the final reccomndadyions
    if "final_recommendation" not in state:
        return "comb_results"
    
    # Finally when all the steps are done we can end thge Graph
    return "__end__"