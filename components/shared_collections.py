import streamlit as st
from typing import Dict, List

def initialize_shared_state():
    """Initialize shared state for user collections"""
    if 'user_collections' not in st.session_state:
        st.session_state.user_collections = {}
    if 'user_ratings' not in st.session_state:
        st.session_state.user_ratings = {}

def update_user_collection(username: str, cards: List[Dict], total_value: float):
    """Update a user's collection in shared state"""
    st.session_state.user_collections[username] = {
        'cards': cards,
        'total_value': total_value,
        'timestamp': st.session_state.get('last_update', 'Just now')
    }

def add_rating(from_user: str, to_user: str, rating: int):
    """Add a rating for a user's collection"""
    if to_user not in st.session_state.user_ratings:
        st.session_state.user_ratings[to_user] = {}
    st.session_state.user_ratings[to_user][from_user] = rating

def get_average_rating(username: str) -> float:
    """Get average rating for a user's collection"""
    if username not in st.session_state.user_ratings:
        return 0.0
    ratings = st.session_state.user_ratings[username].values()
    return sum(ratings) / len(ratings) if ratings else 0.0

def display_shared_collections(current_user: str):
    """Display all users' collections with ratings"""
    if not st.session_state.user_collections:
        st.info("No other collections to display yet. Be the first to share yours!")
        return

    st.markdown("### 🌟 Community Collections")
    
    for username, collection in st.session_state.user_collections.items():
        if username != current_user:  # Don't show current user's collection
            with st.expander(f"📚 {username}'s Collection"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Total Value:** ${collection['total_value']:.2f}")
                    st.markdown(f"**Cards:** {len(collection['cards'])}")
                    st.markdown(f"**Last Updated:** {collection['timestamp']}")
                
                with col2:
                    # Rating system
                    current_rating = st.session_state.user_ratings.get(username, {}).get(current_user, 0)
                    new_rating = st.select_slider(
                        "Rate this collection",
                        options=[1, 2, 3, 4, 5],
                        value=current_rating,
                        key=f"rating_{username}"
                    )
                    
                    if new_rating != current_rating:
                        add_rating(current_user, username, new_rating)
                    
                    avg_rating = get_average_rating(username)
                    st.metric("Average Rating", f"⭐ {avg_rating:.1f}")

                # Show preview of cards
                if collection['cards']:
                    st.markdown("**Featured Cards:**")
                    for i, card in enumerate(collection['cards'][:3]):  # Show first 3 cards
                        st.markdown(f"- {card['card_name']} (${card['current_price']:.2f})")
                    if len(collection['cards']) > 3:
                        st.markdown(f"*...and {len(collection['cards']) - 3} more cards*")
