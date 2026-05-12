# ─────────────────────────────────────────
#  Briefed — config.py
#  All settings, constants, and API config
# ─────────────────────────────────────────
from dotenv import load_dotenv
import os

load_dotenv()
# ── NewsAPI ───────────────────────────────
# Get your free key at https://newsapi.org/
API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

# ── App Settings ─────────────────────────
APP_NAME = "Briefed"
REFRESH_INTERVAL = 300000  # 5 minutes in milliseconds
MAX_HEADLINES = 20         # Number of headlines to fetch per category

# ── News Categories ───────────────────────
CATEGORIES = ["General", "Technology", "Business", "Science", "Health", "Sports"]
DEFAULT_CATEGORY = "General"
COUNTRY = "in"  # Change to "in" for India, "gb" for UK etc.

# ── Sentiment Thresholds (VADER compound score) ───
# Compound score ranges from -1.0 (most negative) to +1.0 (most positive)
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05

# ── UI Colors ─────────────────────────────
BG_COLOR = "#0d1117"          # Main background
SURFACE_COLOR = "#161b22"     # Card / panel background
BORDER_COLOR = "#30363d"      # Subtle borders

TEXT_PRIMARY = "#e6edf3"      # Main text
TEXT_MUTED = "#8b949e"        # Secondary text

POSITIVE_COLOR = "#3fb950"    # Green
NEGATIVE_COLOR = "#f85149"    # Red
NEUTRAL_COLOR = "#8b949e"     # Gray

ACCENT_COLOR = "#58a6ff"      # Blue — buttons, highlights
GAUGE_BG = "#21262d"          # Sentiment bar background

# ── Sentiment Emojis ──────────────────────
POSITIVE_EMOJI = "🟢"
NEGATIVE_EMOJI = "🔴"
NEUTRAL_EMOJI  = "⚪"

# ── Font ──────────────────────────────────
FONT_FAMILY = "Helvetica"
FONT_SIZE_TITLE = 20
FONT_SIZE_HEADLINE = 11
FONT_SIZE_SMALL = 9