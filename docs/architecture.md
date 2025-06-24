# Architecture Overview

## System Components

### 1. Message Ingestion (Pub/Sub)
- Receives real-time messages from various sources
- Provides reliable message delivery and buffering
- Decouples message producers from processors

### 2. Stream Processing (Dataflow)
- Processes messages in real-time using Apache Beam
- Integrates with Google Natural Language API for sentiment analysis
- Enriches data with sentiment scores and timestamps
- Handles error processing and dead letter queues

### 3. Data Warehouse (BigQuery)
- Stores processed messages with sentiment analysis results
- Provides SQL interface for ad-hoc queries
- Supports real-time analytics and reporting
- Maintains separate tables for processed data and errors

### 4. Batch Analytics (Dataproc)
- Performs hourly aggregation of sentiment data
- Generates business intelligence reports
- Uses Apache Spark for large-scale data processing
- Creates trend analysis and statistical summaries

### 5. Data Lake (Cloud Storage)
- Stores analytics results in CSV format
- Provides cost-effective long-term storage
- Enables integration with external BI tools
- Maintains staging and temporary processing files

## Data Flow

```
Messages → Pub/Sub → Dataflow → BigQuery
                      ↓
                   Errors → Error Table
                      
BigQuery → Dataproc → Analytics Results → Cloud Storage
```

## Scalability Features

- **Auto-scaling**: Dataflow and Dataproc automatically scale based on workload
- **Serverless**: Managed services reduce operational overhead
- **Parallel Processing**: Distributed processing across multiple workers
- **Load Balancing**: Pub/Sub distributes messages across consumers

## Security

- **IAM Roles**: Fine-grained access control for each service
- **Service Accounts**: Dedicated accounts for pipeline components
- **VPC**: Network isolation and security
- **Encryption**: Data encrypted at rest and in transit
```

## Performance Optimization

- **Streaming Windows**: Configurable time windows for batch processing
- **Dead Letter Queues**: Handle failed message processing
- **Monitoring**: Real-time metrics and alerting
- **Cost Optimization**: Automatic resource scaling based on demand

## Service Dependencies

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Pub/Sub   │───▶│   Dataflow   │───▶│  BigQuery   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                    │
                           ▼                    ▼
                   ┌──────────────┐    ┌─────────────┐
                   │ Natural Lang │    │  Dataproc   │
                   │     API      │    └─────────────┘
                   └──────────────┘            │
                                              ▼
                                      ┌─────────────┐
                                      │Cloud Storage│
                                      └─────────────┘
```
```

## Complete `README.md` with Enhanced Content

```markdown:README.md
# Real-Time Sentiment Analytics Pipeline

