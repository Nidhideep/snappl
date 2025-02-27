import streamlit as st

def display_card(card):
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(
                "https://images.unsplash.com/photo-1644361566696-3d442b5b482a",
                use_column_width=True
            )
        
        with col2:
            st.markdown(f"### {card['name']}")
            st.markdown(f"**Set:** {card['set']}")
            st.markdown(f"**Condition:** {card['condition']}")
            st.markdown(f"**Price:** ${card['price']:,.2f}")
            st.markdown(f"**Market Trend:** {card['market_trend']}")
            
            if st.button("Add to Watchlist", key=f"watch_{card['name']}_{card['condition']}"):
                st.success("Added to watchlist!")

def display_card_grid(cards_df, filters=None):
    if filters:
        # Apply filters here
        pass
        
    st.markdown("## Available Cards")
    
    for idx, card in cards_df.iterrows():
        with st.container():
            st.markdown("---")
            display_card(card)
