# Machine Learning DevOps Engineer Nanodegree Program Projects

This repository contains the solutions for projects completed as part of Udacity's **Machine Learning DevOps Engineer Nanodegree Program**. This program focuses on teaching software engineering and DevOps skills necessary for integrating and managing machine learning models in production environments.

## 🎓 About the Course

**Udacity Machine Learning DevOps Engineer Nanodegree Program** aims to teach software engineering and DevOps skills necessary for integrating and managing machine learning models in production environments. The program covers:

- **Clean Code Principles**: PEP8 standards, modular code structure, documentation
- **Version Control**: Git usage, branch strategies, code review processes
- **Testing & Debugging**: Unit tests, integration tests, logging
- **Model Deployment**: Containerization (Docker), cloud deployment, API development
- **Model Monitoring**: Performance monitoring, data drift detection, model retraining
- **MLOps Pipelines**: End-to-end ML pipelines, CI/CD, automation
- **Cloud Platforms**: AWS, Azure, GCP integration
- **Microservices**: API development with FastAPI, Flask

## 📚 Projects

This repository contains the following 4 main projects:

### 1. [Predict Customer Churn with Clean Code](./predict_customer_churn_with_clean_code/)
**Customer Churn Prediction - Clean Code Implementation**

This project develops a machine learning model to predict credit card customer churn. The project emphasizes clean and modular code writing, code efficiency, documentation, and debugging best practices.

**Features:**
- Modular function structure (`churn_library.py`)
- Comprehensive logging and testing system
- EDA visualizations and model evaluation
- PEP8 code quality standards
- PyLint and AutoPEP8 integration

### 2. [Build ML Pipeline for Short-Term Rental Prices](./build-ml-pipeline-for-short-term-rental-prices/)
**Short-Term Rental Price Prediction ML Pipeline**

This project develops an end-to-end ML pipeline for predicting short-term rental prices using NYC Airbnb data. The project aims to automate data engineering, model training, evaluation, and deployment processes.

**Features:**
- MLflow experiment tracking
- Weights & Biases integration
- Hyperparameter optimization
- Automated data validation
- Model versioning and deployment
- Comprehensive monitoring

### 3. [ML Model to Cloud Application Platform with FastAPI](./ml_model_to_cloud_application_platform_with_FastAPI/)
**Cloud Application Platform with FastAPI**

This project integrates a machine learning model for income prediction using census data into a cloud application platform using FastAPI.

**Features:**
- FastAPI framework for modern API development
- RESTful API endpoints
- Interactive API documentation (Swagger UI)
- Comprehensive testing suite
- CI/CD pipeline (GitHub Actions)
- Cloud deployment (Render.com)
- Type hints and Pydantic models

### 4. [Dynamic Risk Assessment System](./dynamic-risk-assessment-system/)
**Dynamic Risk Assessment System**

This project develops a comprehensive machine learning system for predicting corporate client attrition risk with automated monitoring, retraining, and deployment capabilities.

**Features:**
- Automated data ingestion
- Model training and scoring
- Production deployment
- Comprehensive diagnostics
- API endpoints (Flask)
- Automated retraining pipeline
- Cron job automation
- Performance monitoring

## 🏗️ Repository Structure

```
machine-learning-devops-projects/
├── README.md                                    # Main README file
├── docker/                                      # Docker configuration files
│   ├── Dockerfile                              # Docker configuration
│   ├── docker-compose.yml                     # Docker Compose setup
│   ├── .dockerignore                          # Docker ignore file
│   └── README.md                              # Docker documentation
├── predict_customer_churn_with_clean_code/      # Project 1: Customer Churn Prediction
├── build-ml-pipeline-for-short-term-rental-prices/  # Project 2: ML Pipeline
├── ml_model_to_cloud_application_platform_with_FastAPI/  # Project 3: FastAPI Application
└── dynamic-risk-assessment-system/              # Project 4: Risk Assessment System
```

## 🚀 Installation and Usage

Each project can be run independently in its own folder. Each project has its own `requirements.txt` file and detailed README.

### General Installation

#### Option 1: Using Conda (Recommended)
```bash
# Clone the repository
git clone https://github.com/your_username/machine-learning-devops-projects.git
cd machine-learning-devops-projects

# For ML Pipeline project
cd build-ml-pipeline-for-short-term-rental-prices
conda env create -f environment.yml
conda activate nyc_airbnb_dev
```

#### Option 2: Using Docker
```bash
# Clone the repository
git clone https://github.com/your_username/machine-learning-devops-projects.git
cd machine-learning-devops-projects

# Build Docker image
docker build -f docker/Dockerfile -t ml-devops-projects .

# Run specific services
docker-compose -f docker/docker-compose.yml up fastapi-app      # FastAPI service on port 8000
docker-compose -f docker/docker-compose.yml up risk-assessment  # Flask service on port 5000
docker-compose -f docker/docker-compose.yml up ml-pipeline      # ML Pipeline service
```

#### Option 3: Using pip
```bash
# Clone the repository
git clone https://github.com/your_username/machine-learning-devops-projects.git
cd machine-learning-devops-projects

# Install dependencies for each project
cd predict_customer_churn_with_clean_code
pip install -r requirements.txt
```

## 🛠️ Technologies Used

- **Python**: Main programming language
- **Machine Learning**: scikit-learn, pandas, numpy
- **MLOps**: MLflow, Weights & Biases
- **API Development**: FastAPI, Flask
- **Testing**: pytest, unittest
- **Code Quality**: PyLint, AutoPEP8, flake8
- **Containerization**: Docker, Docker Compose
- **Cloud Platforms**: Render.com, AWS
- **CI/CD**: GitHub Actions
- **Monitoring**: Custom logging, performance tracking

## 📊 Project Metrics

- **Total Projects**: 4
- **Code Quality**: PEP8 compliant
- **Test Coverage**: Comprehensive test suites
- **Documentation**: Detailed README for each project
- **Deployment**: Cloud-ready applications

## 🎯 Skills Learned

The following skills were acquired through this program:

1. **Clean Code Principles**: Writing modular, readable, and maintainable code
2. **MLOps Best Practices**: Model lifecycle management, versioning, monitoring
3. **API Development**: RESTful API design and development
4. **Cloud Deployment**: Deployment to modern cloud platforms
5. **CI/CD Pipelines**: Automated testing and deployment processes
6. **Monitoring & Logging**: System monitoring in production environments
7. **Data Engineering**: ETL pipelines and data validation
8. **Model Management**: Model training, evaluation, and deployment

## 📝 License

These projects were developed as part of the Udacity Machine Learning DevOps Engineer Nanodegree Program and are for educational purposes.

## 🤝 Contributing

This repository is for educational purposes. Feel free to fork and experiment with different approaches!

## 📞 Contact

For questions about the projects, please use GitHub Issues.

---

**Note**: This repository has been cleaned of personal tokens and sensitive information. WANDB project links and previous GitHub repository links have been removed. Individual README files for each project and a general README file have been added.