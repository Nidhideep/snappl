import requests
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Optional

@st.cache_data(ttl=3600)  # Cache exchange rates for 1 hour
def fetch_exchange_rates(base_currency: str = "USD") -> Dict:
    """
    Fetch exchange rates from exchangerate.host API
    """
    try:
        response = requests.get(f"https://api.exchangerate.host/latest?base={base_currency}")
        data = response.json()
        if data.get("success", True):  # API returns success field
            return {
                "success": True,
                "rates": data.get("rates", {}),
                "date": data.get("date"),
                "error": None
            }
        return {
            "success": False,
            "rates": {},
            "date": None,
            "error": "Failed to fetch exchange rates"
        }
    except Exception as e:
        return {
            "success": False,
            "rates": {},
            "date": None,
            "error": f"API Error: {str(e)}"
        }

def get_currency_options() -> Dict[str, str]:
    """
    Returns an expanded list of currency options with their descriptions
    """
    return {
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'AUD': 'Australian Dollar',
        'CAD': 'Canadian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'HKD': 'Hong Kong Dollar',
        'NZD': 'New Zealand Dollar',
        'SEK': 'Swedish Krona',
        'KRW': 'South Korean Won',
        'SGD': 'Singapore Dollar',
        'NOK': 'Norwegian Krone',
        'MXN': 'Mexican Peso',
        'INR': 'Indian Rupee',
        'RUB': 'Russian Ruble',
        'ZAR': 'South African Rand',
        'BRL': 'Brazilian Real',
        'AED': 'UAE Dirham'
    }

def convert_price(amount: float, from_currency: str, to_currency: str) -> Dict:
    """
    Convert price from one currency to another
    """
    if from_currency == to_currency:
        return {
            "success": True,
            "amount": amount,
            "rate": 1.0,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

    rates = fetch_exchange_rates(from_currency)
    if not rates["success"]:
        return {
            "success": False,
            "amount": amount,
            "error": rates["error"]
        }

    try:
        conversion_rate = rates["rates"][to_currency]
        converted_amount = amount * conversion_rate
        return {
            "success": True,
            "amount": converted_amount,
            "rate": conversion_rate,
            "date": rates["date"]
        }
    except KeyError:
        return {
            "success": False,
            "amount": amount,
            "error": f"Currency {to_currency} not found in exchange rates"
        }

def format_currency(amount: float, currency: str) -> str:
    """
    Format currency amount with proper symbol and decimals
    """
    currency_symbols = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥',
        'AUD': 'A$', 'CAD': 'C$', 'CHF': 'Fr.',
        'CNY': '¥', 'HKD': 'HK$', 'NZD': 'NZ$'
    }

    symbol = currency_symbols.get(currency, currency + ' ')
    
    # Special case for currencies that don't typically show decimals
    if currency in ['JPY', 'KRW']:
        return f"{symbol}{int(amount):,}"
    
    return f"{symbol}{amount:,.2f}"
