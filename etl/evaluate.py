import pickle
import json
from pathlib import Path
import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from etl.utils import load_config, setup_logging
import pandas as pd


def main(config_path: str = 'config.yaml'):
    setup_logging()
    logger = logging.getLogger('evaluate')
    cfg = load_config(config_path)

    proc_path = Path(cfg['processed_data_path'])
    model_path = Path(cfg['model_path'])
    metrics_path = Path(cfg['metrics_path'])
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Загрузка данных и модели для оценки")
    df = pd.read_csv(proc_path)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    X = df.drop(columns=['diagnosis'])
    y_true = df['diagnosis']
    y_pred = model.predict(X)

    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred)
    }

    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    logger.info(f"Метрики сохранены в {metrics_path}")

if __name__ == '__main__':
    main()