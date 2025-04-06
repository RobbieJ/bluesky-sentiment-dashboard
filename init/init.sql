
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    uri TEXT NOT NULL,
    cid TEXT NOT NULL UNIQUE,
    author TEXT,
    text TEXT,
    created_at TIMESTAMP
);
