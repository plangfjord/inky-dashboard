# apps/news/data.py

import feedparser
from datetime import datetime

FEEDS = [
    {"name": "NRK",           "url": "https://www.nrk.no/nyheter/siste.rss", "limit": 8, "priority": 1},
    {"name": "DN",            "url": "https://services.dn.no/api/feed/rss/?categories=nyheter&topics=finans,utenriks,politikk,teknologi,makro%C3%B8konomi,b%C3%B8rs,shipping", "limit": 8, "priority": 2},
    {"name": "TU",            "url": "https://www.tu.no/rss", "limit": 6, "priority": 3},
    {"name": "Reuters",       "url": "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen", "limit": 8, "priority": 10},
    {"name": "Bloomberg Tech", "url": "https://feeds.bloomberg.com/technology/news.rss", "limit": 6, "priority": 11},
]


def clean_title(title, source):
    """Renser og normaliserer tittel."""
    if not title:
        return "Untitled"
    
    title = title.strip()
    
    # Spesialrensning per kilde
    if source == "Reuters":
        title = title.replace(" - Reuters", "").replace(" | Reuters", "")
    if source == "TU":
        title = title.replace("[Ekstra] ", "")
    
    return " ".join(title.split())


def fetch_news():
    """Henter alle nyheter fra feedene. Returnerer alt (til AI/cache)."""
    all_items = []
    seen_titles = set()

    for feed in FEEDS:
        try:
            parsed = feedparser.parse(feed["url"])
            count = 0
            
            for entry in parsed.entries:
                if count >= feed["limit"]:
                    break

                title = clean_title(entry.get("title", ""), feed["name"])

                normalized = title.lower().strip()
                if normalized in seen_titles:
                    continue

                seen_titles.add(normalized)

                item = {
                    "source": feed["name"],
                    "title": title,
                    "link": entry.get("link", ""),
                    "priority": feed["priority"],
                    "fetched_at": datetime.now(),
                }
                all_items.append(item)
                count += 1

        except Exception as e:
            print(f"Feed error {feed['name']}: {e}")

    return all_items


def get_curated_news(all_items):
    """Returnerer kurert utvalg til visning på skjermen."""
    
    # Grupper nyheter per kilde
    by_source = {}
    for item in all_items:
        src = item["source"]
        by_source.setdefault(src, []).append(item)

    norwegian = []
    international = []

    # Norske nyheter - eksakt ønsket rekkefølge og mengde
    #2 nrk, 3 DN, 1 TU
    norwegian.extend(by_source.get("NRK", [])[:2])
    norwegian.extend(by_source.get("DN", [])[:3])
    norwegian.extend(by_source.get("TU", [])[:1])

    # Internasjonale nyheter
    # 3 Reuters, 2 Bloomberg Tech
    international.extend(by_source.get("Reuters", [])[:3])
    international.extend(by_source.get("Bloomberg Tech", [])[:2])

    curated = norwegian + international

    return curated