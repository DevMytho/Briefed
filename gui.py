# ─────────────────────────────────────────
#  Briefed — gui.py
#  Main Tkinter UI
# ─────────────────────────────────────────

import tkinter as tk
from tkinter import ttk
from news import fetch_headlines
from sentiment import analyse, overall_sentiment
from config import (
    APP_NAME, REFRESH_INTERVAL, CATEGORIES, DEFAULT_CATEGORY,
    BG_COLOR, SURFACE_COLOR, BORDER_COLOR,
    TEXT_PRIMARY, TEXT_MUTED, ACCENT_COLOR, GAUGE_BG,
    POSITIVE_COLOR, NEGATIVE_COLOR, NEUTRAL_COLOR,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_HEADLINE, FONT_SIZE_SMALL
)


class BriefedApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("780x620")
        self.minsize(680, 500)
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)

        self.current_category = tk.StringVar(value=DEFAULT_CATEGORY)
        self._after_id = None  # For cancelling auto-refresh

        self._build_ui()
        self.load_news()

    # ── UI Builder ────────────────────────────────────────────────────────────

    def _build_ui(self):
        """Build all UI sections top to bottom."""
        self._build_header()
        self._build_gauge()
        self._build_categories()
        self._build_headline_list()
        self._build_footer()

    def _build_header(self):
        header = tk.Frame(self, bg=BG_COLOR, pady=16)
        header.pack(fill="x", padx=24)

        tk.Label(
            header,
            text=APP_NAME,
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(side="left")

        self.refresh_btn = tk.Button(
            header,
            text="↻ Refresh",
            font=(FONT_FAMILY, 10),
            bg=SURFACE_COLOR,
            fg=ACCENT_COLOR,
            activebackground=BORDER_COLOR,
            activeforeground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.load_news,
        )
        self.refresh_btn.pack(side="right")

        self.status_label = tk.Label(
            header,
            text="Loading...",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            bg=BG_COLOR,
            fg=TEXT_MUTED,
        )
        self.status_label.pack(side="right", padx=12)

    def _build_gauge(self):
        """Sentiment index bar at the top."""
        gauge_frame = tk.Frame(self, bg=SURFACE_COLOR, pady=14)
        gauge_frame.pack(fill="x", padx=24, pady=(0, 8))

        top_row = tk.Frame(gauge_frame, bg=SURFACE_COLOR)
        top_row.pack(fill="x", padx=16)

        tk.Label(
            top_row,
            text="Overall Sentiment",
            font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            bg=SURFACE_COLOR,
            fg=TEXT_MUTED,
        ).pack(side="left")

        self.gauge_label = tk.Label(
            top_row,
            text="—",
            font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            bg=SURFACE_COLOR,
            fg=TEXT_PRIMARY,
        )
        self.gauge_label.pack(side="right")

        # Progress bar canvas
        self.gauge_canvas = tk.Canvas(
            gauge_frame,
            height=10,
            bg=GAUGE_BG,
            highlightthickness=0,
        )
        self.gauge_canvas.pack(fill="x", padx=16, pady=(8, 0))

    def _build_categories(self):
        """Category filter buttons."""
        cat_frame = tk.Frame(self, bg=BG_COLOR, pady=6)
        cat_frame.pack(fill="x", padx=24)

        for cat in CATEGORIES:
            btn = tk.Radiobutton(
                cat_frame,
                text=cat,
                variable=self.current_category,
                value=cat,
                command=self.load_news,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=BG_COLOR,
                fg=TEXT_MUTED,
                selectcolor=SURFACE_COLOR,
                activebackground=BG_COLOR,
                activeforeground=TEXT_PRIMARY,
                indicatoron=False,
                relief="flat",
                padx=10,
                pady=4,
                cursor="hand2",
            )
            btn.pack(side="left", padx=2)

    def _build_headline_list(self):
        """Scrollable list of headlines."""
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=24, pady=8)

        # Canvas + scrollbar for scrollable area
        self.canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _build_footer(self):
        footer = tk.Frame(self, bg=SURFACE_COLOR, pady=8)
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="Powered by NewsAPI + VADER  •  Built by Devvv",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            bg=SURFACE_COLOR,
            fg=TEXT_MUTED,
        ).pack()

    # ── Data Loading ──────────────────────────────────────────────────────────

    def load_news(self):
        """Fetch headlines and re-render the UI."""
        # Cancel any pending auto-refresh
        if self._after_id:
            self.after_cancel(self._after_id)

        self.status_label.config(text="Fetching...")
        self.refresh_btn.config(state="disabled")
        self.update()

        category = self.current_category.get()
        headlines = fetch_headlines(category)

        if not headlines:
            self.status_label.config(text="No headlines found.")
        else:
            self.status_label.config(text=f"{len(headlines)} headlines  •  {category}")

        self._render_gauge(headlines)
        self._render_headlines(headlines)

        self.refresh_btn.config(state="normal")

        # Schedule next auto-refresh
        self._after_id = self.after(REFRESH_INTERVAL, self.load_news)

    # ── Rendering ─────────────────────────────────────────────────────────────

    def _render_gauge(self, headlines: list[dict]):
        """Update the sentiment bar and label."""
        result = overall_sentiment(headlines)
        pct = result["score_pct"]
        color = result["color"]
        label = result["label"]

        self.gauge_label.config(
            text=f"{result['emoji']}  {label}  ({pct}%)",
            fg=color,
        )

        # Draw the bar
        self.gauge_canvas.update_idletasks()
        width = self.gauge_canvas.winfo_width()
        bar_width = int(width * pct / 100)

        self.gauge_canvas.delete("all")
        self.gauge_canvas.create_rectangle(0, 0, bar_width, 10, fill=color, outline="")

    def _render_headlines(self, headlines: list[dict]):
        """Clear and repopulate the headline list."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not headlines:
            tk.Label(
                self.scroll_frame,
                text="No headlines to display. Check your API key or internet connection.",
                font=(FONT_FAMILY, FONT_SIZE_HEADLINE),
                bg=BG_COLOR,
                fg=TEXT_MUTED,
                wraplength=600,
            ).pack(pady=40)
            return

        for item in headlines:
            result = analyse(item["title"])
            self._render_headline_card(item, result)

    def _render_headline_card(self, item: dict, sentiment: dict):
        """Render a single headline card."""
        card = tk.Frame(
            self.scroll_frame,
            bg=SURFACE_COLOR,
            pady=10,
            padx=14,
        )
        card.pack(fill="x", pady=3)

        # Top row: emoji + sentiment label + source
        top = tk.Frame(card, bg=SURFACE_COLOR)
        top.pack(fill="x")

        tk.Label(
            top,
            text=f"{sentiment['emoji']}  {sentiment['label']}",
            font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            bg=SURFACE_COLOR,
            fg=sentiment["color"],
        ).pack(side="left")

        tk.Label(
            top,
            text=item["source"],
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            bg=SURFACE_COLOR,
            fg=TEXT_MUTED,
        ).pack(side="right")

        # Headline text
        tk.Label(
            card,
            text=item["title"],
            font=(FONT_FAMILY, FONT_SIZE_HEADLINE),
            bg=SURFACE_COLOR,
            fg=TEXT_PRIMARY,
            wraplength=680,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def run():
    app = BriefedApp()
    app.mainloop()