import streamlit as st
from utils.image_processor import analyze_card_image
from utils.market_data import PokemonMarketData
import plotly.graph_objects as go
from datetime import datetime, timedelta

def display_market_info(card_name: str):
    """
    Display real-time market information for a Pokemon card.
    """
    market_data = PokemonMarketData()
    result = market_data.get_card_market_data(card_name)

    if not result['success']:
        st.warning(f"Could not fetch market data: {result['error']}")
        return

    data = result['data']

    # Display current market data
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Price",
            f"${data['current_price']:.2f}",
            delta=data['trend'].split()[0]
        )

    with col2:
        st.metric("Set", data['set'])

    with col3:
        st.metric("Availability", data['availability'])

    st.caption(f"Last updated: {data['last_update']}")

def display_card_analysis(uploaded_file):
    """
    Display the analysis results for an uploaded Pokemon card image.
    """
    if uploaded_file is None:
        return

    with st.spinner('Analyzing Pokemon card image...'):
        # Process the uploaded image
        analysis_result = analyze_card_image(uploaded_file)

        if not analysis_result['success']:
            st.error(f"Error analyzing image: {analysis_result['error']}")
            return

        analysis_data = analysis_result['data']

        # Display analysis results
        st.subheader("Pokemon Card Analysis Results")

        # Create columns for layout
        col1, col2 = st.columns([1, 2])

        with col1:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Card", use_container_width=True)

        with col2:
            # Display extracted Pokemon information
            st.markdown("### Card Details")
            pokemon_info = analysis_data['pokemon_info']

            st.write(f"**Pokemon Name:** {pokemon_info['name']}")
            if pokemon_info['hp']:
                st.write(f"**HP:** {pokemon_info['hp']}")

            if pokemon_info['attacks']:
                st.markdown("#### Attacks")
                for attack in pokemon_info['attacks']:
                    st.write(f"- {attack}")

            with st.expander("Raw Text Content"):
                for line in analysis_data['text_content']:
                    st.write(line)

        # Market Analysis Section
        st.markdown("### Real-Time Market Analysis")
        if pokemon_info['name']:
            display_market_info(pokemon_info['name'])

        # Market Trends
        market_data = PokemonMarketData()
        trends = market_data.get_market_trends()

        if trends['success']:
            st.markdown("### Market Overview")
            trend_data = trends['data']

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Market Price", f"${trend_data['average_price']:.2f}")
                st.metric("Lowest Price", f"${trend_data['lowest_price']:.2f}")

            with col2:
                st.metric("Highest Price", f"${trend_data['highest_price']:.2f}")
                st.metric("Total Cards Tracked", trend_data['total_cards'])