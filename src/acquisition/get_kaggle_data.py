import kagglehub
import os
import shutil

# Download latest version
path = kagglehub.dataset_download("atharvasoundankar/smart-farming-sensor-data-for-yield-prediction")

print("Path to dataset files:", path)

# 2. Définition de notre dossier local
destination = "data/raw/kaggle_smart_farming/"
os.makedirs(destination, exist_ok=True)

# 3. Copie des fichiers vers notre architecture H2Olytics
for file in os.listdir(path):
    shutil.copy(os.path.join(path, file), destination)

print(f"Fichiers déplacés avec succès vers : {destination}")