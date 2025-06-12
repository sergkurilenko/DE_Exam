import boto3
from pathlib import Path
import logging
from etl.utils import load_config, setup_logging

def main(config_path: str = 'config.yaml'):
    setup_logging()
    logger = logging.getLogger('upload')
    cfg = load_config(config_path)

    bucket = cfg['s3']['bucket']
    prefix = cfg['s3']['prefix']
    region = cfg['aws']['region']

    s3 = boto3.client('s3', region_name=region)

    for key in ['model_path', 'metrics_path']:
        local_path = Path(cfg[key])
        s3_key = f"{prefix}/{local_path.name}"
        logger.info(f"Выгрузка {local_path} в s3://{bucket}/{s3_key}")
        s3.upload_file(str(local_path), bucket, s3_key)
    logger.info("Выгрузка завершена")

if __name__ == '__main__':
    main()