from langgraph.graph import StateGraph, START, END
from src.graph.state import AgentState
from src.nodes.router import router
from src.nodes.specs_agent import specs_agent
from src.nodes.search_agent import search_agent
from src.nodes.review_agent import review_agent
from src.nodes.combine_results import comb_results

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router)
    graph.add_node("specs_agent", specs_agent)
    graph.add_node("search_agent", search_agent)
    graph.add_node("review_agent", review_agent)
    graph.add_node("comb_results", comb_results)

    # Router is the fist node
    graph.add_edge(START, "router")

    # After riuter, we can fanout in parallerl to three agents
    # langgraph parallelism is driven by "updates" to the three shared states
    # When multiple nodes are reachable from the same previous node,
    # they can run in parallel, depending on the executor.
    graph.add_edge("router", "specs_agent")
    graph.add_edge("router", "search_agent")
    graph.add_edge("router", "review_agent")

    graph.add_edge("specs_agent", "comb_results")
    graph.add_edge("search_agent", "comb_results")
    graph.add_edge("review_agent", "comb_results")

    graph.add_edge("comb_results", END)

    app = graph.compile()
    return app




