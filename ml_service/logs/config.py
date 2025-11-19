import logging
import os
from datetime import datetime

def setup_logger(log_dir="ml_service/experiments/logs", log_filename=None, level=logging.INFO):
    """
    Sets up a centralized logger that writes to both console and file.
    All modules can import this logger using:
        from logger_config import setup_logger
        logger = setup_logger()

    Args:
        log_dir (str): Directory where logs are stored.
        log_filename (str): Name of the log file. Defaults to timestamped name.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """

    # Create log directory if not exists
    os.makedirs(log_dir, exist_ok=True)

    # Default log filename with timestamp
    if not log_filename:
        log_filename = f"logging_ml_service_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    log_path = os.path.join(log_dir, log_filename)

    # Configure logger
    logger = logging.getLogger("ResumeLogger")
    logger.setLevel(level)

    # Avoid duplicate handlers if already configured
    if logger.handlers:
        return logger

    # File handler (persistent logs)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(level)

    # Console handler (real-time logs)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Log format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logger initialized. Logs will be written to {log_path}")
    return logger
