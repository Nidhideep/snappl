import streamlit as st
from utils.chart_helpers import create_price_history_chart, create_market_trend_chart

def display_market_metrics(metrics):
    st.markdown("## Market Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Listings", metrics['total_listings'])
    
    with col2:
        st.metric("Average Price", f"${metrics['avg_price']:,.2f}")
    
    with col3:
        st.metric("Daily Volume", metrics['daily_volume'])
    
    with col4:
        st.metric("Price Trend", f"{metrics['price_trend']}%")

def display_market_analysis(price_history_df, cards_df):
    st.markdown("## Market Analysis")
    
    tab1, tab2 = st.tabs(["Price History", "Market Trends"])
    
    with tab1:
        fig = create_price_history_chart(price_history_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = create_market_trend_chart(cards_df)
        st.plotly_chart(fig, use_container_width=True)
