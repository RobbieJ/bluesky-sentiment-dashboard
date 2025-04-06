import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sentiment_analysis import analyze_sentiment

# PostgreSQL connection using SQLAlchemy
DB_URI = "postgresql://user:pass@postgres:5432/sentimentdb"
engine = create_engine(DB_URI)

# Load posts and analyze sentiment
def load_posts():
    try:
        query = "SELECT text, created_at FROM posts ORDER BY created_at DESC LIMIT 100;"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

# Streamlit UI
def main():
    st.set_page_config(page_title="Bluesky Sentiment Dashboard", layout="wide")
    st.title("📊 Bluesky Sentiment Dashboard")
    
    df = load_posts()
    
    if not df.empty:
        df['sentiment'] = df['text'].apply(analyze_sentiment)
        
        st.subheader("Latest Posts with Sentiment")
        st.dataframe(df[['created_at', 'sentiment', 'text']])

        st.subheader("📈 Sentiment Distribution")
        sentiment_counts = df['sentiment'].value_counts()
        st.bar_chart(sentiment_counts)
    else:
        st.warning("No posts available to display.")

if __name__ == "__main__":
    main()