[![CI/CD](https://github.com/YOUR_USERNAME/real-time-sentiment-analytics/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/real-time-sentiment-analytics/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)

A production-ready, scalable real-time sentiment analysis pipeline built on Google Cloud Platform that processes streaming messages, performs AI-powered sentiment analysis, and generates business intelligence reports.

## 🏗️ Architecture

```
Messages → Pub/Sub → Dataflow → BigQuery → Dataproc → Cloud Storage
           📡        🌊         📊         🔥        💾
```

## 🚀 Features

- **Real-time Processing**: Stream processing with Apache Beam
- **AI-Powered Analysis**: Google Natural Language API integration
- **Scalable Architecture**: Serverless and auto-scaling components
- **Business Intelligence**: Automated hourly trend analysis
- **Cost Optimized**: Pay-per-use serverless architecture
- **Production Ready**: Comprehensive error handling and monitoring

## Complete `docs/deployment.md`

```markdown:docs/deployment.md
# Deployment Guide

## Prerequisites

1. Google Cloud Platform account with billing enabled
2. gcloud CLI installed and configured
3. Python 3.8+ installed
4. Git installed

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/your-username/real-time-sentiment-analytics.git
cd real-time-sentiment-analytics
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env with your project details
```

### 3. Run Setup Script
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh your-project-id us-central1
```

### 4. Deploy Pipeline
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 📁 Project Structure

```
real-time-sentiment-analytics/
├── README.md
├── requirements.txt
├── setup.sh
├── config/
│   └── pipeline_config.yaml
├── src/
│   ├── pubsub/
│   │   └── message_publisher.py
│   ├── dataflow/
│   │   └── streaming_pipeline.py
│   └── dataproc/
│       └── batch_analytics.py
├── scripts/
│   ├── deploy.sh
│   └── cleanup.sh
├── tests/
│   └── test_pipeline.py
├── docs/
│   ├── architecture.md
│   └── deployment.md
└── .github/
    ├── workflows/
    │   └── ci.yml
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

## 🔧 Configuration

Update `config/pipeline_config.yaml` with your project details:

```yaml
project:
  id: "your-project-id"
  region: "us-central1"
  zone: "us-central1-a"

pubsub:
  topic: "message-topic"

bigquery:
  dataset: "analytics_results"
  table: "processed_messages"

storage:
  bucket: "your-project-id-pipeline"
```

## Manual Deployment Steps

### 1. Infrastructure Setup
```bash
# Enable APIs
```bash
gcloud services enable pubsub.googleapis.com dataflow.googleapis.com bigquery.googleapis.com dataproc.googleapis.com language.googleapis.com
```

# Create resources
```bash
# Pub/Sub Topic
gcloud pubsub topics create message-topic

# BigQuery Dataset
bq mk --location=us-central1 analytics_results

# Cloud Storage Bucket
gsutil mb -l us-central1 gs://your-project-pipeline

# Dataproc Cluster
gcloud dataproc clusters create analytics-cluster --region=us-central1
```

### 2. Deploy Components
```bash
# Upload code
gsutil -m cp -r src/ gs://your-project-pipeline/code/

# Start streaming pipeline
python src/dataflow/streaming_pipeline.py

# Submit batch job
gcloud dataproc jobs submit pyspark src/dataproc/batch_analytics.py --cluster=analytics-cluster
```

## 🚀 Usage

### 1. Start Streaming Pipeline
```bash
python src/dataflow/streaming_pipeline.py
```

### 2. Publish Messages
```bash
python src/pubsub/message_publisher.py
```

### 3. Run Batch Analytics
```bash
gcloud dataproc jobs submit pyspark src/dataproc/batch_analytics.py --cluster=analytics-cluster --region=us-central1
```

## 📊 Sample Output

```csv
window_start,window_end,avg_sentiment_score,avg_sentiment_magnitude,message_count
2025-06-23 10:00:00,2025-06-23 11:00:00,0.049999982,0.849999994,16
```

## Monitoring

- **Dataflow**: Monitor job status in Cloud Console
- **BigQuery**: Check data ingestion and query performance
- **Pub/Sub**: Monitor message throughput and backlog
- **Dataproc**: Track job execution and cluster utilization

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ --cov=src/

# Run specific test
pytest tests/test_pipeline.py::TestSentimentPipeline::test_sentiment_analysis
```

## 🛡️ Security

- **IAM Roles**: Fine-grained access control
- **Service Accounts**: Dedicated accounts for each component
- **Encryption**: Data encrypted at rest and in transit
- **VPC**: Network isolation and security

## 💰 Cost Optimization

- **Serverless**: Pay only for what you use
- **Auto-scaling**: Resources scale based on demand
- **Managed Services**: No infrastructure management overhead

## Troubleshooting

### Common Issues

1. **Permission Errors**: Verify IAM roles are correctly assigned
2. **Resource Limits**: Check quotas and increase if needed
3. **Network Issues**: Ensure VPC and firewall rules are configured
4. **API Limits**: Monitor API usage and request quota increases

### Logs

- **Dataflow**: `gcloud logging read "resource.type=dataflow_job"`
- **Dataproc**: `gcloud logging read "resource.type=dataproc_cluster"`
- **Pub/Sub**: `gcloud logging read "resource.type=pubsub_topic"`
```

## Complete `.gitignore`

```gitignore:.gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Environment Variables
.env
.env.local
.env.production

# Google Cloud
*.json
service-account-key.json
credentials.json

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
temp/
tmp/

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Terraform
*.tfstate
*.tfstate.*
.terraform/
```

## Complete `LICENSE`

```license:LICENSE
MIT License

Copyright (c) 2025 Real-Time Sentiment Analytics Pipeline

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

# 🚀 Steps to Push Code to GitHub

## 1. Create GitHub Repository

### Via GitHub Web Interface:
1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Repository name: `real-time-sentiment-analytics`
4. Description: `Production-ready real-time sentiment analysis pipeline on Google Cloud Platform`
5. Set to **Public** or **Private**
6. **Don't** initialize with README (we have our own)
7. Click "Create Repository"

## 2. Initialize Local Git Repository

```bash
# Navigate to your project directory
cd real-time-sentiment-analytics

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Real-time sentiment analytics pipeline

- Complete streaming pipeline with Pub/Sub, Dataflow, BigQuery
- Batch analytics with Dataproc and Spark
- Production-ready configuration and deployment scripts
- Comprehensive documentation and testing framework
- IAM roles and security configuration
- Automated setup and cleanup scripts"
```

## 3. Connect to GitHub and Push

```bash
# Add GitHub remote (replace with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/real-time-sentiment-analytics.git

# Push to GitHub
git push -u origin main
```

## 4. Create Additional Branches (Optional)

```bash
# Create development branch
git checkout -b development
git push -u origin development

# Create feature branches
git checkout -b feature/enhanced-analytics
git push -u origin feature/enhanced-analytics

# Switch back to main
git checkout main
```

## 5. Add GitHub Repository Features

### Create Issues Templates
Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown:.github/ISSUE_TEMPLATE/bug_report.md
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- GCP Project ID: [e.g. my-project-123]
- Region: [e.g. us-central1]
- Python version: [e.g. 3.9]

**Additional context**
Add any other context about the problem here.
```

### Create Pull Request Template
Create `.github/pull_request_template.md`:

```markdown:.github/pull_request_template.md
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

## 6. Add GitHub Actions (CI/CD)

Create `.github/workflows/ci.yml`:

```yaml:.github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src/ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install linting tools
      run: |
        pip install flake8 black isort
    
    - name: Run linting
      run: |
        flake8 src/ tests/
        black --check src/ tests/
        isort --check-only src/ tests/
```

## 7. Final Steps

```bash
# Add GitHub-specific files
git add .github/
git commit -m "Add GitHub templates and CI/CD workflow"
git push origin main

# Create and push tags for releases
git tag -a v1.0.0 -m "Initial release: Production-ready sentiment analytics pipeline"
git push origin v1.0.0
```

## 8. Update README with Badges

Add these badges to the top of your README.md:

```markdown
[![CI/CD](https://github.com/YOUR_USERNAME/real-time-sentiment-analytics/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/real-time-sentiment-analytics/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
```

---

# 🛑 Services to Stop After Completion

## Immediate Cleanup (Cost-Saving)

### 1. Stop Dataflow Jobs
```bash
# List active jobs
gcloud dataflow jobs list --region=us-central1 --status=active

# Cancel specific job
gcloud dataflow jobs cancel JOB_ID --region=us-central1
```

### 2. Delete Dataproc Cluster
```bash
gcloud dataproc clusters delete analytics-cluster --region=us-central1
```

### 3. Stop Compute Engine Instances (if any)
```bash
gcloud compute instances list
gcloud compute instances stop INSTANCE_NAME --zone=us-central1-a
```

## Optional Cleanup (Data Preservation)

### Keep These (Low/No Cost):
- ✅ **Pub/Sub Topics** (no cost when idle)
- ✅ **BigQuery Dataset** (storage cost only)
- ✅ **Cloud Storage Bucket** (storage cost only)
- ✅ **IAM Roles** (no cost)

### Delete These (If No Longer Needed):
```bash
# Delete BigQuery dataset
bq rm -r -f analytics_results

# Delete Pub/Sub topic
gcloud pubsub topics delete message-topic

# Delete Cloud Storage bucket
gsutil -m rm -r gs://your-project-pipeline
```

## Cost Monitoring

```bash
# Check current costs
gcloud billing budgets list

# Set up budget alerts
gcloud billing budgets create --billing-account=BILLING_ACCOUNT_ID --display-name="Pipeline Budget" --budget-amount=50USD
