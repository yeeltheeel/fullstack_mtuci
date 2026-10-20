FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt debugpy

COPY . .

EXPOSE 8000 5678

# Overridden by compose command: for dev. This is the prod default
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
