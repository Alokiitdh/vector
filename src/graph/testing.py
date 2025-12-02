from src.graph.main_graph import build_graph
# from IPython.display import Image

if __name__ == "__main__":
    app = build_graph()

    initial_state = {
        "user_query": "Motorbike for daily compute",
        # optional; only if your search_agent uses it
        "messages": [],
    }

    final_state = app.invoke(initial_state)

    print("\n=== FINAL STATE ===")
    print("Specs:\n", final_state.get("product_specs"))
    print("\nProduct list:\n", final_state.get("product_list"))
    print("\nFinal recommendation:\n", final_state.get("final_recommendation"))

# app = build_graph()
# png_bytes = app.get_graph().draw_mermaid_png()

# # Save to file
# with open("main_graph.png", "wb") as f:
#     f.write(png_bytes)

# print("Saved as graph.png")



