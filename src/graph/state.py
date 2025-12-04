# State.py
from typing import List, TypedDict, Literal, Optional, Annotated
from pydantic import BaseModel, Field
from typing_extensions import NotRequired
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class ProductSpecs(TypedDict):
    category: str
    max_price: Optional[float]
    min_price: Optional[float]
    brand_preferences: List[str]
    use_cases: List[str]
    key_requirements: List[str]

class ProductReviewSummary(TypedDict):
    pros: List[str]
    cons: List[str]
    overall_sentiment: Literal["positive", "neutral", "negative"]

class Product_info(BaseModel):
    id: str = Field(description="Internal or source product id")
    name: str = Field(description="Name of the product")
    price: float = Field(description="Numeric price of the product")
    currency: Optional[str] = Field(
        default=None,
        description='Currency code should be "INR"'
    )
    rating: Optional[float] = Field(
        default=None,
        description="Average rating between 0 and 5"
    )
    rating_count: Optional[int] = Field(
        default=None,
        description="Number of ratings"
    )
    url: str = Field(description="Product page URL")
    image_url: Optional[str] = Field(
        default=None,
        description="Image URL of the product"
    )
    source: Optional[str] = Field(
        default=None,
        description='Source site, e.g. "amazon", "bestbuy"'
    )
    availability: Optional[str] = Field(
        default=None,
        description='Availability, e.g. "in_stock", "out_of_stock"'
    )
    snippet: Optional[str] = Field(
        default=None,
        description="Short description/snippet from search results"
    )
    review: ProductReviewSummary

class Product(BaseModel):
    products: List[Product_info]



class Choice(BaseModel):
    product_id: str
    product_name: str
    reason: str

class RecommendationItem(BaseModel):
    """
    Detailed recommendation entry for each product:
    - product details (id, name, price, etc.)
    - why it’s recommended
    - tradeoffs / downsides
    """
    product_id: str
    product_name: str
    price: Optional[float] = None
    currency: Optional[str] = None
    rating: Optional[float] = None
    source: Optional[str] = None
    url: Optional[str] = None

    why: str
    tradeoffs: str
class Recommendation(BaseModel):
    top_picks: List[str]
    recommendations: List[RecommendationItem]
    final_choice: Choice

class AgentState(TypedDict):
    user_query: str
    """
    I am adding NotRequired fields below to allow flexibility in the agent state as it progresses through different stages.
    """
    # Agent Outputs
    messages: NotRequired[Annotated[List[AnyMessage], add_messages]]
    product_specs: NotRequired[ProductSpecs]
    product_list: NotRequired[Product]

    # Final Aggregated Recommendation
    final_recommendation: NotRequired[Recommendation]

    # Control flags
    step: NotRequired[Literal[
        "specs_generation", 
        "product_search",
        "final_recommendation"]]
