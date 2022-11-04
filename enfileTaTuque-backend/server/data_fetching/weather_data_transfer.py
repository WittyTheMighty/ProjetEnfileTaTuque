import requests
import json
from dotenv import load_dotenv
from azure.storage.blob import ContainerClient
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pytz

CURR_DIR = Path(__file__).parent.resolve()
TMP_DIR = os.path.join(CURR_DIR, 'tmp')
os.makedirs(TMP_DIR, exist_ok=True)

# GET API KEY
load_dotenv()
api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


LON = "-73.74"
LAT = "45.47"
EXCLUDE = 'daily,minutely,alerts'

WEATHER_URL =  f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude={EXCLUDE}&appid={api_key}&units=metric"

keep_cols = ['dt', 'temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg']

local_raw_file_name = f"weather_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
hist_weather_file_name = "hist_weather.csv"
forecast_weather_file_name = "forecast.csv"

container_name = "hackqc"
raw_folder = "enfiletatuque/weather_extracts/"
tabular_folder = "enfiletatuque/"


def convert_windspeed(windspeed):
    return windspeed * 3.6


def convert_pressure(pressure):
    return pressure * 0.1


def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return t.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=t.minute//30)


def convert_date(timestamp):
    return hour_rounder(datetime.fromtimestamp(timestamp, tz=pytz.timezone('US/Eastern'))).strftime('%Y-%m-%d %H:%M')


def format_df(df):
    df['date'] = df['dt'].apply(convert_date)
    df['pressure'] = df['pressure'].apply(convert_pressure)
    df['wind_speed'] = df['wind_speed'].apply(convert_windspeed)
    df = df.drop(columns=['dt'])
    return df


def get_current_df(json):
    df = pd.json_normalize(json['current'])[keep_cols]
    df = format_df(df)
    return df


def get_forecast_df(json):
    df = pd.json_normalize(json['hourly'])[keep_cols]
    df = format_df(df)
    return df


# GET DATA FROM OpenWeatherMap
resp = requests.get(WEATHER_URL)
json_obj = json.loads(resp.text)
with open(os.path.join(TMP_DIR, local_raw_file_name), 'w') as f:
    json.dump(json_obj, f)

try:
    container_client = ContainerClient.from_connection_string(connect_str, container_name=container_name)

    # UPLOAD RAW EXTRACTS
    blob_name = raw_folder + local_raw_file_name
    blob_client = container_client.get_blob_client(blob_name)
    print(f"Uploading file {local_raw_file_name} to {container_name}.")
    with open(os.path.join(TMP_DIR, local_raw_file_name), 'rb') as data:
        blob_client.upload_blob(data)

    # FORMAT WEATHER DFS
    current_df = get_current_df(json_obj)
    forecast_df = get_forecast_df(json_obj)


    # UPDATE/UPLOAD HIST WEATHER DATASET
    csv_blob_name = tabular_folder + hist_weather_file_name
    csv_blob_client = container_client.get_blob_client(csv_blob_name)
    if csv_blob_client.exists():
        print(f'Reading historical dataset from {container_name}')
        dest_file = os.path.join(TMP_DIR, hist_weather_file_name)
        with open(dest_file, "wb") as my_blob:
            download_stream = csv_blob_client.download_blob()
            my_blob.write(download_stream.readall())
        df = pd.read_csv(dest_file)
        df = pd.concat((df, current_df))
        df.drop_duplicates(subset='date', keep='last', inplace=True)
    else:
        df = current_df

    print(f'Uploading historical dataset to {container_name}')
    csv_blob_client.upload_blob(data=df.to_csv(index=False), overwrite=True)


    # UPDATE FORECAST WEATHER DATASET
    csv_blob_name = tabular_folder + forecast_weather_file_name
    csv_blob_client = container_client.get_blob_client(csv_blob_name)

    print(f'Uploading forecast dataset to {container_name}')
    csv_blob_client.upload_blob(data=forecast_df.to_csv(index=False), overwrite=True)

except Exception as ex:
   print('Exception:')
   print(ex)

