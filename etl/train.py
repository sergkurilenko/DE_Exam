import pickle
from pathlib import Path
import logging
from sklearn.linear_model import LogisticRegression
from etl.utils import load_config, setup_logging
import pandas as pd


def main(config_path: str = 'config.yaml'):
    setup_logging()
    logger = logging.getLogger('train')
    cfg = load_config(config_path)

    proc_path = Path(cfg['processed_data_path'])
    model_path = Path(cfg['model_path'])
    model_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Загрузка данных для обучения из {proc_path}")
    df = pd.read_csv(proc_path)
    X = df.drop(columns=['diagnosis'])
    y = df['diagnosis']

    logger.info("Обучение LogisticRegression")
    model = LogisticRegression(
        random_state=cfg['model']['random_state'],
        C=cfg['model']['C'],
        max_iter=1000
    )
    model.fit(X, y)

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    logger.info(f"Модель сохранена в {model_path}")

if __name__ == '__main__':
    main()