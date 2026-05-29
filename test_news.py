# test_news.py

from apps.news.data import fetch_news

news = fetch_news()

print("\n========== NEWS ==========\n")

for index, item in enumerate(news):

    print(
        f"{index + 1}. "
        f"[{item['source']}]"
    )

    print(item["title"])

    print()