---
sidebar_position: 1
title: Getting Started
---

# Getting Started with Kubernetes Practice Assistant

Welcome to the Kubernetes Practice Assistant (KPA) - an interactive learning environment designed to help you master Kubernetes through hands-on practice and AI-powered guidance.

## What is KPA?

KPA is a web-based application that provides:

- 🎯 **Interactive scenarios** for Kubernetes practice
- 🤖 **AI-powered assistance** to guide you through challenges
- 💻 **Web-based terminal** with kubectl access
- 📚 **Structured learning paths** for CKA/CKAD preparation
- 🔄 **Real-time feedback** on your commands and progress

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher
- pip (Python package manager)
- A Kubernetes cluster (optional - can run locally with kind/minikube)
- An OpenAI API key (for AI assistance features)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/robert-cronin/kpa.git
cd kpa
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Run the Application

You can start KPA using either method:

```bash
# Method 1: Direct Python execution
python -m app.main

# Method 2: Using the task runner
task start
```

The application will start on `http://localhost:8080`

## Next Steps

- [Installation Guide](./installation) - Detailed setup instructions
- [Usage Guide](./usage) - Learn how to use KPA effectively

## Getting Help

If you encounter any issues:

1. Check the documentation
2. Open an issue on [GitHub](https://github.com/robert-cronin/kpa/issues)

Happy learning! 🚀
