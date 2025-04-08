# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt stopwords

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p instance logs uploads

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application with Waitress
CMD ["python", "-m", "waitress", "--host=0.0.0.0", "--port=8000", "run:run(env='production')"]
