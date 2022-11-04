from server.data_fetching.fetch_from_azure import fetch_data, TABULAR_FOLDER,HYDRO_DATA_FILENAME,FORECAST_WEATHER_FILENAME,HIST_WEATHER_FILENAME
import os

import pandas as pd
import uuid

def create_data_fetcher_training():
    def get_data(no_arg):
        unique_filename = str(uuid.uuid4())
        with open(unique_filename,'wb') as tmp:
            fetch_data(tmp, TABULAR_FOLDER+HYDRO_DATA_FILENAME)
        df_conso = pd.read_csv(unique_filename)
        os.remove(unique_filename)

        unique_filename = str(uuid.uuid4())
        with open(unique_filename, 'wb') as tmp:
            fetch_data(tmp, TABULAR_FOLDER + HIST_WEATHER_FILENAME)
        df_weather = pd.read_csv(unique_filename)
        os.remove(unique_filename)

        return df_conso , df_weather
    return get_data


def create_data_fetcher_predict():
    def get_data(no_arg):
        unique_filename = str(uuid.uuid4())
        with open(unique_filename, 'wb') as tmp:
            fetch_data(tmp, TABULAR_FOLDER + HYDRO_DATA_FILENAME)
        df_conso = pd.read_csv(unique_filename)
        os.remove(unique_filename)

        unique_filename = str(uuid.uuid4())
        with open(unique_filename, 'wb') as tmp:
            fetch_data(tmp, TABULAR_FOLDER + FORECAST_WEATHER_FILENAME)
        df_weather = pd.read_csv(unique_filename)
        os.remove(unique_filename)

        return df_conso, df_weather

    return get_data
