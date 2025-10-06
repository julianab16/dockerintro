FROM python:3.12-alpine
WORKDIR /app

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create log directory and set permissions
RUN mkdir -p /var/log/app && chown -R app:app /var/log/app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD wget -qO- http://localhost:8080/health >/dev/null || exit 1

# Start the application
CMD ["python", "/app/app.py"]