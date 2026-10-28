FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends chromium ca-certificates fonts-liberation && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data && useradd -m -u 10001 agent && chown -R agent:agent /app
USER agent
ENV HOST=0.0.0.0 PORT=8000 DATA_DIR=/app/data
EXPOSE 8000
CMD ["python", "-m", "falvorn"]
