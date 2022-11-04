from sklearn.linear_model import LinearRegression
import pandas as pd
from datetime import datetime

def create_pipeline(list_functions):
    def pipeline(input):
        res = input
        for function in list_functions:
            res = function(res)
        return res

    return pipeline


_list_weather_col = ['temp', 'humidity', 'wind_deg',
                     'wind_speed', 'pressure']


def preprocess_training(input):
    df_cons, df_weather = input
    df_cons['date'] = pd.to_datetime(df_cons['date'])
    df_cons = df_cons.set_index('date')
    df_weather['date'] = pd.to_datetime(df_weather['date'])
    df_weather = df_weather.set_index('date')
    df_all = pd.merge(df_cons[['Quebec_Consommation_Sources.thermique']], df_weather, left_index=True, right_index=True)
    return df_all
def preprocess_predict(input):
    df_cons, df_weather = input
    df_cons['date'] = pd.to_datetime(df_cons['date'])
    df_cons = df_cons.set_index('date')
    df_weather['date'] = pd.to_datetime(df_weather['date'])
    df_weather = df_weather.set_index('date')

    return df_cons, df_weather


def create_features_training(df_all):
    df_res = df_all.copy()

    for i in range(6,30):
        df_res[f'lags_{i}'] = df_res['Quebec_Consommation_Sources.thermique'].shift(i)
    for c in _list_weather_col:
        df_res[f'{c}_mean'] = df_res[c].shift(-24).rolling('24H').mean()

    return df_res
def create_features_prediction(input):
    df_cons, df_weather = input
    for i in range(24):
        df_cons[f'lags_{i + 6}'] = df_cons['Quebec_Consommation_Sources.thermique'].shift(i)
    for c in _list_weather_col:
        df_weather[f'{c}_mean'] = df_weather[c].head(24).mean()

    df_cons = df_cons.tail(1)[[f'lags_{i}' for i in range(6, 30)]]
    df_weather = df_weather.tail(1)[list(map(lambda x: f'{x}_mean', _list_weather_col))]
    df_weather.index = df_cons.index
    df_res = pd.concat([df_cons, df_weather], axis=1)

    return df_res

def format_output_predictions(preds):
    cur_dt = datetime.now().replace(minute=0, second=0, microsecond=0)
    dt_range = pd.date_range(cur_dt,periods = 24,freq='H')
    dict_res = {}
    for i in range(len(preds[0])):
        dict_res[dt_range[i]] = preds[0][i]
    return dict_res

def add_output(df):
    df_res = df.copy()
    for i in range(24):
        df_res[f'out_{i}'] = df_res['Quebec_Consommation_Sources.thermique'].shift(-i)
    return df_res


def clean_cols(df):
    list_col = [f'out_{i}' for i in range(24)] \
               + [f'lags_{i}' for i in range(6, 30)] \
               + list(map(lambda x: f'{x}_mean', _list_weather_col))
    return df[list_col]


def dropna(df):
    return df.dropna(axis=0)


def splitX_Y(df):
    x_cols = [f'lags_{i}' for i in range(6, 30)] \
             + list(map(lambda x: f'{x}_mean', _list_weather_col))
    y_cols = [f'out_{i}' for i in range(24)]
    return df[x_cols], df[y_cols]



def model_trainer(train):
    (trainX, trainY) = train
    model = LinearRegression()
    model.fit(trainX, trainY)
    return model



def create_trainer(create_data_fetcher_training, create_data_fetcher_predict):
    pipeline_training = create_pipeline([
        create_data_fetcher_training(),
        preprocess_training,
        create_features_training,
        add_output,
        clean_cols,
        dropna,
        splitX_Y,
        model_trainer
    ])

    def create_predictor():
        model = pipeline_training(None)
        pipeline_prediction = create_pipeline([
            create_data_fetcher_predict(),
            preprocess_predict,
            create_features_prediction,
            model.predict,
            format_output_predictions

        ])

        def predictor():
            res = pipeline_prediction(None)
            return res
        return predictor
    return create_predictor


