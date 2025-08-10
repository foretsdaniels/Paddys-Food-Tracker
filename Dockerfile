# ============================================================================
# Restaurant Ingredient Tracker - Production Docker Image
# ============================================================================
# 
# This Dockerfile creates a production-ready container for the Streamlit
# restaurant ingredient tracking application with:
# - Multi-stage build for smaller final image
# - Security best practices (non-root user)
# - Optimized Python dependencies
# - Health checks for container monitoring
# - Proper logging configuration

# ============================================================================
# Build Stage - Install dependencies and prepare application
# ============================================================================
FROM python:3.11-slim as builder

# Set build arguments for customization
ARG PYTHON_VERSION=3.11
ARG APP_USER=streamlit
ARG APP_UID=1000
ARG APP_GID=1000

# Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create application user and group for security
RUN groupadd -g ${APP_GID} ${APP_USER} && \
    useradd -u ${APP_UID} -g ${APP_GID} -m -s /bin/bash ${APP_USER}

# Set working directory
WORKDIR /app

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .

# ============================================================================
# Production Stage - Create minimal runtime image
# ============================================================================
FROM python:3.11-slim as production

# Set build arguments (repeated for production stage)
ARG APP_USER=streamlit
ARG APP_UID=1000
ARG APP_GID=1000

# Set production environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true

# Install minimal system dependencies for runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create application user and group (matching builder stage)
RUN groupadd -g ${APP_GID} ${APP_USER} && \
    useradd -u ${APP_UID} -g ${APP_GID} -m -s /bin/bash ${APP_USER}

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY --chown=${APP_USER}:${APP_USER} app.py ./
COPY --chown=${APP_USER}:${APP_USER} sample_*.csv ./
COPY --chown=${APP_USER}:${APP_USER} README.md ./

# Create necessary directories with proper permissions
RUN mkdir -p /app/data /app/logs /app/exports && \
    chown -R ${APP_USER}:${APP_USER} /app

# Switch to non-root user for security
USER ${APP_USER}

# Expose Streamlit port
EXPOSE 8501

# Add health check to monitor container health
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Use tini as init system for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default command to run the Streamlit application
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.fileWatcherType=none", \
     "--browser.gatherUsageStats=false"]