import os, sys
from datetime import datetime
from flightprice.exception import FlightPriceException

FILE_NAME = "flight_price.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"


class TrainigPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%Y%m%d__%H%M%S')}")
        except Exception as e:
            raise FlightPriceException(e, sys)
        

class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainigPipelineConfig):
        try:
            self.database_name = "flight_details"
            self.collection_name = "flight_database"
            self.data_injestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_injestion")
            self.feature_store_file_path = os.path.join(self.data_injestion_dir,"feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_injestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_injestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e:
            raise FlightPriceException(e, sys)
    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise FlightPriceException(e, sys)

class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainigPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_threshold:float = 0.2
        self.base_file_path = os.path.join("flight_price.csv")
    
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainigPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
        self.transform_train_path =  os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))
        self.transform_test_path =os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
        self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)



class ModelTrainingConfig:
    def __init__(self,training_pipeline_config:TrainigPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,'model_trainer')
        self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
        self.expected_accuracy = 0.7
        self.overfitting_threshold = 0.3
    