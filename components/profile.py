import streamlit as st

def display_profile():
    st.markdown("## Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(
            "https://images.unsplash.com/photo-1533900298318-6b8da08a523e",
            use_column_width=True
        )
    
    with col2:
        st.markdown("### John Doe")
        st.markdown("Member since: January 2023")
        st.markdown("Trading Score: ⭐⭐⭐⭐")
        
        st.markdown("#### Statistics")
        st.markdown("Cards Owned: 47")
        st.markdown("Total Value: $12,450")
        st.markdown("Recent Transactions: 5")
