# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY build-ml-pipeline-for-short-term-rental-prices/requirements.txt ./build-ml-pipeline-for-short-term-rental-prices/
COPY ml_model_to_cloud_application_platform_with_FastAPI/requirements.txt ./ml_model_to_cloud_application_platform_with_FastAPI/
COPY dynamic-risk-assessment-system/requirements.txt ./dynamic-risk-assessment-system/

# Install Python dependencies
RUN pip install --no-cache-dir -r build-ml-pipeline-for-short-term-rental-prices/requirements.txt
RUN pip install --no-cache-dir -r ml_model_to_cloud_application_platform_with_FastAPI/requirements.txt
RUN pip install --no-cache-dir -r dynamic-risk-assessment-system/requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose ports for different services
EXPOSE 8000 5000

# Default command (can be overridden)
CMD ["python", "--version"]
