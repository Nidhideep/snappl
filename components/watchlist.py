import streamlit as st

def display_watchlist(cards_df):
    st.markdown("## Your Watchlist")
    
    if len(cards_df) == 0:
        st.info("Your watchlist is empty. Add cards to track their prices!")
        return
    
    for idx, card in cards_df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{card['name']}** ({card['condition']})")
                st.markdown(f"Set: {card['set']}")
            
            with col2:
                st.markdown(f"${card['price']:,.2f}")
                st.markdown(f"Trend: {card['market_trend']}")
            
            with col3:
                if st.button("Remove", key=f"remove_{idx}"):
                    st.success("Removed from watchlist!")
