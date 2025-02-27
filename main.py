import streamlit as st
from utils.market_data import PokemonMarketData # Placeholder import

# Page configuration
st.set_page_config(
    page_title="Pokemon Card Market Analysis",
    page_icon="🃏",
    layout="wide"
)

# Title and description
st.title("Pokemon Card Market Analysis")
st.markdown("Enter a Pokemon card name to get real-time market data and card information.")

# Search input
card_name = st.text_input("Search for a Pokemon card:", placeholder="e.g., Charizard, Pikachu")

if card_name:
    market_data = PokemonMarketData()
    result = market_data.get_card_market_data(card_name)

    if result['success']:
        data = result['data']

        # Create two columns for layout
        col1, col2 = st.columns([1, 2])

        with col1:
            # Display card image
            if data.get('image_url'):
                st.image(data['image_url'], caption=data['card_name'], use_column_width=True)
            else:
                st.write("No image found for this card.")


        with col2:
            # Display market data
            st.header(data['card_name'])
            if data.get('set'):
                st.subheader(f"Set: {data['set']}")
            else:
                st.write("Set information not available.")

            # Market metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                try:
                    st.metric(
                        "Current Price",
                        f"${data['current_price']:.2f}",
                        delta=data['trend'].split()[0]
                    )
                except (KeyError, TypeError):
                    st.metric("Current Price", "N/A")

            with metric_col2:
                try:
                    st.metric("Availability", data['availability'])
                except KeyError:
                    st.metric("Availability", "N/A")

            with metric_col3:
                try:
                    st.metric("Last Updated", data['last_update'])
                except KeyError:
                    st.metric("Last Updated", "N/A")


            # Market analysis
            st.markdown("### Market Analysis")
            try:
                st.markdown(f"""
                - **Price Trend**: {data['trend']}
                - **Market Status**: {data['availability']} availability
                - **Set Information**: From {data['set']}
                """)
            except KeyError:
                st.write("Market analysis not available.")


    else:
        st.error(f"Error fetching card data: {result['error']}")
        st.info("""
        Tips:
        - Check the spelling of the card name
        - Try using the full name of the card
        - Some cards might not have market data available
        """)

# Placeholder for utils.market_data module
# This module needs to be implemented with actual API calls.
# Replace this with your actual implementation
from typing import Dict, Any

class PokemonMarketData:
    def get_card_market_data(self, card_name: str) -> Dict[str, Any]:
        # Replace this with your actual API call and data processing
        # This is a placeholder that simulates successful and unsuccessful responses
        if card_name.lower() in ["charizard", "pikachu"]:
            return {
                'success': True,
                'data': {
                    'card_name': card_name.title(),
                    'image_url': "https://example.com/image.jpg",  # Replace with actual image URL
                    'current_price': 100.50,
                    'trend': "Up 10%",
                    'availability': "High",
                    'last_update': "2024-03-08",
                    'set': "Base Set"
                }
            }
        else:
            return {
                'success': False,
                'error': "Card not found"
            }