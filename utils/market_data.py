import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from typing import Dict, List, Optional

class PokemonMarketData:
    """
    Handles real-time market data fetching and processing for Pokemon cards.
    Currently using TCGPlayer API as the data source.
    """
    
    def __init__(self):
        self.base_url = "https://api.pokemontcg.io/v2"
        self.cache_duration = timedelta(minutes=5)
        self.last_update = None
        self.cache = {}

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_card_market_data(self, card_name: str) -> Dict:
        """
        Fetch current market data for a specific Pokemon card.
        """
        try:
            # Clean the card name for the API query
            query = card_name.lower().strip()
            
            # Make API request
            response = requests.get(
                f"{self.base_url}/cards",
                params={"q": f"name:{query}"},
                headers={"X-Api-Key": st.secrets.get("POKEMON_TCG_API_KEY", "")}
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

            # Process market data
            card_data = data["data"][0]
            market_data = {
                "card_name": card_data["name"],
                "set": card_data.get("set", {}).get("name", "Unknown"),
                "current_price": card_data.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0),
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "trend": self._calculate_trend(card_data),
                "availability": self._get_availability_status(card_data)
            }

            return {
                "success": True,
                "error": None,
                "data": market_data
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error fetching market data: {str(e)}",
                "data": None
            }

    def _calculate_trend(self, card_data: Dict) -> str:
        """Calculate price trend based on historical data."""
        prices = card_data.get("cardmarket", {}).get("prices", {})
        avg_price = prices.get("averageSellPrice", 0)
        avg_7days = prices.get("avg7", 0)
        
        if avg_price > avg_7days:
            return "↑ Rising"
        elif avg_price < avg_7days:
            return "↓ Falling"
        return "→ Stable"

    def _get_availability_status(self, card_data: Dict) -> str:
        """Determine card availability status."""
        total_prints = card_data.get("set", {}).get("total", 0)
        if total_prints <= 50:
            return "Rare"
        elif total_prints <= 100:
            return "Uncommon"
        return "Common"

    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_market_trends(self) -> Dict:
        """
        Get overall market trends and statistics.
        """
        try:
            response = requests.get(
                f"{self.base_url}/cards",
                params={"pageSize": 100, "orderBy": "set.releaseDate"},
                headers={"X-Api-Key": st.secrets.get("POKEMON_TCG_API_KEY", "")}
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
