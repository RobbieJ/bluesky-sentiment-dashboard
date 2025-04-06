
# appview_client.py
# Pulls posts from Bluesky's AppView API for demo purposes

import requests
import psycopg2
from datetime import datetime

DB_PARAMS = {
    'dbname': 'sentimentdb',
    'user': 'user',
    'password': 'pass',
    'host': 'postgres',
    'port': 5432
}

def fetch_recent_posts():
    url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getTimeline"
    headers = {"User-Agent": "BlueskySentimentApp/0.1"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('feed', [])
    else:
        print("Failed to fetch posts:", response.status_code)
        return []

def store_post(post):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        record = post['post']
        cur.execute(
            """
            INSERT INTO posts (uri, cid, author, text, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (cid) DO NOTHING;
            """,
            (
                record.get('uri'),
                record.get('cid', record.get('uri')),
                record.get('author', {}).get('handle', 'unknown'),
                record.get('text', ''),
                record.get('indexedAt', datetime.utcnow().isoformat())
            )
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Database error:", e)

def main():
    posts = fetch_recent_posts()
    for p in posts:
        store_post(p)

if __name__ == "__main__":
    main()
