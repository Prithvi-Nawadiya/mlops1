# MLOps Batch Job Task

This repository contains a minimal MLOps-style batch job that computes signals from financial data (OHLCV).

## Features
- **Reproducibility**: Deterministic results using seeds and configuration files.
- **Observability**: Detailed logging and machine-readable metrics.
- **Deployment**: Fully Dockerized for consistent execution across environments.

## Project Structure
- `run.py`: Main execution script.
- `config.yaml`: Configuration parameters (seed, window, version).
- `data.csv`: Input OHLCV data.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Containerization setup.
- `metrics.json`: Output metrics (machine-readable).
- `run.log`: Execution logs.

## Local Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
   ```

## Docker Instructions

1. Build the image:
   ```bash
   docker build -t mlops-task .
   ```

2. Run the container:
   ```bash
   docker run --rm mlops-task
   ```

## Example metrics.json
```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```
