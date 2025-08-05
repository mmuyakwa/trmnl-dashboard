FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install uv first for better caching
RUN pip install --no-cache-dir uv

# Copy requirements first for better caching
COPY pyproject.toml .

# Install Python dependencies using uv with caching
RUN uv pip install --system --no-cache-dir -e .

# Copy application code
COPY app/ .
COPY .env .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run application
CMD ["python", "app.py"]