# ─────────────────────────────────────────
#  Briefed — news.py
#  Fetches latest headlines from NewsAPI
# ─────────────────────────────────────────

import requests
from config import API_KEY, MAX_HEADLINES

# Using /everything endpoint with India query — far more reliable
# than /top-headlines with country="in" on the free tier
EVERYTHING_URL = "https://newsapi.org/v2/everything"

def fetch_headlines(category: str = "general") -> list[dict]:
    """
    Fetch top headlines for a given category, focused on Indian news.
    Returns a list of dicts with 'title' and 'source'.
    Returns an empty list if the request fails.
    """

    # Build the search query
    if category.lower() == "general":
        query = "India"
    else:
        query = f"India {category}"

    params = {
        "apiKey": API_KEY,
        "q": query,
        "language": "en",
        "pageSize": MAX_HEADLINES,
        "sortBy": "publishedAt",  # Latest news first
    }

    try:
        response = requests.get(EVERYTHING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        headlines = []
        for article in data.get("articles", []):
            title = article.get("title", "").strip()
            source = article.get("source", {}).get("name", "Unknown")

            # Skip removed or empty articles
            if title and title != "[Removed]":
                headlines.append({
                    "title": title,
                    "source": source,
                })

        return headlines

    except requests.exceptions.ConnectionError:
        print("[Briefed] No internet connection.")
        return []

    except requests.exceptions.Timeout:
        print("[Briefed] Request timed out.")
        return []

    except requests.exceptions.HTTPError as e:
        print(f"[Briefed] HTTP error: {e}")
        return []

    except Exception as e:
        print(f"[Briefed] Unexpected error: {e}")
        return []