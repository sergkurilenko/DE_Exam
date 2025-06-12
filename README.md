# Проект: Автоматизированный ETL-пайплайн для диагностики заболеваний

# Выполнил: Куриленко Сергей

## Структура репозитория

```
├── dags/
│   └── pipeline_dag.py           # Airflow DAG
├── etl/
│   ├── extract.py                # Загрузка и первичный анализ данных
│   ├── transform.py              # Очистка и предобработка
│   ├── train.py                  # Обучение модели
│   ├── evaluate.py               # Расчет метрик и сохранение результатов
│   └── utils.py                  # Общие вспомогательные функции
├── results/
│   ├── model.pkl                 # Сохраненная модель
│   └── metrics.json              # Итоговые метрики
├── logs/                         # Логи выполнения задач Airflow и скриптов
├── README.md                     # Описание проекта и инструкции
├── requirements.txt              # Зависимости проекта
└── config.yaml                   # Конфигурация (пути, параметры модели, подключение к хранилищу)
```

---

## README.md — Содержание и разделы

1. **Название проекта и содержание**
2. **Цель проекта и обоснование**
   - Диагностика рака молочной железы с помощью модели \
     LogisticRegression на датасете WDBC
3. **ML-задача**
   - Классификация: доброкачественная vs злокачественная опухоль
4. **Схема пайплайна**
   - Mermaid-диаграмма или блок-схема:
     ```mermaid
     graph LR
       A[Загрузка данных] --> B[Предобработка]
       B --> C[Обучение модели]
       C --> D[Оценка метрик]
       D --> E[Выгрузка результатов]
     ```
5. **Описание шагов пайплайна**
   - `extract.py`: скачивает CSV, проверяет целостность, сохраняет на диск
   - `transform.py`: переименовывает колонки, нормализует признаки
   - `train.py`: обучает LogisticRegression, сохраняет модель
   - `evaluate.py`: вычисляет Accuracy, Precision, Recall, F1, сохраняет JSON
   6. **Инструкции по запуску**
      - Локально: 
       ```
       python etl/extract.py --config config.yaml
       python etl/transform.py --config config.yaml
       python etl/train.py --config config.yaml
       python etl/evaluate.py --config config.yaml
       python etl/upload.py --config config.yaml
       ```
   - Через Airflow:
     ```bash
     airflow dags trigger pipeline_dag
     airflow tasks test pipeline_dag extract 2025-06-12
     ```
7. **DAG в Airflow**
   - Название: `pipeline_dag`
   - Операторы: PythonOperator для каждого скрипта
   - Зависимости: `extract >> transform >> train >> evaluate >> upload`
8. **Интеграция с хранилищем**
   - S3: передача через Boto3, конфиг в `config.yaml`
   - Локально: `results/` подкаталог, структура `results/{date}/`
9. **Анализ ошибок и устойчивость**
   - Retry в Airflow (3 попытки, delay=5 мин)
   - Timeout для каждого таска
   - Логирование через `logging` и callbacks
10. **Идеи для развития**
    - Использовать Cross-Validation и гиперпараметры
    - Добавить мониторинг с Grafana
    - Распараллелить предобработку
    - Перейти на модель XGBoost или RandomForest



