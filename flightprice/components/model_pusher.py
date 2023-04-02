from flightprice.entity import config_entity, artifact_entity
from flightprice.exception import FlightPriceException
from flightprice.utils import load_object,save_object
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
import sys
from flightprice.predictor import ModelResolver
from flightprice.logger import logging
from flightprice.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact
from flightprice.entity.config_entity import ModelPusherConfig
from flightprice.predictor import ModelResolver



class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig,
                 data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)

        except Exception as e:
            raise FlightPriceException(e, sys)
        
    def initiate_model_pusher(self)->ModelPusherArtifact:

        try:
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)


            #model pusher dir
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_dir, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path,obj=target_encoder)



            #save model 
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path,obj=target_encoder)

            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir = self.model_pusher_config.pusher_model_dir,
                                                        saved_model_dir = self.model_pusher_config.saved_model_dir)
            
            return model_pusher_artifact



        except Exception as e:
            raise FlightPriceException(e, sys)
        

        # try:
        #     pass
        # except Exception as e:
        #     raise FlightPriceException(e, sys)
        