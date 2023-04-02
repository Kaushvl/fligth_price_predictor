from flightprice.entity.config_entity import DataIngestionConfig,DataValidationConfig
from flightprice.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from flightprice.exception import FlightPriceException
from flightprice.logger import logging
import pandas as pd
from typing import Optional
import os,sys
from scipy.stats import ks_2samp
import numpy as np
from flightprice.config import TARGET_COLUMN
from flightprice import utils
class DataValidation:
    def __init__(self,
                 data_validation_config:DataValidationConfig, 
                 data_ingestion_config:DataIngestionConfig, 
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_config = data_ingestion_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise FlightPriceException(e, sys)
        
    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            logging.info("droping missing value columns")
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum() / df.shape[0]
            drop_column_names = null_report[null_report > threshold].index
            
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns) == 0:
                return 0
            return df

        except Exception as e:
            raise FlightPriceException(e, sys)


    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            logging.info(f"checking all required columns")
            base_columns = base_df
            current_columns = current_df

            missing_columns =  []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"column : {base_column} is not available")
                    missing_columns.append(base_columns)

            if len(missing_columns)>0:
                self.validation_error[report_key_name] = missing_columns
                return False
            return True
        
        except Exception as e:
            raise FlightPriceException(e, sys)


    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report=dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]
                # logging.info(f"column : {base_column}")
                same_distribution =ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    #We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                    #different distribution

            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise FlightPriceException(e, sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("initiate data validation")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN} ,inplace=True)
            base_df = self.drop_missing_values_columns(df=base_df,report_key_name="Missing_values_within_base_data")


            # train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            # test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("reading train and test df ")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("train and test df loaded")

            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="Missing_values_within_base_data")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="Missing_values_within_base_data")

            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df,exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df,exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df,exclude_columns=exclude_columns)

            
            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")
          
            #write the report
            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
                                  data=self.validation_error)

            data_validation_artifact = DataValidationArtifact(report_file_path = self.data_validation_config.report_file_path)
            
            
            return data_validation_artifact


        except Exception as e:
            raise FlightPriceException(e, sys)