from flightprice.logger import logging
from flightprice.exception import FlightPriceException
import sys
from flightprice.utils import get_collection_as_dataframe
from flightprice.entity.config_entity import DataIngestionConfig
from flightprice.entity import config_entity 
from flightprice.components.data_ingestion import Dataingestion
from flightprice.components.data_validation import DataValidation
from flightprice.components.model_trainer import ModelTrainer
from flightprice.components.data_transformation import DataTransformation

# def test_logger_and_exception():
    # try:
    #     logging.info("Starting point the test_logger_and_exception")
    #     result = 3/0
    #     print(result)
    #     logging.info("Ending point the test_logger_and_exception")
    # except Exception as e:
    #     logging.debug(str(e))
    #     raise FlightPriceException(e, sys)

if __name__ == "__main__":
    try:
        # test_logger_and_exception()
        # get_collection_as_dataframe(database_name="flight_details", collection_name="flight_database")
        training_pipeline_config = config_entity.TrainigPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config= training_pipeline_config)
        print(data_ingestion_config.to_dict())

        data_injestion = Dataingestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_injestion.initiate_data_injestion()

        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                         data_ingestion_config=data_ingestion_config,
                                         data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()


        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_tarnsformatin = DataTransformation(data_transformation_config=data_transformation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_tarnsformatin.initiate_data_transformatin()


        model_trainer_config  = config_entity.ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()



    except Exception as e:
        print(e)
  