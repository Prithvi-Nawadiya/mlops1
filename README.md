# MLOps Batch Job: Financial Signal Pipeline

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 1. Project Overview
The **MLOps Batch Job** is a robust, production-ready Python pipeline designed for financial data processing. It demonstrates core MLOps principles including **reproducibility**, **observability**, and **containerization**. The pipeline ingests OHLCV (Open, High, Low, Close, Volume) data, performs feature engineering through rolling statistics, and generates actionable trading signals based on configurable parameters.

## 2. Features
- **Deterministic Execution**: Uses a seeded random number generator and configuration-driven logic to ensure identical results across runs.
- **Robust Validation**: Comprehensive checks for configuration integrity and dataset quality (missing columns, empty files, etc.).
- **Observability**: Generates machine-readable `metrics.json` for monitoring and human-readable `run.log` for debugging.
- **Production-Ready Deployment**: Fully containerized using Docker for consistent performance in any environment.
- **Efficient Processing**: Leverages vectorized operations with Pandas and NumPy for high-performance data manipulation.

## 3. Project Structure
```text
.
├── Dockerfile          # Containerization configuration
├── README.md           # Project documentation
├── config.yaml         # Pipeline configuration (seed, window, version)
├── data.csv            # Input OHLCV dataset
├── requirements.txt    # Python dependencies
├── run.py              # Main execution script
├── metrics.json        # Output: Machine-readable run metrics
└── run.log             # Output: Detailed execution logs
```

## 4. Configuration Example (`config.yaml`)
The pipeline is entirely driven by a YAML configuration file:
```yaml
seed: 42          # For deterministic results
window: 5         # Rolling mean window size
version: "v1"     # Pipeline versioning
```

## 5. Signal Logic
The pipeline computes a binary signal based on the relationship between the current `close` price and its `rolling mean`:
- **Signal = 1**: If `close > rolling_mean`
- **Signal = 0**: If `close <= rolling_mean` (or if rolling mean is unavailable due to window constraints)

## 6. Local Setup Instructions
Follow these steps to set up the project on your local machine.

### 7. Virtual Environment Setup
It is recommended to use a virtual environment to manage dependencies:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 8. Dependency Installation
Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

### 9. Local Run Command
Execute the pipeline using the following CLI structure:
```bash
python run.py \
  --input data.csv \
  --config config.yaml \
  --output metrics.json \
  --log-file run.log
```

## 10. Docker Build and Run Commands
Deploy the pipeline as a containerized service:

**Build the image:**
```bash
docker build -t mlops-task .
```

**Run the container:**
```bash
docker run --rm mlops-task
```

## 11. Example `metrics.json` Output
```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.5009,
  "latency_ms": 15,
  "seed": 42,
  "status": "success"
}
```

## 12. Error Handling Section
The pipeline implements a "fail-safe" metrics generation policy. In the event of an execution error (e.g., missing file, invalid config), the script captures the exception and writes an error-state JSON:
```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Missing required column: close"
}
```

## 13. Logging Section
Logs are captured with timestamps and severity levels in `run.log`. Key events logged include:
- Job initialization and timestamp.
- Configuration validation status.
- Dataset loading statistics.
- Processing milestones (Rolling mean, Signal generation).
- Final metrics summary and exit status.

## 14. Technologies Used
- **Python 3.9+**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical computing and seeding.
- **PyYAML**: YAML configuration parsing.
- **Docker**: Container orchestration.

