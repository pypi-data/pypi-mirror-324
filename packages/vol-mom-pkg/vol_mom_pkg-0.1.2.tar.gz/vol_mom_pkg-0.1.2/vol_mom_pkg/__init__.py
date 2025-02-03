from .signals import calculate_portfolios
from .trade import place_orders
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Use the correct variable names expected by Alpaca
APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
APCA_API_BASE_URL = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")
