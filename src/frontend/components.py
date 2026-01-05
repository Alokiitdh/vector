# components.py

"""
Streamlit components and utilities for the VECTOR frontend
"""

import streamlit as st
from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class VectorUI:
    """UI components for the VECTOR application"""
    
    @staticmethod
    def get_currency_symbol(code: str) -> str:
        symbols = {"USD": "$", "INR": "₹", "EUR": "€", "GBP": "£"}
        return symbols.get(code.upper(), "$")
    
    @staticmethod
    def setup_page_config():
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="VECTOR - Product Research Agent",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @staticmethod
    def load_custom_css():
        """Load custom CSS for styling"""
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1e88e5;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .product-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            background-color: #f9f9f9;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .recommendation-box {
            background-color: #e8f5e8;
            border-left: 5px solid #4caf50;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }
        
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .price-tag {
            background-color: #4caf50;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-weight: bold;
            display: inline-block;
        }
        
        .rating-stars {
            color: #ffd700;
            font-size: 1.2rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render the main header"""
        st.markdown('<h1 class="main-header">🔍 VECTOR</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-Powered Product Research Agent</p>', unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar() -> str:
        """Render the sidebar with configuration and examples WITHOUT allowing API modification."""
        
        FIXED_API_URL = "http://localhost:8000/USER"   # <-- Hard-coded, cannot be changed

        with st.sidebar:
            # st.header("⚙️ API Configuration")
            # st.write("The API endpoint used by the app:")
            # st.code(FIXED_API_URL)  # read-only display

            st.header("⚙️ Configuration")
            currency = st.selectbox(
                "Preferred Currency",
                ["USD", "INR", "EUR", "GBP"],
                index=0
            )

            st.header("📝 How to use")
            st.write(
                """
            1. **Enter your query**: Be specific about what you're looking for  
            2. **Include details**: Budget, brand preferences, use cases  
            3. **Search**: Click *Search Products*  
            4. **Review**: Analyze AI recommendations  
            """
            )

            st.header("💡 Example Queries")
            examples = [
                "Lightweight laptop under 120000rs for programming",
                "Gaming headset under 20000rs with noise cancellation",
            ]

            for i, example in enumerate(examples):
                if st.button(f"📝 Use this example", key=f"example_{i}"):
                    st.session_state.query = example
                st.caption(example)
                st.write("---")

            return FIXED_API_URL, currency

    
    @staticmethod
    def create_price_comparison_chart(products: List[Dict]) -> go.Figure:
        """Create a price comparison chart"""
        if not products:
            return None
        
        names = [p.get('name', 'Unknown')[:20] + '...' if len(p.get('name', '')) > 20 
                else p.get('name', 'Unknown') for p in products]
        prices = [p.get('price', 0) if p.get('price') is not None else 0 for p in products]
        ratings = [p.get('rating', 0) if p.get('rating') is not None else 0 for p in products]
        
        # Ensure we have valid prices for scaling
        max_price = max(prices) if prices and max(prices) > 0 else 1
        
        fig = go.Figure()
        
        # Add price bars
        fig.add_trace(go.Bar(
            name='Price',
            x=names,
            y=prices,
            marker_color='lightblue',
            yaxis='y',
            offsetgroup=1
        ))
        
        # Add rating line
        fig.add_trace(go.Scatter(
            name='Rating',
            x=names,
            y=[(r if r is not None else 0) * max_price / 5 for r in ratings],  # Scale ratings to price range
            mode='lines+markers',
            marker_color='orange',
            yaxis='y2',
            line=dict(width=3)
        ))
        
        fig.update_layout(
            title="Price vs Rating Comparison",
            xaxis_title="Products",
            yaxis=dict(title="Price", side="left"),
            yaxis2=dict(title="Rating (0-5)", side="right", overlaying="y"),
            showlegend=True,
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def render_product_metrics(products: List[Dict]):
        """Render product metrics overview"""
        if not products:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics - handle None values properly
        prices = [p.get('price', 0) for p in products if p.get('price') is not None and p.get('price') > 0]
        ratings = [p.get('rating', 0) for p in products if p.get('rating') is not None]
        
        with col1:
            st.metric(
                label="📦 Products Found",
                value=len(products)
            )
        
        with col2:
            if prices:
                avg_price = sum(prices) / len(prices)
                st.metric(
                    label="💰 Avg Price",
                    value=f"{VectorUI.get_currency_symbol(products[0].get('currency', 'USD'))}{avg_price:.0f}"
                )
            else:
                st.metric(label="💰 Avg Price", value="N/A")
        
        with col3:
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                st.metric(
                    label="⭐ Avg Rating",
                    value=f"{avg_rating:.1f}/5.0"
                )
            else:
                st.metric(label="⭐ Avg Rating", value="N/A")
        
        with col4:
            if prices:
                price_range = max(prices) - min(prices)
                st.metric(
                    label="📊 Price Range",
                    value=f"{VectorUI.get_currency_symbol(products[0].get('currency', 'USD'))}{price_range:.0f}"
                )
            else:
                st.metric(label="📊 Price Range", value="N/A")

class ProductDisplay:
    """Handle product display logic"""

    @staticmethod
    def render_product_card(product: Dict, index: int):
        """Render a single product card"""
        with st.container():
            st.markdown('<div class="product-card">', unsafe_allow_html=True)

            # ---- IMAGE RESOLUTION (IMPROVED) ----
            image_url = (
                product.get("image_url")
                or product.get("thumbnail")
                or (product.get("images")[0] if isinstance(product.get("images"), list) and product.get("images") else None)
            )

            product_url = product.get("url")

            # Create layout depending on image availability
            if image_url:
                img_col, info_col = st.columns([1, 3])
            else:
                # No image, use full width for info
                img_col = None
                info_col = st.container()

            # ---- SHOW IMAGE IF PRESENT ----
            if image_url and img_col:
                with img_col:
                    # Make image clickable if product URL exists
                    if product_url:
                        st.markdown(
                            f"""
                            <a href="{product_url}" target="_blank">
                                <img src="{image_url}" style="width:100%; border-radius:10px; cursor:pointer;" />
                            </a>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.image(image_url, use_column_width=True)

            # ---- PRODUCT INFO SECTION ----
            with info_col:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(f"🛍️ {product.get('name', 'Unknown Product')}")

                    # Price
                    price = product.get("price")
                    if price is not None:
                        st.markdown(
                            f'<span class="price-tag">{VectorUI.get_currency_symbol(product.get("currency", "USD"))}{price}</span>',
                            unsafe_allow_html=True
                        )

                    # Rating
                    rating = product.get("rating")
                    if rating is not None:
                        stars = "⭐" * int(rating)
                        st.markdown(
                            f'<span class="rating-stars">{stars}</span> ({rating}/5.0)',
                            unsafe_allow_html=True
                        )
                        if product.get("rating_count"):
                            st.caption(f"Based on {product['rating_count']} reviews")

                with col2:
                    if product_url:
                        st.link_button("🔗 View Product", product_url, width="stretch")

                    if product.get("source"):
                        st.caption(f"Source: {product['source']}")

                    # Availability
                    status = product.get("availability")
                    if status:
                        if status.lower() == "in_stock":
                            st.success(f"✅ {status}")
                        else:
                            st.error(f"❌ {status}")

            st.markdown('</div>', unsafe_allow_html=True)

class RecommendationDisplay:
    """Handle recommendation display logic"""
    
    @staticmethod
    def render_recommendations(recommendations: Dict):
        """Render the final recommendations"""
        if not recommendations:
            return
        
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.subheader("🎯 AI Recommendations")
        
        # Top picks
        if recommendations.get('top_picks'):
            st.write("**🏆 Top Picks:**")
            for i, pick in enumerate(recommendations.get('top_picks', []), 1):
                st.write(f"{i}. {pick}")
            st.divider()
        
        # Detailed recommendations
        if recommendations.get('recommendations'):
            st.write("**📋 Detailed Analysis:**")
            
            for i, rec in enumerate(recommendations.get('recommendations', []), 1):
                with st.expander(f"🔍 #{i} {rec.get('product_name', 'Product')}", expanded=i==1):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Why recommended:** {rec.get('why', 'N/A')}")
                        if rec.get('tradeoffs'):
                            st.write(f"**Tradeoffs:** {rec.get('tradeoffs')}")
                    
                    with col2:
                        if rec.get('price'):
                            curr = rec.get('currency', 'USD')
                            symbol = VectorUI.get_currency_symbol(curr)
                            st.metric("Price", f"{symbol}{rec.get('price')}")
                        if rec.get('rating'):
                            st.metric("Rating", f"{rec.get('rating')}/5.0")
                        if rec.get('url'):
                            st.link_button("🔗 View Product", rec.get('url'), width="stretch")
        
        # Final choice
        if recommendations.get('final_choice'):
            final_choice = recommendations.get('final_choice')
            st.divider()
            st.write("**🎖️ Final Choice:**")
            st.success(f"**{final_choice.get('product_name')}**")
            st.write(f"**Reason:** {final_choice.get('reason', 'N/A')}")
        
        st.markdown('</div>', unsafe_allow_html=True)