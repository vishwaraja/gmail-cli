# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY setup.py .

# Install the package
RUN pip install -e .

# Create directory for credentials and tokens
RUN mkdir -p /app/data

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash gmail-cli && \
    chown -R gmail-cli:gmail-cli /app
USER gmail-cli

# Set data directory as volume
VOLUME ["/app/data"]

# Set default command
ENTRYPOINT ["gmail"]
CMD ["--help"]
