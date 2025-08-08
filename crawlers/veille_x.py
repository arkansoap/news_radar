import argparse
from rich.console import Console
from sqlalchemy.orm import Session
from typing import List

from repositories.news_radar_X_post import save
from services.veille_X.scraping_X_to_json import get_tweets
from schemas import NewsRadarXPostWrite
from database import get_session  # à adapter selon ta gestion de session

console = Console()


def get_and_save_posts_X(db: Session, username: str, limit: int):
    posts = get_tweets(username=username, limit=limit)
    for post in posts:
        post_obj = NewsRadarXPostWrite(
            username=post.get("username"),
            text_=post.get("text_"),
            link=post.get("link"),
            date=post.get("date"),
        )
        save(db=db, post=post_obj)


def main(usernames: List[str], limit: int):
    db: Session = get_session()
    try:
        for username in usernames:
            print(f"Traitement pour @{username} (limit={limit})...")
            try:
                get_and_save_posts_X(db, username, limit)
            except Exception as e:
                print(f"Erreur lors du traitement de @{username} : {e}")
                console.print_exception()
                db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape and save tweets for one or several usernames."
    )
    parser.add_argument(
        "-u",
        "--usernames",
        nargs="+",
        default=["elonmusk", "nasa", "github"],  # liste par défaut
        help="Liste des usernames à scraper (ex: -u elonmusk nasa)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help="Nombre max de posts à récupérer par username",
    )
    args = parser.parse_args()

    main(usernames=args.usernames, limit=args.limit)
