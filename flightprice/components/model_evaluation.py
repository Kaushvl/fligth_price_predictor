from flightprice.entity import config_entity, artifact_entity
from flightprice.exception import FlightPriceException
from flightprice.utils import load_object
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
import sys
from flightprice.predictor import ModelResolver
from flightprice.logger import logging 
from flightprice.config import TARGET_COLUMN


class ModelEvaluation:
    def __init__(self, 
                 model_eval_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise FlightPriceException(e , sys)
        
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                              improved_accuracy=None)
                logging.info(f"model eval artifact: {model_eval_artifact}")
                return model_eval_artifact

            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()


            # for previous model
            transformer = load_object(transformer_path)
            model = load_object(model_path)
            target_encoder = load_object(target_encoder_path)

            #for current model 
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df

            input_features_name = list(transformer.feature_names_in_)

            for i in input_features_name:
                if test_df[i].dtypes == 'object':
                    test_df[i] = target_encoder.fit_transform(test_df[i])
            
            input_arr = transformer.transform(test_df[input_features_name])
            y_pred = model.predict(input_arr)

            #comparision btween new and old model

            previous_model_score = r2_score(y_true=y_true,y_pred=y_pred)

            #accuracy current model 

            input_features_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_features_name])
            
            y_pred = current_model.predict(input_arr)
            y_true = target_df

            current_model_score = r2_score(y_true=y_true,y_pred=y_pred)




            #final comparission
            if current_model_score <=  previous_model_score:
                logging.info(f" current model is not better than previous model ")
                raise Exception("current model is not better than previous model")
            
            model_eval_artifact =artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                        improved_accuracy=current_model_score-previous_model_score)
            
            return model_eval_artifact

        except Exception as e:
            raise FlightPriceException(e , sys)
        

        # try:
        #     pass
        # except Exception as e:
        #     raise FlightPriceException(e , sys)
        

        # try:
        #     pass
        # except Exception as e:
        #     raise FlightPriceException(e , sys)
        

        # try:
        #     pass
        # except Exception as e:
        #     raise FlightPriceException(e , sys)