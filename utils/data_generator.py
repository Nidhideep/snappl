import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_card_data(num_cards=50):
    card_names = [
        "Blue-Eyes White Dragon", "Black Lotus", "Charizard", "Pikachu",
        "Dark Magician", "Mox Pearl", "Time Walk", "Blastoise",
        "Red-Eyes Black Dragon", "Ancestral Recall", "Mewtwo", "Venusaur"
    ]
    
    conditions = ["Mint", "Near Mint", "Excellent", "Good", "Poor"]
    sets = ["Base Set", "Alpha", "Beta", "Unlimited", "1st Edition"]
    
    data = []
    for _ in range(num_cards):
        name = np.random.choice(card_names)
        condition = np.random.choice(conditions)
        card_set = np.random.choice(sets)
        
        base_price = np.random.uniform(100, 10000)
        current_price = base_price * (1 + np.random.uniform(-0.2, 0.2))
        
        data.append({
            "name": name,
            "condition": condition,
            "set": card_set,
            "price": round(current_price, 2),
            "last_sold": datetime.now() - timedelta(days=np.random.randint(1, 30)),
            "market_trend": np.random.choice(["↑", "↓", "→"]),
            "popularity_score": np.random.randint(1, 100),
            "available_quantity": np.random.randint(1, 50)
        })
    
    return pd.DataFrame(data)

def generate_price_history(days=30):
    dates = pd.date_range(end=datetime.now(), periods=days)
    prices = [100]
    for _ in range(days-1):
        change = np.random.uniform(-5, 5)
        new_price = max(prices[-1] * (1 + change/100), 10)
        prices.append(new_price)
    
    return pd.DataFrame({
        "date": dates,
        "price": prices
    })

def generate_market_metrics():
    return {
        "total_listings": np.random.randint(1000, 5000),
        "avg_price": round(np.random.uniform(500, 2000), 2),
        "daily_volume": np.random.randint(100, 1000),
        "price_trend": round(np.random.uniform(-10, 10), 2)
    }
