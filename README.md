# H2Olytics

H2Olytics/
├── data/               # Stockage des fichiers bruts et finaux
│   ├── raw/            # Datasets Kaggle et Open-Meteo bruts
│   └── processed/      # Dataset final après merge
├── src/                # Code source du projet
│   ├── __init__.py
│   ├── acquisition/    # Scripts pour télécharger les données
│   │   ├── get_kaggle_data.py
│   │   └── get_weather_data.py
│   ├── processing/     # Scripts de nettoyage et merge
│   │   └── merge_datasets.py
│   ├── models/         # Scripts d'entraînement (Random Forest, etc.)
│   │   └── train_model.py
│   └── app/            # Interface Streamlit
│       └── dashboard.py
├── notebooks/          # Tests et exploration (fichiers .ipynb)
├── .python-version     # Version de Python gérée par uv
├── pyproject.toml      # Dépendances du projet (géré par uv)
└── README.md