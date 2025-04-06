
# streamlit_app.py
import streamlit as st
import psycopg2
import pandas as pd
from sentiment_analysis import analyze_sentiment

DB_PARAMS = {
    'dbname': 'sentimentdb',
    'user': 'user',
    'password': 'pass',
    'host': 'postgres',
    'port': 5432
}

def load_posts():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        query = "SELECT text, created_at FROM posts ORDER BY created_at DESC LIMIT 100;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

def main():
    st.title("Bluesky Sentiment Dashboard")
    df = load_posts()
    if not df.empty:
        df['sentiment'] = df['text'].apply(analyze_sentiment)
        st.write(df)
        st.bar_chart(df['sentiment'].value_counts())
    else:
        st.warning("No posts available to display.")

if __name__ == "__main__":
    main()
