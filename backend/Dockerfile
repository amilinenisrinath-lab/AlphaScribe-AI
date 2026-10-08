# Multi-stage Dockerfile: Python 3.11 + R + ggplot2 environment
FROM python:3.11-slim

# Install system dependencies & R runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    r-base \
    r-base-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install ggplot2 & jsonlite in R
RUN R -e "install.packages(c('ggplot2', 'jsonlite'), repos='https://cloud.r-project.org')"

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Expose FastAPI port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
