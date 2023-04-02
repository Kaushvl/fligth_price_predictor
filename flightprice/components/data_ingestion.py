from flightprice.entity import config_entity
import pandas as pd
import numpy as np
import os, sys
from flightprice.entity import artifact_entity
from flightprice.exception import FlightPriceException
from flightprice import utils
from flightprice.logger import logging
from sklearn.model_selection import train_test_split

class Dataingestion:
    def __init__(self, data_ingestion_config = config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise FlightPriceException(e, sys)
        
    def initiate_data_injestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Export collection data as dataframe")
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"store data for further store")
            df.replace(to_replace='na', value=np.NaN,inplace=True)
            logging.info(f"create feature store folder if not available")

            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("save df to feature store folder ")

            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info(f"spliting data into train and test")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=1)
            
            logging.info("Create dataset dir folder if not excist")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True) 

            logging.info("save dataset to feature store")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False, header=True)

            #prepare artifact folder
            data_injestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path,
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
            )
            return data_injestion_artifact

        except Exception as e:
            raise FlightPriceException(e, sys)