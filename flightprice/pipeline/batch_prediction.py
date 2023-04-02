from flightprice.exception import FlightPriceException
from flightprice.logger import logging
import numpy as np
import pandas as pd
import os , sys
from flightprice.predictor import ModelResolver
from flightprice.utils import load_object
from datetime import datetime


PREDICTION_DIR = 'prediction'
def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        model_resolver = ModelResolver(model_registry="savel_models")

        df = pd.read_csv(input_file_path)
        df.replace({'na':np.NaN},inplace=True)

        #data validation
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())


        input_features_names = list(transformer.feature_names_in_)
        for i in input_features_names:
            if df[i].dtypes=='object':
                df[i] = target_encoder.fit_transform(df[i])

        input_arr =transformer.transform(df[input_features_names])

        model = load_object(file_path=model_resolver.get_latest_dir_path())
        prediction = model.predict(input_arr)
        df['prediction'] = prediction
        

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%Y%m%d__%H%M%S')}.csv")

        prediction_file_name = os.path.join(PREDICTION_DIR,prediction_file_name)

        df.to_csv(prediction_file_name,index=False,header=True)

        return prediction_file_name

    except Exception as e:
        raise FlightPriceException(e, sys)
    