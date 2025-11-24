
from typing import List, TypedDict, Literal, Optional

class ProductSpecs(TypedDict):
    category: str
    max_price: Optional[float]
    min_price: Optional[float]
    brand_preferences: List[str]
    use_cases: List[str]
    key_requirements: List[str]


class Product(TypedDict):
    id: str
    name: str
    price: float
    ratings: float
    url: str

class ProductReviewSummary(TypedDict):
    product_id: str
    pros: List[str]
    cons: List[str]
    overall_sentiment: Literal["positive", "neutral", "negative"]

class AgentState(TypedDict):
    user_query: str

    # Agent Outputs
    product_specs: ProductSpecs
    product_list: List[Product]
    product_review: List[ProductReviewSummary]

    # Final Aggregated Recommendation
    final_recommendation: str

    # Control flags
    step:Literal["specs_generation", "product_search", "review_analysis", "final_recommendation"]
