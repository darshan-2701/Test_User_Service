# ───────────── Base Python Image ─────────────
FROM python:3.13-slim

# Prevent Python buffer
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run app (uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]