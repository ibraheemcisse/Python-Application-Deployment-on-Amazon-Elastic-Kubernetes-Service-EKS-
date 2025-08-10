# Multi-stage Dockerfile for Flask application
# Stage 1: Build stage
FROM python:3.9-slim as builder

# Set build arguments
ARG APP_VERSION=1.0.0
ARG BUILD_DATE
ARG VCS_REF

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.9-slim as production

# Labels for metadata
LABEL maintainer="your-email@example.com" \
      version="${APP_VERSION}" \
      description="Flask application for EKS deployment" \
      build-date="${BUILD_DATE}" \
      vcs-ref="${VCS_REF}"

# Install runtime dependencies and security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r flask && useradd -r -g flask -u 1000 flask

# Create application directory with proper permissions
WORKDIR /app
RUN chown -R flask:flask /app

# Create necessary directories for logs and temp files
RUN mkdir -p /tmp /var/log && \
    chown -R flask:flask /tmp /var/log

# Copy Python packages from builder stage
COPY --from=builder --chown=flask:flask /root/.local /home/flask/.local

# Copy application files
COPY --chown=flask:flask app.py .
COPY --chown=flask:flask templates/ ./templates/
COPY --chown=flask:flask static/ ./static/

# Switch to non-root user
USER flask

# Add local Python packages to PATH
ENV PATH=/home/flask/.local/bin:$PATH

# Set Python environment variables
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Expose port (informational)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Use exec form for better signal handling
CMD ["python", "app.py"]
