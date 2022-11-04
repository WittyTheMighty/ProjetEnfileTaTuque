import requests
import json
from dotenv import load_dotenv
from azure.storage.blob import ContainerClient
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

CURR_DIR = Path(__file__).parent.resolve()
TMP_DIR = os.path.join(CURR_DIR, 'tmp')
os.makedirs(TMP_DIR, exist_ok=True)

DATA_URL = 'https://donnees.solutions.hydroquebec.com/donnees-ouvertes/data/json/ges-electricite.json'

local_raw_file_name = f"data_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
tabular_file_name = "data_tabular.csv"

container_name = "hackqc"
raw_folder = "enfiletatuque/raw_extracts/"
tabular_folder = "enfiletatuque/"


def consolidate_data(json_obj):
    data = pd.json_normalize(json_obj['details'])
    date_cutoff = datetime.now() - pd.Timedelta(6, unit='h') # to_validate
    dates = pd.to_datetime(data.date)
    return data[dates < date_cutoff]


def merge_dfs(df, new_chunk):
    # Make sure all columns match
    for col in set(df.columns).union(set(new_chunk.columns)):
        if col not in new_chunk:
            new_chunk[col] = pd.NA
        if col not in df:
            df[col] = pd.NA

    merged_df = pd.concat((df, new_chunk))
    merged_df.date = pd.to_datetime(merged_df.date)
    merged_df = merged_df.set_index('date').resample('H').max()
    merged_df = merged_df.dropna(how='all').reset_index()
    merged_df.sort_values(by='date', inplace=True)
    return merged_df


# GET AZURE STORAGE CONNECTION STRING
load_dotenv()
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# GET DATA FROM DonneesQC
resp = requests.get(DATA_URL)
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

    # UPDATE/UPLOAD TABULAR DATASET
    csv_blob_name = tabular_folder + tabular_file_name
    csv_blob_client = container_client.get_blob_client(csv_blob_name)
    if csv_blob_client.exists():
        print(f'Reading tabular dataset from {container_name}')
        dest_file = os.path.join(TMP_DIR, tabular_file_name)
        with open(dest_file, "wb") as my_blob:
            download_stream = csv_blob_client.download_blob()
            my_blob.write(download_stream.readall())
        df = pd.read_csv(dest_file)
        new_chunk = consolidate_data(json_obj)
        df = merge_dfs(df, new_chunk)
    else:
        df = consolidate_data(json_obj)

    print(f'Uploading tabular dataset to {container_name}')
    csv_blob_client.upload_blob(data=df.to_csv(index=False), overwrite=True)

except Exception as ex:
   print('Exception:')
   print(ex)

