FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (better Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose app port (documentation + clarity)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
