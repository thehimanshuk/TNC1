import logging
import os

def setup_logging():
    log_directory = "./logs"
    log_filename = "logs.log"
    full_log_path = os.path.join(log_directory, log_filename)

    # Ensure the log directory exists
    os.makedirs(log_directory, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s',
        filename=full_log_path,
        filemode='a'  # Append mode
    )