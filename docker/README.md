# Docker Configuration

This directory contains Docker configuration files for running the Machine Learning DevOps projects in containerized environments.

## 📁 Files

- `Dockerfile` - Main Docker configuration for building the project image
- `docker-compose.yml` - Docker Compose configuration for running multiple services
- `.dockerignore` - Files and directories to exclude from Docker build context
- `README.md` - This documentation file

## 🚀 Quick Start

### Build the Docker Image
```bash
# From the project root directory
docker build -f docker/Dockerfile -t ml-devops-projects .
```

### Run with Docker Compose
```bash
# From the project root directory
docker-compose -f docker/docker-compose.yml up
```

### Run Individual Services
```bash
# FastAPI Service (port 8000)
docker-compose -f docker/docker-compose.yml up fastapi-app

# Flask Risk Assessment Service (port 5000)
docker-compose -f docker/docker-compose.yml up risk-assessment

# ML Pipeline Service
docker-compose -f docker/docker-compose.yml up ml-pipeline
```

## 🛠️ Services

### FastAPI App
- **Port**: 8000
- **Project**: Census Income Prediction API
- **Command**: `python main.py`
- **Working Directory**: `/app/ml_model_to_cloud_application_platform_with_FastAPI`

### Risk Assessment
- **Port**: 5000
- **Project**: Dynamic Risk Assessment System
- **Command**: `python app.py`
- **Working Directory**: `/app/dynamic-risk-assessment-system`

### ML Pipeline
- **Project**: NYC Airbnb Price Prediction Pipeline
- **Command**: `python main.py`
- **Working Directory**: `/app/build-ml-pipeline-for-short-term-rental-prices`

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose installed on your system
- Sufficient disk space for Python packages and model files

## 🔧 Customization

### Environment Variables
You can customize the services by modifying the `docker-compose.yml` file:

```yaml
environment:
  - PYTHONPATH=/app
  - WANDB_PROJECT=your_project_name
  - WANDB_ENTITY=your_entity_name
```

### Volume Mounts
The services are configured with volume mounts for development:
- Source code is mounted for live development
- Model artifacts and data directories are mounted for persistence

### Port Configuration
Modify the port mappings in `docker-compose.yml` if needed:
```yaml
ports:
  - "8000:8000"  # FastAPI
  - "5000:5000"  # Flask
```

## 🐛 Troubleshooting

### Build Issues
- Ensure all requirements.txt files are present
- Check that the Dockerfile paths are correct
- Verify Python version compatibility

### Runtime Issues
- Check container logs: `docker-compose logs [service-name]`
- Verify port availability
- Ensure volume mounts are working correctly

### Memory Issues
- Large model files may require additional memory
- Consider using `.dockerignore` to exclude unnecessary files
- Monitor Docker resource usage

## 📝 Notes

- The Docker image includes all necessary Python dependencies
- Model files and artifacts are excluded from the build context (see `.dockerignore`)
- Services are configured for development with volume mounts
- For production deployment, consider using multi-stage builds
