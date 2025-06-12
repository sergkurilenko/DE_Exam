import yaml
import logging
from pathlib import Path

def load_config(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
        handlers=[logging.FileHandler("logs/pipeline.log"), logging.StreamHandler()]
    )