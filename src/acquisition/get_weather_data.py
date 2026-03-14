# import openmeteo_requests

# import pandas as pd
# import requests_cache
# from retry_requests import retry

# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# openmeteo = openmeteo_requests.Client(session = retry_session)

# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
# 	"latitude": [31.6342, 34.261, 30.4202, 34.0331],
# 	"longitude": [-7.9999, -6.5802, -9.5982, -5.0003],
# 	"daily": ["et0_fao_evapotranspiration", "wind_speed_10m_max", "shortwave_radiation_sum"],
# 	"timezone": "auto",
# }
# responses = openmeteo.weather_api(url, params=params)

# # Process 4 locations
# for response in responses:
# 	print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
# 	print(f"Elevation: {response.Elevation()} m asl")
# 	print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
# 	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
	
# 	# Process daily data. The order of variables needs to be the same as requested.
# 	daily = response.Daily()
# 	daily_et0_fao_evapotranspiration = daily.Variables(0).ValuesAsNumpy()
# 	daily_wind_speed_10m_max = daily.Variables(1).ValuesAsNumpy()
# 	daily_shortwave_radiation_sum = daily.Variables(2).ValuesAsNumpy()
	
# 	daily_data = {"date": pd.date_range(
# 		start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
# 		end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
# 		freq = pd.Timedelta(seconds = daily.Interval()),
# 		inclusive = "left"
# 	)}
	
# 	daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration
# 	daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
# 	daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
	
# 	daily_dataframe = pd.DataFrame(data = daily_data)
# 	print("\nDaily data\n", daily_dataframe)
	
import openmeteo_requests
import pandas as pd
import requests_cache
import os
from retry_requests import retry

# 1. Configuration et Chemins
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_dir = os.path.join(base_dir, "data", "raw")
os.makedirs(output_dir, exist_ok=True)

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# 2. Paramètres (Marrakech, Kénitra, Agadir, Fès)
#url = "https://api.open-meteo.com/v1/forecast"
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": [31.6342, 34.261, 30.4202, 34.0331],
    "longitude": [-7.9999, -6.5802, -9.5982, -5.0003],
    "start_date": "2024-01-01", # On remonte au début du dataset Kaggle
    "end_date": "2024-10-31",   # Jusqu'à la fin du dataset Kaggle
    "daily": ["et0_fao_evapotranspiration", "wind_speed_10m_max", "shortwave_radiation_sum"],
    "timezone": "auto",
}

# 3. Récupération et Transformation
responses = openmeteo.weather_api(url, params=params)
all_locations_data = []

# Noms des régions pour le mapping
region_names = ["Haouz (Marrakech)", "Gharb (Kenitra)", "Souss-Massa (Agadir)", "Saiss (Fes)"]

for i, response in enumerate(responses):
    daily = response.Daily()
    
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "region": region_names[i],
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "et0": daily.Variables(0).ValuesAsNumpy(),
        "wind_speed_max": daily.Variables(1).ValuesAsNumpy(),
        "radiation_sum": daily.Variables(2).ValuesAsNumpy()
    }
    all_locations_data.append(pd.DataFrame(data=daily_data))

# 4. Sauvegarde
df_weather = pd.concat(all_locations_data, ignore_index=True)
df_weather.to_csv(os.path.join(output_dir, "weather_maroc_raw.csv"), index=False)
print(f"Données météo sauvegardées dans : {output_dir}/weather_maroc_raw.csv")

