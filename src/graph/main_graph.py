# main_graph.py

from langgraph.graph import StateGraph, START, END
from src.graph.state import AgentState
from src.nodes.router import router_node, router_steps
from src.nodes.specs_agent import specs_agent
from src.nodes.search_agent import app as search_graph_app
from src.nodes.combine_results import comb_results


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("specs_agent", specs_agent)
    graph.add_node("search_agent", search_graph_app)
    graph.add_node("comb_results", comb_results)

    # Router is the fist node
    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        router_steps, # This function will return one of the keys below
        {
            "specs_agent": "specs_agent",
            "search_agent": "search_agent",
            "comb_results": "comb_results",
            "__end__": END,
        }
    )
    graph.add_edge("specs_agent", "router")
    graph.add_edge("search_agent", "router")

    graph.add_edge("comb_results", END)

    app = graph.compile()
    return app


