# Contents of /InfraAuditAI/InfraAuditAI/src/scripts/monitor_pipeline.py

import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_pipeline():
    """
    Monitors the CI/CD pipeline for any issues or failures.
    Logs the status of the pipeline at regular intervals.
    """
    logging.info("Starting to monitor the CI/CD pipeline...")
    
    while True:
        # Here you would implement the logic to check the status of the pipeline
        # For demonstration, we will log a message every 10 seconds
        logging.info("Checking pipeline status...")
        
        # Simulate checking the pipeline status
        time.sleep(10)  # Sleep for 10 seconds before the next check

if __name__ == "__main__":
    monitor_pipeline()