import argparse
import json
import logging
import time
import yaml
import pandas as pd
import numpy as np
import sys
import os

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def write_metrics(output_path, metrics):
    try:
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        # Requirement: Print final metrics JSON to stdout for Docker
        print(json.dumps(metrics, indent=2))
    except Exception as e:
        logging.error(f"Failed to write metrics to {output_path}: {e}")

def main():
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description="MLOps Batch Job")
    parser.add_argument("--input", required=True, help="Path to input data.csv")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--output", required=True, help="Path to metrics.json output")
    parser.add_argument("--log-file", required=True, help="Path to run.log")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_file)
    logging.info("Job started")
    
    version = "unknown"
    seed = None
    
    try:
        # 1. Load + validate config
        if not os.path.exists(args.config):
            raise FileNotFoundError(f"Config file not found: {args.config}")
            
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
        
        required_fields = ['seed', 'window', 'version']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        
        seed = config['seed']
        window = config['window']
        version = config['version']
        
        np.random.seed(seed)
        logging.info(f"Config loaded and validated: seed={seed}, window={window}, version={version}")
        
        # 2. Load + validate dataset
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"Input file not found: {args.input}")
            
        df = pd.read_csv(args.input)
        if df.empty:
            raise ValueError("Input CSV is empty")
            
        if 'close' not in df.columns:
            raise ValueError("Missing required column: close")
            
        rows_loaded = len(df)
        logging.info(f"Loaded {rows_loaded} rows from {args.input}")
        
        # 3. Rolling mean
        logging.info(f"Computing rolling mean with window {window}")
        df['rolling_mean'] = df['close'].rolling(window=window).mean()
        
        # 4. Signal generation
        # Important: handle NaNs from rolling mean.
        # We exclude rows where rolling_mean is NaN for signal_rate computation
        # but the logic says signal = 1 if close > rolling_mean else 0.
        # If rolling_mean is NaN, close > rolling_mean is False, so signal is 0.
        logging.info("Generating signals")
        df['signal'] = (df['close'] > df['rolling_mean']).astype(int)
        
        # We only count rows where rolling_mean is valid for signal_rate?
        # Actually, let's keep it simple: signal_rate = mean(signal) across processed rows.
        # The first window-1 rows will have NaN rolling_mean and thus signal 0.
        
        signal_rate = float(df['signal'].mean())
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        metrics = {
            "version": version,
            "rows_processed": rows_loaded,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }
        
        logging.info(f"Metrics summary: rows_processed={rows_loaded}, signal_rate={signal_rate:.4f}, latency_ms={latency_ms}")
        logging.info("Job completed successfully")
        
        write_metrics(args.output, metrics)
        sys.exit(0)

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error occurred: {error_msg}")
        
        latency_ms = int((time.time() - start_time) * 1000)
        metrics = {
            "version": version,
            "status": "error",
            "error_message": error_msg
        }
        # Note: if config couldn't be loaded, version might be unknown. 
        # But instructions say "Metrics file must be written in both success and error cases."
        write_metrics(args.output, metrics)
        sys.exit(1)

if __name__ == "__main__":
    main()
