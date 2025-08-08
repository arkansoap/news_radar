import email.utils
import json
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright


# TODO Gestion proxies - voir fin de conv GPT "compléter CRUD ... "
def get_tweets(username: str, limit: int = 10):
    tweets = []
    url = f"https://x.com/{username}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def handle_response(response):
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

                            dt = email.utils.parsedate_to_datetime(created_at)

                            tweets.append(
                                {
                                    "username": username,
                                    "text_": full_text,
                                    "link": f"https://x.com/{username}/status/{tweet_id}",
                                    "date": dt.isoformat(),
                                }
                            )

        page.on("response", handle_response)
        page.goto(url, timeout=60000)
        page.wait_for_selector("article", timeout=15000)

        # Charger un peu plus de tweets
        for _ in range(2):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        browser.close()

    return tweets[:limit]


if __name__ == "__main__":
    username = "elonmusk"  # ⚠️ changer ici
    tweets = get_tweets(username, limit=5)

    # Affichage brut en JSON
    print(json.dumps(tweets, ensure_ascii=False, indent=2))
