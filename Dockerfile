# Use official Python runtime as base
FROM python:3.11-slim

# Install system dependencies (if needed for file operations)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 streamlit && \
    chown -R streamlit:streamlit /app

# Copy requirements
COPY --chown=streamlit:streamlit requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=streamlit:streamlit . .

# Switch to non-root user
USER streamlit

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]