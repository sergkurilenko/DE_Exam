import os
import logging
import shutil
import boto3
from pathlib import Path
from etl.utils import load_config, setup_logging

def main(config_path: str = 'config.yaml'):
    setup_logging()
    logger = logging.getLogger('upload')
    cfg = load_config(config_path)

    # Локальное сохранение моделей и метрик
    local_results_dir = cfg["res_path"]
    for key in ['model_path', 'metrics_path']:
        src = Path(cfg[key])
        dst = os.path.join(local_results_dir, src.name)
        logger.info(f"Копирование {src} → {dst}")
        shutil.copy(src, dst)

    # Если в конфиге включена загрузка в S3
    if cfg.get('push_to_s3', 0) == 1:
        bucket = cfg['s3']['bucket']
        prefix = cfg['s3']['prefix']
        region = cfg['aws']['region']
        s3 = boto3.client('s3', region_name=region)
        for file in local_results_dir.iterdir():
            s3_key = f"{prefix}/{file.name}"
            logger.info(f"Выгрузка {file} в s3://{bucket}/{s3_key}")
            s3.upload_file(str(file), bucket, s3_key)
        logger.info("Загрузка в S3 завершена")

if __name__ == '__main__':
    main()