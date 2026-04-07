FROM python:3.12-slim

WORKDIR /app

# Set Python path to include src directory
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies (sem build-essential, usar wheels pré-compiladas)
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
