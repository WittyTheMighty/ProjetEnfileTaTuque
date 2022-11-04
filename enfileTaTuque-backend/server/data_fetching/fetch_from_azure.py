from dotenv import load_dotenv
from azure.storage.blob import ContainerClient
import os
CONTAINER_NAME = "hackqc"
TABULAR_FOLDER = "enfiletatuque/"
HYDRO_DATA_FILENAME = "data_tabular.csv"
HIST_WEATHER_FILENAME = "hist_weather.csv"
FORECAST_WEATHER_FILENAME = "forecast.csv"

def fetch_data(file_handle, blob_name):
    # GET AZURE STORAGE CONNECTION STRING

    load_dotenv()
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    try:
        print('Connecting to container')
        container_client = ContainerClient.from_connection_string(connect_str, container_name=CONTAINER_NAME)

        blob_client = container_client.get_blob_client(blob_name)
        if blob_client.exists():
            print(f'Reading {blob_name} dataset from {CONTAINER_NAME}')
            download_stream = blob_client.download_blob()
            file_handle.write(download_stream.readall())
            print(f'File written')
        else:
            print(f'{blob_name} not found in {CONTAINER_NAME}')
            
    except Exception as ex:
        print('Exception:')
        print(ex)