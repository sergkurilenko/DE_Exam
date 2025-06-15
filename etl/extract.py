import requests
from pathlib import Path
import logging
from etl.utils import load_config, setup_logging

def main(config_path: str = 'config.yaml'):
    setup_logging()
    logger = logging.getLogger('extract')
    cfg = load_config(config_path)

    url = cfg['source_url']
    raw_path = Path(cfg['raw_data_path'])
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Загрузка данных из {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    raw_path.write_bytes(resp.content)
    logger.info(f"Сохранено raw в {raw_path}")

if __name__ == '__main__':
    main()