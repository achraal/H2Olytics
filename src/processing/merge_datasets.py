import pandas as pd
import os

# 1. Chemins
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
kaggle_path = os.path.join(base_dir, "data", "raw", "kaggle_smart_farming", "Smart_Farming_Crop_Yield_2024.csv")
weather_path = os.path.join(base_dir, "data", "raw", "weather_maroc_raw.csv")

# 2. Chargement
df_kag = pd.read_csv(kaggle_path)
df_meteo = pd.read_csv(weather_path)

# 3. Harmonisation des DATES (YYYY-MM-DD)
df_kag['date_join'] = pd.to_datetime(df_kag['timestamp']).dt.strftime('%Y-%m-%d')
df_meteo['date_join'] = pd.to_datetime(df_meteo['date']).dt.strftime('%Y-%m-%d')

# 4. Mapping des régions pour la correspondance Maroc
region_map = {
    'North India': 'Gharb (Kenitra)',
    'South USA': 'Souss-Massa (Agadir)',
    'East Africa': 'Haouz (Marrakech)',
    'Central USA': 'Saiss (Fes)'
}
df_kag['region_maroc'] = df_kag['region'].map(region_map)

# 5. LE MERGE (Left Join)
# Ici, on utilise 'region' pour le fichier météo (le nom correct dans votre CSV)
df_final = pd.merge(
    df_kag, 
    df_meteo[['date_join', 'region', 'et0', 'wind_speed_max', 'radiation_sum']], 
    left_on=['date_join', 'region_maroc'], 
    right_on=['date_join', 'region'],
    how='left'
)

# 6. Nettoyage : On supprime la colonne de région en double
# (Celle qui vient de df_meteo)
if 'region_y' in df_final.columns:
    df_final = df_final.drop(columns=['region_y'])
elif 'region_right' in df_final.columns:
    df_final = df_final.drop(columns=['region_right'])

# 7. Sauvegarde
output_path = os.path.join(base_dir, "data", "processed", "dataset_final.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_final.to_csv(output_path, index=False)

print(f"Succès ! Le dataset final a été créé.")
print(f"Nombre de lignes conservées : {len(df_final)}")
print(f"Chemin : {output_path}")