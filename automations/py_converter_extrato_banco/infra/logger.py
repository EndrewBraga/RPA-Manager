import logging
from pathlib import Path


def configurar_logger(pasta_base):

    # ignore the pasta_base for log placement; instead keep logs in a central `logs/<automation>` folder
    # derive workspace root by walking up from this file
    repo_root = Path(__file__).resolve().parents[3]
    automation_name = Path(__file__).resolve().parents[1].name

    log_dir = repo_root / "logs" / automation_name
    log_dir.mkdir(parents=True, exist_ok=True)

    arquivo_log = log_dir / "processamento.log"

    logger = logging.getLogger("extrato_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(arquivo_log, encoding="utf-8")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger