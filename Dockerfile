
FROM python:3.11-slim

WORKDIR /app
COPY app /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
