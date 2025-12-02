#Combine_results.py

from typing import cast
from src.graph.state import AgentState, ProductSpecs, Product, Recommendation
from src.llm.llm_openai import llm_openai
from langchain_core.messages import SystemMessage, HumanMessage


# LLM configured to output `Recommendation` model
llm_reco_structured = llm_openai.with_structured_output(Recommendation)

# First we need to convert the dictionary in to natural language format.
def _format_specs(specs: ProductSpecs) -> str:
    return (
        f"Category: {specs.get('category')}\n"
        f"Max price: {specs.get('max_price')}\n"
        f"Min price: {specs.get('min_price')}\n"
        f"Brand preferences: {', '.join(specs.get('brand_preferences', []))}\n"
        f"Use cases: {', '.join(specs.get('use_cases', []))}\n"
        f"Key requirements: {', '.join(specs.get('key_requirements', []))}"
    )

def _format_products(product_list: Product) -> str:
    """
    Turn the structured Product list into a readable text block
    that the LLM can reason over.
    """
    lines = []
    for idx, p in enumerate(product_list.products, start=1):
        review = p.review or {}
        pros = review.get("pros", [])
        cons = review.get("cons", [])
        overall = review.get("overall_sentiment")

        lines.append(
            f"{idx}. {p.name}\n"
            f"   - id: {p.id}\n"
            f"   - price: {p.price} {p.currency or ''}\n"
            f"   - rating: {p.rating} (from {p.rating_count} reviews) if available\n"
            f"   - source: {p.source or 'unknown'}\n"
            f"   - availability: {p.availability or 'unknown'}\n"
            f"   - url: {p.url}\n"
            f"   - snippet: {p.snippet or 'N/A'}\n"
            f"   - review pros: {', '.join(pros) if pros else 'N/A'}\n"
            f"   - review cons: {', '.join(cons) if cons else 'N/A'}\n"
            f"   - overall sentiment: {overall or 'N/A'}\n"
        )

    return "\n".join(lines)


def comb_results(state: AgentState) -> AgentState:
    """
    Combine extracted specs + product list into a final recommendation
    text stored in state["final_recommendation"].
    """
    state["step"] = "final_recommendation"

    specs = cast(ProductSpecs, state.get("product_specs"))  # type: ignore
    product_list = cast(Product, state.get("product_list"))  # type: ignore

    # Safety: if search failed / returned nothing
    if not specs or not product_list or not getattr(product_list, "products", []):
        state["final_recommendation"] = (
            "I couldn't find any suitable products based on the current state. "
            "You may want to adjust the query or try again."
        )
        return state

    specs_text = _format_specs(specs)
    products_text = _format_products(product_list)

    system_prompt = SystemMessage(
        content=(
            "You are an expert product recommendation assistant.\n"
            "You are given:\n"
            "1) The user's desired specifications\n"
            "2) A shortlist of candidate products with price, rating, snippet, and review summaries\n\n"
            "Your job:\n"
            "- Compare the products strictly against the user's specs\n"
            "- Prioritize fit to use-cases and key requirements first, then price, then ratings\n"
            "- Select the top 1–3 products\n"
            "- Explain *why* they match the user’s needs\n"
            "- Mention trade-offs when relevant\n"
            "- End with a clear final recommendation and optional alternatives.\n"
            "Respond in concise markdown."
        )
    )

    human_message = HumanMessage(
        content=(
            "Here are the user specifications:\n"
            "-------------------------------\n"
            f"{specs_text}\n\n"
            "Here is the product shortlist:\n"
            "------------------------------\n"
            f"{products_text}\n\n"
            "Please provide the final recommendations now."
        )
    )

    response = llm_reco_structured.invoke([system_prompt, human_message])

    state["final_recommendation"] = response
    return state