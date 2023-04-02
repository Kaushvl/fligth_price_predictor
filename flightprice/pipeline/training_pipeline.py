from flightprice.entity import config_entity, artifact_entity
from flightprice.exception import FlightPriceException
import sys, os
from flightprice.components.data_ingestion import Dataingestion
from flightprice.components.data_validation import DataValidation
from flightprice.components.data_transformation import DataTransformation
from flightprice.components.model_trainer import ModelTrainer
from flightprice.components.model_pusher import ModelPusher
from flightprice.components.model_evaluation import ModelEvaluation
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

def start_trainig_pipeline():
    try:
        training_pipeline_config = config_entity.TrainigPipelineConfig()


        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion= Dataingestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact =data_ingestion.initiate_data_injestion()


        data_validation_config  = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                         data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        

        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                 data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformatin()


        model_trainer_config = config_entity.ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()


        model_evaluation_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_evaluation = ModelEvaluation(model_eval_config=model_evaluation_config,
                                           data_ingestion_artifact=data_ingestion_artifact,
                                           data_transformation_artifact=data_transformation_artifact,
                                           model_trainer_artifact=model_trainer_artifact)
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()



        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                   data_transformation_artifact=data_transformation_artifact,
                                   model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()



    except Exception as e:
        raise FlightPriceException(e, sys)