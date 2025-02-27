import streamlit as st
from utils.market_data import PokemonMarketData

def display_card(card, card_index):
    market_data = PokemonMarketData()
    result = market_data.get_card_market_data(card['name'])

    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                "https://images.unsplash.com/photo-1644361566696-3d442b5b482a",
                use_container_width=True
            )

        with col2:
            st.markdown(f"### {card['name']}")
            st.markdown(f"**Set:** {card['set']}")
            st.markdown(f"**Condition:** {card['condition']}")

            # Display market data if available
            if result['success']:
                data = result['data']
                col_price, col_trend = st.columns(2)

                with col_price:
                    st.metric(
                        "Market Price",
                        f"${data['current_price']:,.2f}",
                        delta=data['trend'].split()[0]
                    )

                with col_trend:
                    st.metric("Availability", data['availability'])

                st.caption(f"Last updated: {data['last_update']}")
            else:
                st.markdown(f"**Price:** ${card['price']:,.2f}")
                st.markdown(f"**Market Trend:** {card['market_trend']}")

            # Use a unique key combining index, name, and condition
            if st.button("Add to Watchlist", key=f"watch_{card_index}_{card['name']}_{card['condition']}"):
                st.success("Added to watchlist!")

def display_card_grid(cards_df, filters=None):
    if filters:
        # Apply filters here
        pass

    st.markdown("## Available Cards")

    # Display market overview if cards are found
    if not cards_df.empty:
        market_data = PokemonMarketData()
        trends = market_data.get_market_trends()

        if trends['success']:
            st.markdown("### Market Overview")
            trend_data = trends['data']

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Average Price", f"${trend_data['average_price']:.2f}")
            with col2:
                st.metric("Lowest Price", f"${trend_data['lowest_price']:.2f}")
            with col3:
                st.metric("Highest Price", f"${trend_data['highest_price']:.2f}")
            with col4:
                st.metric("Cards Tracked", trend_data['total_cards'])

            st.markdown("---")

    for idx, card in cards_df.iterrows():
        with st.container():
            st.markdown("---")
            display_card(card, idx)