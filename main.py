import streamlit as st
from utils.market_data import PokemonMarketData
from utils.currency_converter import get_currency_options, convert_price, format_currency
from components.shared_collections import initialize_shared_state, update_user_collection, display_shared_collections

# Page configuration
st.set_page_config(
    page_title="Snappl Pokemon Card Market Analysis",
    page_icon="attached_assets/pokemon.webp",
    layout="wide",
    initial_sidebar_state="collapsed"  # This will collapse the sidebar by default
)

# Initialize session state for user name
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

initialize_shared_state() #Added

# User name input form
if st.session_state.user_name is None:
    with st.form("user_name_form"):
        user_name = st.text_input("Enter your name:", placeholder="e.g., John")
        submit = st.form_submit_button("Start Feeling Rich!")
        if submit and user_name:
            st.session_state.user_name = user_name
            st.rerun()

# Only show the main app if user has entered their name
if st.session_state.user_name:
    # Logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("attached_assets/pokemon.webp", width=200)

    st.title("Snappl Pokemon Card Market Analysis")
    st.markdown(f"Welcome, {st.session_state.user_name}! Enter a Pokemon card name to get real-time market data and card information.")
    st.markdown("*Info: There are some Pokemon cards we have not got written down!*")

    # Initialize session state for selected cards
    if 'selected_cards' not in st.session_state:
        st.session_state.selected_cards = []

    # Search input
    card_name = st.text_input(
        "Search for a Pokemon card:",
        placeholder="e.g., Charizard, Pikachu"
    )

    # Calculator Section at the top (moved outside search results)
    calculator_container = st.container()

    if card_name:
        market_data = PokemonMarketData()
        result = market_data.get_card_market_data(card_name)

        if result['success']:
            cards_data = result['data']

            st.markdown(f"### Found {len(cards_data)} variants of {card_name}")
            st.markdown("---")

            # Create a grid layout for multiple cards
            cols = st.columns(2)  # Display 2 cards per row

            for idx, card in enumerate(cards_data):
                col = cols[idx % 2]  # Alternate between columns

                with col:
                    st.markdown("---")
                    # Card container
                    with st.container():
                        # Checkbox and card title in the same row
                        col_check, col_title = st.columns([1, 4])
                        with col_check:
                            # Create a unique key using card properties
                            checkbox_key = f"select_{card['card_name']}_{card['set']}_{card['number']}"
                            # Check if card is already selected
                            is_already_selected = any(
                                selected['card_name'] == card['card_name'] and
                                selected['set'] == card['set'] and
                                selected['number'] == card['number']
                                for selected in st.session_state.selected_cards
                            )
                            is_selected = st.checkbox("", key=checkbox_key, value=is_already_selected)

                            if is_selected and not is_already_selected:
                                st.session_state.selected_cards.append(card)
                            elif not is_selected and is_already_selected:
                                st.session_state.selected_cards = [
                                    c for c in st.session_state.selected_cards
                                    if not (c['card_name'] == card['card_name'] and
                                            c['set'] == card['set'] and
                                            c['number'] == card['number'])
                                ]

                        with col_title:
                            st.markdown(f"### {card['card_name']}")

                        # Display card image and basic info
                        if card.get('image_url'):
                            st.image(card['image_url'], caption=card['card_name'], use_container_width=True)

                        # Card details
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

    # Update Calculator Section with selected cards (outside the search results)
    with calculator_container:
        if st.session_state.selected_cards:
            st.markdown("### Selected Cards Calculator")

            # Add personalized message with total
            total_usd = sum(card['current_price'] for card in st.session_state.selected_cards)
            st.markdown(f"### Hey {st.session_state.user_name}! Your collection is worth: ${total_usd:.2f} 💰")

            # Update shared collections
            update_user_collection(
                st.session_state.user_name,
                st.session_state.selected_cards,
                total_usd
            )

            # Add disclaimer
            st.info("""
            **Disclaimer:** 
            - These calculations are for entertainment purposes only
            - Actual card values depend on condition, authenticity, and market demand
            - Market prices can vary significantly from these estimates
            - This tool is designed for fun and educational purposes
            """)

            # Currency selection
            currency_options = get_currency_options()
            selected_currency = st.selectbox(
                "Select Currency",
                options=list(currency_options.keys()),
                format_func=lambda x: f"{x} - {currency_options[x]}"
            )

            # Display selected cards in a table
            st.markdown("#### Selected Cards:")
            st.markdown(f"*Total cards selected: {len(st.session_state.selected_cards)}*")

            for card in st.session_state.selected_cards:
                # Convert individual card price
                conversion = convert_price(card['current_price'], 'USD', selected_currency)
                if conversion['success']:
                    converted_price = format_currency(conversion['amount'], selected_currency)
                    usd_price = format_currency(card['current_price'], 'USD')
                    st.markdown(f"- {card['card_name']} ({card['set']}): {usd_price} ({converted_price})")
                else:
                    st.markdown(f"- {card['card_name']} ({card['set']}): ${card['current_price']:.2f}")

            # Show total with currency conversion
            st.markdown("---")
            conversion = convert_price(total_usd, 'USD', selected_currency)
            if conversion['success']:
                converted_total = format_currency(conversion['amount'], selected_currency)
                st.markdown(f"""
                **Total:** ${total_usd:.2f}  
                **Converted Total:** {converted_total}  
                *Exchange rate as of {conversion['date']}*
                """)
            else:
                st.markdown(f"**Total:** ${total_usd:.2f}")
                st.error(f"Currency conversion error: {conversion.get('error')}")

            st.markdown("---") #Added
            display_shared_collections(st.session_state.user_name) #Added

    # Hide Streamlit default menu and footer
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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