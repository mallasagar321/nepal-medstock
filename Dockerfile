FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY templates ./templates
ENV PORT=5000 DB_PATH=/data/medstock.db
VOLUME /data
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:5000/health')"
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} app:create_app()"]
