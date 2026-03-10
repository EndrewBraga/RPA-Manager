import os
from datetime import datetime


def create_logger(automation_name):

    log_dir = f"logs/{automation_name}"

    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = f"{log_dir}/execution_{timestamp}.log"

    return log_file