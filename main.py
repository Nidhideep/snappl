import streamlit as st
from utils.market_data import PokemonMarketData

# Page configuration
st.set_page_config(
    page_title="Snappl Pokemon Card Market Analysis",
    page_icon="attached_assets/create pokemon card image.jpg",
    layout="wide"
)

# Logo and title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("attached_assets/create pokemon card image.jpg", width=200)

st.title("Snappl Pokemon Card Market Analysis")
st.markdown("Enter a Pokemon card name to get real-time market data and card information.")
st.markdown("*Info: There are some Pokemon cards we have not got written down!*")

# Search input
card_name = st.text_input(
    "Search for a Pokemon card:",
    placeholder="e.g., Charizard, Pikachu"
)

if card_name:
    market_data = PokemonMarketData()
    result = market_data.get_card_market_data(card_name)

    if result['success']:
        cards_data = result['data']

        st.markdown(f"### Found {len(cards_data)} variants of {card_name}")

        # Create a grid layout for multiple cards
        cols = st.columns(2)  # Display 2 cards per row

        for idx, card in enumerate(cards_data):
            col = cols[idx % 2]  # Alternate between columns

            with col:
                st.markdown("---")
                # Card container
                with st.container():
                    # Display card image and basic info
                    if card.get('image_url'):
                        st.image(card['image_url'], caption=card['card_name'], use_column_width=True)

                    # Card details
                    st.markdown(f"### {card['card_name']}")
                    st.markdown(f"""
                    **Set:** {card['set']}  
                    **Number:** {card['number']}  
                    **Artist:** {card['artist']}  
                    **Type:** {card['supertype']} {card['subtypes']}  
                    **Rarity:** {card['rarity']}
                    """)

                    # Market metrics in columns
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric(
                            "Price",
                            f"${card['current_price']:.2f}",
                            delta=card['trend'].split()[0]
                        )
                    with m2:
                        st.metric("Availability", card['availability'])
                    with m3:
                        st.metric("Updated", card['last_update'])

    else:
        st.error(f"Error fetching card data: {result['error']}")
        st.info("""
        Tips:
        - Check the spelling of the card name
        - Some cards might not have market data available
        """)

# Placeholder for utils.market_data module
# This module needs to be implemented with actual API calls.
# Replace this with your actual implementation
from typing import Dict, Any, List

class PokemonMarketData:
    def get_card_market_data(self, card_name: str) -> Dict[str, Any]:
        # Replace this with your actual API call and data processing
        # This is a placeholder that simulates successful and unsuccessful responses
        if card_name.lower() in ["charizard", "pikachu", "charizard v", "pikachu vmax"]:
            return {
                'success': True,
                'data': [
                    {
                        'card_name': "Charizard V",
                        'image_url': "https://example.com/charizard_v.jpg",
                        'current_price': 100.50,
                        'trend': "Up 10%",
                        'availability': "High",
                        'last_update': "2024-03-08",
                        'set': "Sword & Shield",
                        'number': '10',
                        'artist': 'Artist1',
                        'supertype': 'Pokémon',
                        'subtypes': ['Basic'],
                        'rarity': 'Rare'
                    },
                    {
                        'card_name': "Pikachu VMAX",
                        'image_url': "https://example.com/pikachu_vmax.jpg",
                        'current_price': 50.25,
                        'trend': "Down 5%",
                        'availability': "Medium",
                        'last_update': "2024-03-07",
                        'set': "Sword & Shield",
                        'number': '20',
                        'artist': 'Artist2',
                        'supertype': 'Pokémon',
                        'subtypes': ['Basic'],
                        'rarity': 'Rare Holo'
                    }
                ]
            }
        else:
            return {
                'success': False,
                'error': "Card not found"
            }