FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install PromptShield package
RUN pip install -e .

# Expose port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

