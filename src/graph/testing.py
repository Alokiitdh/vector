from src.graph.main_graph import build_graph
from IPython.display import Image


app = build_graph()
png_bytes = app.get_graph().draw_mermaid_png()

# Save to file
with open("graph_1.png", "wb") as f:
    f.write(png_bytes)

print("Saved as graph.png")



