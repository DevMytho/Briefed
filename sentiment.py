# ─────────────────────────────────────────
#  Briefed — sentiment.py
#  Runs VADER sentiment analysis on headlines
# ─────────────────────────────────────────

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import (
    POSITIVE_THRESHOLD, NEGATIVE_THRESHOLD,
    POSITIVE_COLOR, NEGATIVE_COLOR, NEUTRAL_COLOR,
    POSITIVE_EMOJI, NEGATIVE_EMOJI, NEUTRAL_EMOJI
)

# Initialise once — no need to recreate for every headline
_analyzer = SentimentIntensityAnalyzer()


def analyse(headline: str) -> dict:
    """
    Run sentiment analysis on a single headline string.

    Returns a dict:
    {
        "compound": float,   # -1.0 to +1.0
        "label": str,        # "Positive", "Negative", or "Neutral"
        "emoji": str,        # 🟢 / 🔴 / ⚪
        "color": str,        # hex color string
        "score_pct": int,    # 0–100, normalised for the UI gauge
    }
    """
    scores = _analyzer.polarity_scores(headline)
    compound = scores["compound"]

    if compound >= POSITIVE_THRESHOLD:
        label = "Positive"
        emoji = POSITIVE_EMOJI
        color = POSITIVE_COLOR
    elif compound <= NEGATIVE_THRESHOLD:
        label = "Negative"
        emoji = NEGATIVE_EMOJI
        color = NEGATIVE_COLOR
    else:
        label = "Neutral"
        emoji = NEUTRAL_EMOJI
        color = NEUTRAL_COLOR

    # Normalise compound (-1 to +1) → percentage (0 to 100)
    score_pct = int((compound + 1) / 2 * 100)

    return {
        "compound": compound,
        "label": label,
        "emoji": emoji,
        "color": color,
        "score_pct": score_pct,
    }


def overall_sentiment(headlines: list[dict]) -> dict:
    """
    Calculate the overall sentiment index across all headlines.
    Takes the list of headline dicts (with 'title' key) from news.py.

    Returns same dict format as analyse(), representing the average.
    """
    if not headlines:
        return analyse("")  # Returns neutral for empty input

    total = sum(
        _analyzer.polarity_scores(h["title"])["compound"]
        for h in headlines
    )
    avg_compound = total / len(headlines)

    # Build a fake "headline" with the average compound to reuse analyse logic
    # We manually construct the result instead
    if avg_compound >= POSITIVE_THRESHOLD:
        label, emoji, color = "Positive", POSITIVE_EMOJI, POSITIVE_COLOR
    elif avg_compound <= NEGATIVE_THRESHOLD:
        label, emoji, color = "Negative", NEGATIVE_EMOJI, NEGATIVE_COLOR
    else:
        label, emoji, color = "Neutral", NEUTRAL_EMOJI, NEUTRAL_COLOR

    score_pct = int((avg_compound + 1) / 2 * 100)

    return {
        "compound": avg_compound,
        "label": label,
        "emoji": emoji,
        "color": color,
        "score_pct": score_pct,
    }