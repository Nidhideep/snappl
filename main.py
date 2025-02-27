import streamlit as st
import pandas as pd
from utils.data_generator import generate_card_data, generate_price_history, generate_market_metrics
from components.card_grid import display_card_grid
from components.market_analytics import display_market_metrics, display_market_analysis
from components.profile import display_profile
from components.watchlist import display_watchlist
from components.card_analyzer import display_card_analysis

# Page configuration
st.set_page_config(
    page_title="Trading Card Market Analysis",
    page_icon="🃏",
    layout="wide"
)

# Load custom CSS
with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'cards_df' not in st.session_state:
    st.session_state.cards_df = generate_card_data()
if 'price_history' not in st.session_state:
    st.session_state.price_history = generate_price_history()
if 'market_metrics' not in st.session_state:
    st.session_state.market_metrics = generate_market_metrics()

# Sidebar
st.sidebar.title("Trading Card Market")
page = st.sidebar.radio("Navigation", ["Market Overview", "Card Analysis", "My Profile", "Watchlist"])

# Card search
st.sidebar.markdown("## Search & Filters")
search_query = st.sidebar.text_input("Search Cards", "")

# Filters
name_filter = st.sidebar.multiselect(
    "Card Name",
    options=st.session_state.cards_df['name'].unique()
)
condition_filter = st.sidebar.multiselect(
    "Condition",
    options=st.session_state.cards_df['condition'].unique()
)
price_range = st.sidebar.slider(
    "Price Range ($)",
    min_value=0,
    max_value=10000,
    value=(0, 10000)
)

# Apply filters and search
filtered_df = st.session_state.cards_df
if search_query:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False)]
if name_filter:
    filtered_df = filtered_df[filtered_df['name'].isin(name_filter)]
if condition_filter:
    filtered_df = filtered_df[filtered_df['condition'].isin(condition_filter)]
filtered_df = filtered_df[
    (filtered_df['price'] >= price_range[0]) &
    (filtered_df['price'] <= price_range[1])
]

# Main content
if page == "Market Overview":
    st.title("Trading Card Market Analysis")

    display_market_metrics(st.session_state.market_metrics)
    st.markdown("---")

    display_market_analysis(
        st.session_state.price_history,
        st.session_state.cards_df
    )
    st.markdown("---")

    display_card_grid(filtered_df)

elif page == "Card Analysis":
    st.title("Card Image Analysis")

    # Card image upload
    uploaded_file = st.file_uploader(
        "Upload a card image for analysis",
        type=['jpg', 'png', 'jpeg'],
        help="Upload a clear image of your trading card for instant analysis"
    )

    if uploaded_file:
        display_card_analysis(uploaded_file)
    else:
        st.info("Upload a card image to get detailed market analysis and price estimates.")

elif page == "My Profile":
    display_profile()

else:  # Watchlist
    display_watchlist(filtered_df.head())

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Trading Card Market Analysis Platform • © 2023</p>
    </div>
    """,
    unsafe_allow_html=True
)