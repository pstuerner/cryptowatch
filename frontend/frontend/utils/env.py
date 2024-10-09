import os

OPENAI_KEY = os.getenv("OPENAI_KEY")
TOKENS_BASKET = [
    {"name": "Bitcoin", "ticker": "BTC"},
    {"name": "Ethereum", "ticker": "ETH"},
    {"name": "Binance", "ticker": "BNB"},
    {"name": "Solana", "ticker": "SOL"},
    {"name": "Ripple", "ticker": "XRP"},
    {"name": "Tron", "ticker": "TRX"},
    {"name": "Cardano", "ticker": "ADA"},
    {"name": "Avalanche", "ticker": "AVAX"}
]