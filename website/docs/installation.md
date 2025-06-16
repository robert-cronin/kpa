---
sidebar_position: 2
title: Installation Guide
---

# Installation Guide

This guide provides detailed instructions for installing and setting up the Kubernetes Practice Assistant (KPA) on your system.

## System Requirements

### Minimum Requirements

- **OS**: Linux, macOS, or Windows (with WSL2)
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum
- **Storage**: 1GB free space

### Recommended Requirements

- **Memory**: 8GB RAM or more
- **CPU**: 2+ cores
- **Kubernetes**: Local cluster (kind, minikube, or k3s)

## Installation Methods

### Method 1: Local Development Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/robert-cronin/kpa.git
cd kpa
```

#### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional
PORT=8080
DATABASE_PATH=./kpa.db
LOG_LEVEL=INFO
```

#### Step 5: Initialize the Database

The database will be automatically created when you first run the application. It contains pre-configured scenarios for Kubernetes practice.

#### Step 6: Run the Application

```bash
# Using Python directly
python -m app.main

# Or using the task runner
task start
```

Access the application at `http://localhost:8080`

### Method 2: Docker Installation

#### Step 1: Build the Docker Image

```bash
docker build -t kpa:latest .
```

#### Step 2: Run the Container

```bash
docker run -d \
  -p 8080:8080 \
  -e OPENAI_API_KEY=your-openai-api-key \
  --name kpa \
  kpa:latest
```

### Method 3: Kubernetes Deployment

#### Step 1: Create ConfigMap for Configuration

```bash
kubectl create configmap kpa-config \
  --from-literal=OPENAI_API_KEY=your-openai-api-key
```

#### Step 2: Deploy using Helm

```bash
# Add the KPA Helm repository (if available)
helm repo add kpa https://robert-cronin.github.io/kpa-helm-charts
helm repo update

# Install KPA
helm install kpa kpa/kpa \
  --set config.openaiApiKey=your-openai-api-key \
  --set ingress.enabled=true \
  --set ingress.host=kpa.your-domain.com
```

Or deploy using the included Helm chart:

```bash
cd chart
helm install kpa . \
  --set config.openaiApiKey=your-openai-api-key
```

## Setting Up a Local Kubernetes Cluster

KPA works best with a local Kubernetes cluster. Here are quick setup guides for popular options:

### Option 1: kind (Kubernetes in Docker)

```bash
# Install kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create cluster
kind create cluster --name kpa-cluster
```

### Option 2: minikube

```bash
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start
```

### Option 3: k3s (Lightweight Kubernetes)

```bash
# Install k3s
curl -sfL https://get.k3s.io | sh -

# Check status
sudo k3s kubectl get nodes
```

## Verifying Installation

After installation, verify that KPA is working correctly:

1. **Check Application Health**:

   ```bash
   curl http://localhost:8080/health
   ```

2. **Access the Web Interface**:
   Open your browser and navigate to `http://localhost:8080`

3. **Test kubectl Integration**:
   Try running a scenario that uses kubectl commands

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using port 8080
lsof -i :8080

# Use a different port
PORT=8081 python -m app.main
```

#### Python Version Issues

```bash
# Check Python version
python --version

# Use pyenv to manage Python versions
pyenv install 3.11.0
pyenv local 3.11.0
```

#### Database Connection Errors

```bash
# Remove corrupted database
rm kpa.db

# Restart the application (database will be recreated)
python -m app.main
```

## Next Steps

- [Usage Guide](./usage) - Learn how to use KPA effectively
