# Snappl Pokemon Card Market Analysis

An interactive platform for Pokemon card enthusiasts to explore, analyze, and track trading card market trends with personalized insights.

## Features

- Real-time market data for Pokemon cards
- Multi-currency support with live conversion rates
- User session management
- Community collections sharing
- Collection rating system
- Card variant search and comparison

## Technologies Used

- Python 3.11
- Streamlit
- Pokemon TCG API
- Frankfurter Currency API

## Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Nidhideep/snappl.git
cd snappl
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
- Get a Pokemon TCG API key from https://dev.pokemontcg.io/
- Add it to your .streamlit/secrets.toml file:
```toml
POKEMON_TCG_API_KEY = "your-api-key"
```

4. Run the application:
```bash
streamlit run main.py
```

## Deployment on Render

1. Fork or clone this repository to your GitHub account
2. Sign up on render.com
3. Create a new Web Service
   - Connect your GitHub repository
   - Select the Python environment
   - The build and start commands are pre-configured in render.yaml
4. Add your environment variables:
   - Add POKEMON_TCG_API_KEY in the Render dashboard
5. Deploy your application

## Usage

1. Enter your name to start the application
2. Search for Pokemon cards by name
3. Select cards to add to your collection
4. View real-time market data and price conversions
5. Rate other users' collections
6. Track market trends and card availability

## Disclaimer

This tool is for entertainment purposes only. Actual card values depend on condition, authenticity, and market demand. Market prices can vary significantly from the estimates shown.

## License

MIT License