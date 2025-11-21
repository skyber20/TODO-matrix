FROM python:3.11-slim

WORKDIR /app-todo-list

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir ./data/

COPY app/ ./app/

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import requests; import sys; r = requests.get('http://localhost:8000/health', timeout=5); \
    sys.exit(0) if r.status_code == 200 else sys.exit(1)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]