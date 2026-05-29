# LLM Evaluation Platform

Automated platform to evaluate and compare LLM models using MLflow, Ollama, Docker, and GitHub Actions.

![CI](https://github.com/gajapriyanagulraj/llm-eval-mlflow/actions/workflows/eval.yml/badge.svg)

## What it does

- Runs prompts against local LLMs via Ollama
- Measures latency and scores each response
- Tracks all runs in MLflow
- Compares multiple models side by side
- Automates everything via GitHub Actions CI pipeline

## MLflow Dashboard

### Run Overview
![MLflow Overview](docs/images/mlflow-overview.jpeg)

### Model Metrics
![MLflow Metrics](docs/images/mlflow-metrics.jpeg)

### Artifacts (Full Response JSON)
![MLflow Artifacts](docs/images/mlflow-artifcats.jpeg)

## Results — llama3

| Metric | Value |
|--------|-------|
| Prompts Tested | 5 |
| Avg Score | 9.0 / 10 |
| Avg Latency | 38.54s |
| Failures | 0 |

## Project Structure

```
llm-eval-mlflow/
├── prompts/prompts.json         # Test prompts
├── evaluator/evaluate.py        # Core evaluation logic
├── tracker/tracking.py          # MLflow leaderboard
├── compare_models.py            # Run all models
├── docs/images/                 # Screenshots
├── .github/workflows/eval.yml   # CI pipeline
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Quick Start

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Start Ollama and pull a model
```bash
ollama serve
ollama pull llama3
```

### 3. Start MLflow
```bash
python3 -m mlflow server --host 0.0.0.0 --port 5001 --backend-store-uri ./mlruns
```

### 4. Run evaluation
```bash
MLFLOW_TRACKING_URI=http://localhost:5001 python3 compare_models.py
```

### 5. View results
Open browser: http://localhost:5001

## Docker

```bash
docker compose up
```

## Tech Stack

- **Ollama** — local LLM runner
- **MLflow** — experiment tracking
- **Docker** — containerization
- **GitHub Actions** — CI automation
