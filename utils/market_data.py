import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from typing import Dict, List, Optional
import os

def _validate_api_key(api_key: str) -> Dict:
    """
    Validate the API key by making a test request.
    """
    try:
        response = requests.get(
            "https://api.pokemontcg.io/v2/cards",
            params={"pageSize": 1},
            headers={"X-Api-Key": api_key}
        )

        if response.status_code == 200:
            return {"success": True, "error": None}
        elif response.status_code == 401:
            return {"success": False, "error": "Invalid API key"}
        else:
            return {"success": False, "error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def _fetch_card_market_data(card_name: str, api_key: str) -> Dict:
    """
    Fetch current market data for all variants of a specific Pokemon card.
    """
    if not api_key:
        return {
            "success": False,
            "error": "Pokemon TCG API key not found. Please check your configuration.",
            "data": None
        }

    try:
        # Clean the card name for the API query
        query = f'name:*{card_name}*'  # Use partial matching to find all variants

        # Make API request
        response = requests.get(
            "https://api.pokemontcg.io/v2/cards",
            params={
                "q": query,
                "orderBy": "-cardmarket.prices.averageSellPrice",  # Sort by price descending
                "pageSize": 20  # Get more results to include variants
            },
            headers={"X-Api-Key": api_key}
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API Error: {response.status_code}",
                "data": None
            }

        data = response.json()

        if not data.get("data"):
            return {
                "success": False,
                "error": "No data found for this card",
                "data": None
            }

        # Process all matching cards
        cards_data = []
        search_name_lower = card_name.lower()

        for card in data["data"]:
            if card.get("cardmarket") and search_name_lower in card["name"].lower():
                card_info = {
                    "card_name": card["name"],
                    "set": card.get("set", {}).get("name", "Unknown"),
                    "current_price": card.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0),
                    "image_url": card.get("images", {}).get("large") or card.get("images", {}).get("small"),
                    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "trend": _calculate_price_trend(card),
                    "availability": _get_availability_status(card),
                    "rarity": card.get("rarity", "Unknown"),
                    "supertype": card.get("supertype", "Unknown"),
                    "subtypes": ", ".join(card.get("subtypes", [])),
                    "number": card.get("number", "N/A"),
                    "artist": card.get("artist", "Unknown")
                }
                cards_data.append(card_info)

        if not cards_data:
            return {
                "success": False,
                "error": "No market data available for this card",
                "data": None
            }

        return {
            "success": True,
            "error": None,
            "data": cards_data  # Return list of all variants
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error fetching market data: {str(e)}",
            "data": None
        }

def _calculate_price_trend(card_data: Dict) -> str:
    """Calculate price trend based on historical data."""
    prices = card_data.get("cardmarket", {}).get("prices", {})
    avg_price = prices.get("averageSellPrice", 0)
    avg_7days = prices.get("avg7", 0)

    if avg_price > avg_7days:
        return "↑ Rising"
    elif avg_price < avg_7days:
        return "↓ Falling"
    return "→ Stable"

def _get_availability_status(card_data: Dict) -> str:
    """Determine card availability status."""
    rarity = card_data.get("rarity", "").lower()
    if "rare" in rarity and "ultra" in rarity:
        return "Very Rare"
    elif "rare" in rarity:
        return "Rare"
    elif "uncommon" in rarity:
        return "Uncommon"
    return "Common"

class PokemonMarketData:
    """
    Handles real-time market data fetching and processing for Pokemon cards.
    """

    def __init__(self):
        # Try to get API key from environment first, then fallback to secrets
        self.api_key = os.environ.get("POKEMON_TCG_API_KEY", "")

        if not self.api_key:
            try:
                self.api_key = st.secrets["POKEMON_TCG_API_KEY"]
            except Exception:
                st.error("""
                Pokemon TCG API key not found. Please ensure the API key is properly configured.
                If you haven't set up your API key yet, you can get one from https://dev.pokemontcg.io/
                """)
                self.api_key = ""
                return

        # Validate API key
        validation_result = _validate_api_key(self.api_key)
        if not validation_result["success"]:
            st.error(f"API key validation failed: {validation_result['error']}")
            self.api_key = ""

    def get_card_market_data(self, card_name: str) -> Dict:
        """
        Fetch current market data for all variants of a specific Pokemon card.
        """
        return _fetch_card_market_data(card_name, self.api_key)

    def get_market_trends(self) -> Dict:
        """
        Get overall market trends and statistics.
        """
        return _fetch_market_trends(self.api_key)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def _fetch_market_trends(api_key: str) -> Dict:
    """
    Get overall market trends and statistics.
    """
    if not api_key:
        return {
            "success": False,
            "error": "Pokemon TCG API key not found. Please check your configuration.",
            "data": None
        }

    try:
        response = requests.get(
            "https://api.pokemontcg.io/v2/cards",
            params={"pageSize": 100, "orderBy": "set.releaseDate"},
            headers={"X-Api-Key": api_key}
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API Error: {response.status_code}",
                "data": None
            }

        data = response.json()

        # Calculate market metrics
        cards = data.get("data", [])
        prices = [
            card.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0)
            for card in cards
            if card.get("cardmarket")
        ]

        if not prices:
            return {
                "success": False,
                "error": "No price data available",
                "data": None
            }

        metrics = {
            "total_cards": len(cards),
            "average_price": sum(prices) / len(prices) if prices else 0,
            "highest_price": max(prices) if prices else 0,
            "lowest_price": min(prices) if prices else 0,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return {
            "success": True,
            "error": None,
            "data": metrics
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error fetching market trends: {str(e)}",
            "data": None
        }