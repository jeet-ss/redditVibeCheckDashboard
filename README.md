# Subreddit Vibe Check Dashboard

A simple Streamlit app that “checks the vibe” of a chosen subreddit by analyzing the sentiment of the top 50 **Hot** posts (via RSS). It uses VADER sentiment analysis on post **titles**.

---

## Features

- Select a subreddit (dropdown or custom input)
- Fetch top 50 **Hot** posts from the subreddit RSS feed
- Run sentiment analysis on each post title using VADER
- Display:
  - Overall vibe (Positive / Neutral / Negative)
  - Average sentiment score
  - Counts of positive / negative / neutral titles
  - A table of the individual post scores

---

## How it works

1. Build the RSS URL using the chosen sub reddit:
   `https://www.reddit.com/r/<subreddit>/hot.rss?limit=50`
2. Download the feed using `requests` with a browser User-Agent header
3. Parse RSS using `feedparser`
4. For each post title, compute VADER `compound` sentiment score:
   - **Positive** if `compound > 0.05`
   - **Negative** if `compound < -0.05`
   - **Neutral** otherwise
5. Aggregate scores and render dashboard metrics + a dataframe.

---

## Setup

### Prerequisites

- Python 3.9+ recommended
- Internet access (needed to fetch Reddit RSS feeds)

### Install dependencies

```bash
pip install streamlit requests feedparser vaderSentiment
