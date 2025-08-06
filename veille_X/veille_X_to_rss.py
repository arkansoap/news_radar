import json
import email.utils
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
from playwright.sync_api import sync_playwright


def get_tweets(username: str, limit: int = 10):
    tweets = []
    url = f"https://x.com/{username}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def handle_response(response):
            # On cible uniquement les requêtes JSON qui contiennent les tweets
            if "UserTweets" in response.url:
                try:
                    data = response.json()
                except:
                    return

                instructions = (
                    data.get("data", {})
                    .get("user", {})
                    .get("result", {})
                    .get("timeline", {})
                    .get("timeline", {})
                    .get("instructions", [])
                )

                for instr in instructions:
                    if instr.get("type") == "TimelineAddEntries":
                        for entry in instr.get("entries", []):
                            content = entry.get("content", {})
                            item_content = content.get("itemContent", {})
                            tweet_res = item_content.get("tweet_results", {}).get(
                                "result", {}
                            )

                            if not tweet_res or "legacy" not in tweet_res:
                                continue

                            legacy = tweet_res["legacy"]
                            full_text = legacy.get("full_text")
                            created_at = legacy.get("created_at")
                            tweet_id = legacy.get("id_str")

                            if not full_text or not created_at:
                                continue

                            # Conversion date avec timezone
                            dt = email.utils.parsedate_to_datetime(created_at)

                            tweets.append(
                                {
                                    "text": full_text,
                                    "link": f"https://x.com/{username}/status/{tweet_id}",
                                    "date": dt,
                                }
                            )

        # On écoute toutes les réponses réseau
        page.on("response", handle_response)

        # On ouvre le profil X
        page.goto(url, timeout=60000)
        page.wait_for_selector("article", timeout=15000)

        # On scrolle un peu pour charger plus de tweets si nécessaire
        for _ in range(2):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        browser.close()

    # On limite le nombre de tweets renvoyés
    return tweets[:limit]


def generate_rss(username: str, tweets):
    fg = FeedGenerator()
    fg.title(f"Tweets de {username}")
    fg.link(href=f"https://x.com/{username}", rel="alternate")
    fg.description(f"Flux RSS non officiel du compte X @{username}")

    for tw in tweets:
        fe = fg.add_entry()
        fe.title(tw["text"][:60] + "..." if len(tw["text"]) > 60 else tw["text"])
        fe.link(href=tw["link"])
        fe.description(tw["text"])
        fe.pubDate(tw["date"].astimezone(timezone.utc))

    return fg.rss_str(pretty=True)


if __name__ == "__main__":
    username = "elonmusk"  # ⚠️ changer ici
    tweets = get_tweets(username, limit=5)
    rss_feed = generate_rss(username, tweets)

    with open("tweets.xml", "wb") as f:
        f.write(rss_feed)

    print(f"✅ Flux RSS généré : tweets.xml ({len(tweets)} tweets)")
