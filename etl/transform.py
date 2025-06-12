import pandas as pd
from pathlib import Path
import logging
from sklearn.preprocessing import StandardScaler
from etl.utils import load_config, setup_logging

COLUMN_NAMES = [
    'id', 'diagnosis',
] + [f'{feat}_{stat}' for feat in [
    'radius','texture','perimeter','area','smoothness','compactness',
    'concavity','concave_points','symmetry','fractal_dimension'
] for stat in ['mean','se','worst']]

def main(config_path: str = 'config.yaml'):
    setup_logging()
    logger = logging.getLogger('transform')
    cfg = load_config(config_path)
    raw_path = Path(cfg['raw_data_path'])
    proc_path = Path(cfg['processed_data_path'])
    proc_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Чтение сырого файла {raw_path}")
    df = pd.read_csv(raw_path, header=None, names=COLUMN_NAMES)

    logger.info("Удаляем столбец id и кодируем диагноз")
    df = df.drop(columns=['id'])
    df['diagnosis'] = df['diagnosis'].map({'M':1, 'B':0})

    X = df.drop(columns=['diagnosis'])
    y = df['diagnosis']

    logger.info("Нормализация признаков")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    df_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    df_scaled['diagnosis'] = y.values

    df_scaled.to_csv(proc_path, index=False)
    logger.info(f"Сохранены предобработанные данные в {proc_path}")

if __name__ == '__main__':
    main()