import streamlit as st
import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv
from src.frontend.components import VectorUI, ProductDisplay, RecommendationDisplay

load_dotenv(override=True)

def make_api_request(query: str, api_url: str = "http://localhost:8000/USER") -> Dict[str, Any]:
    """Make API request to the FastAPI backend"""
    try:
        payload = {"user": query}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API server. Make sure the FastAPI server is running on http://localhost:8000")
        return {}
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ API request failed: {e}")
        return {}
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        return {}

def display_product_card(product):
    """Display a single product in a card format"""
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"🛍️ {product.get('name', 'Unknown Product')}")
            st.write(f"**Price:** {product.get('price', 'N/A')} {product.get('currency', '')}")
            
            if product.get('rating'):
                stars = "⭐" * int(product.get('rating', 0))
                st.write(f"**Rating:** {stars} ({product.get('rating')}/5.0)")
                if product.get('rating_count'):
                    st.write(f"**Reviews:** {product.get('rating_count')} reviews")
            
            if product.get('snippet'):
                st.write(f"**Description:** {product.get('snippet')}")
            
            if product.get('availability'):
                availability_color = "🟢" if product.get('availability').lower() == 'in_stock' else "🔴"
                st.write(f"**Availability:** {availability_color} {product.get('availability')}")
        
        with col2:
            if product.get('url'):
                st.link_button("🔗 View Product", product.get('url'))
            
            if product.get('source'):
                st.write(f"**Source:** {product.get('source')}")
        
        # Display review summary if available
        if product.get('review'):
            review = product.get('review')
            if review.get('pros'):
                st.write("**✅ Pros:**")
                for pro in review.get('pros', []):
                    st.write(f"  • {pro}")
            
            if review.get('cons'):
                st.write("**❌ Cons:**")
                for con in review.get('cons', []):
                    st.write(f"  • {con}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_recommendations(recommendations):
    """Display the final recommendations"""
    if not recommendations:
        return
    
    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
    st.subheader("🎯 Final Recommendations")
    
    # Top picks
    if recommendations.get('top_picks'):
        st.write("**🏆 Top Picks:**")
        for pick in recommendations.get('top_picks', []):
            st.write(f"• {pick}")
        st.write("---")
    
    # Detailed recommendations
    if recommendations.get('recommendations'):
        st.write("**📋 Detailed Analysis:**")
        for rec in recommendations.get('recommendations', []):
            with st.expander(f"🔍 {rec.get('product_name', 'Product')}"):
                if rec.get('price'):
                    st.write(f"**Price:** {rec.get('price')} {rec.get('currency', '')}")
                if rec.get('rating'):
                    st.write(f"**Rating:** ⭐ {rec.get('rating')}/5.0")
                if rec.get('source'):
                    st.write(f"**Source:** {rec.get('source')}")
                if rec.get('url'):
                    st.link_button("🔗 View Product", rec.get('url'))
                
                st.write(f"**Why recommended:** {rec.get('why', 'N/A')}")
                if rec.get('tradeoffs'):
                    st.write(f"**Tradeoffs:** {rec.get('tradeoffs')}")
    
    # Final choice
    if recommendations.get('final_choice'):
        final_choice = recommendations.get('final_choice')
        st.write("---")
        st.write("**🎖️ Final Choice:**")
        st.success(f"**{final_choice.get('product_name')}**")
        st.write(f"**Reason:** {final_choice.get('reason', 'N/A')}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Setup page and load CSS
    VectorUI.setup_page_config()
    VectorUI.load_custom_css()
    
    # Render header
    VectorUI.render_header()
    
    # Render sidebar and get API URL
    api_url = VectorUI.render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Query input
        query = st.text_area(
            "🔍 Enter your product search query:",
            value=st.session_state.get('query', ''),
            height=100,
            placeholder="e.g., 'I need a lightweight laptop under $1200 for programming. Prefer Dell or Lenovo.'"
        )
        
        # Update session state
        if query != st.session_state.get('query', ''):
            st.session_state.query = query
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        search_button = st.button("🚀 Search Products", type="primary", use_container_width=True)
        clear_button = st.button("🗑️ Clear Results", use_container_width=True)
    
    # Clear results
    if clear_button:
        if 'results' in st.session_state:
            del st.session_state.results
        st.rerun()
    
    # Process search
    if search_button and query.strip():
        with st.spinner("🔍 Searching for products... This may take a moment."):
            results = make_api_request(query, api_url)
            if results:
                st.session_state.results = results
    
    # Display results
    if 'results' in st.session_state:
        results = st.session_state.results
        
        # Display product list
        if results.get('product_list') and results['product_list'].get('products'):
            products = results['product_list']['products']
            
            st.subheader("📦 Product Results")
            st.write(f"Found {len(products)} products")
            
            # Show metrics overview
            VectorUI.render_product_metrics(products)
            
            # Show price comparison chart
            chart = VectorUI.create_price_comparison_chart(products)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["🎯 Detailed View", "📊 Quick Overview", "📈 Analytics"])
            
            with tab1:
                for i, product in enumerate(products):
                    ProductDisplay.render_product_card(product, i)
            
            with tab2:
                # Create a simple table view
                table_data = []
                for product in products:
                    table_data.append({
                        "Product": product.get('name', 'N/A'),
                        "Price": f"₹{product.get('price', 'N/A')} {product.get('currency', '')}",
                        "Rating": f"{product.get('rating', 'N/A')}/5.0" if product.get('rating') else 'N/A',
                        "Source": product.get('source', 'N/A'),
                        "Availability": product.get('availability', 'N/A')
                    })
                st.dataframe(table_data, use_container_width=True)
            
            with tab3:
                # Additional analytics
                col1, col2 = st.columns(2)
                
                with col1:
                    # Price distribution
                    prices = [p.get('price', 0) for p in products if p.get('price')]
                    if prices:
                        st.subheader("💰 Price Distribution")
                        import plotly.express as px
                        import pandas as pd
                        df = pd.DataFrame({'Price': prices})
                        fig = px.histogram(df, x='Price', nbins=10, title="Price Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Rating distribution
                    ratings = [p.get('rating', 0) for p in products if p.get('rating')]
                    if ratings:
                        st.subheader("⭐ Rating Distribution")
                        df = pd.DataFrame({'Rating': ratings})
                        fig = px.histogram(df, x='Rating', nbins=5, title="Rating Distribution")
                        st.plotly_chart(fig, use_container_width=True)
        
        # Display recommendations
        if results.get('final_recommendation'):
            RecommendationDisplay.render_recommendations(results['final_recommendation'])
        
        # Raw data toggle
        with st.expander("🔧 Raw API Response (for debugging)"):
            st.json(results)

if __name__ == "__main__":
    main()