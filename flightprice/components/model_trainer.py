from flightprice.entity import config_entity, artifact_entity
from flightprice.exception import FlightPriceException
from sklearn.linear_model import LinearRegression 
from xgboost import XGBRFRegressor,XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from flightprice import utils
import numpy as np
from sklearn.metrics import r2_score
import sys


class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainingConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise FlightPriceException(e, sys)
        

    def train_model(self,x,y):
        try:
            # lr = LinearRegression()
            # lr.fit(x,y)
            # return lr
            # xgr = XGBRegressor()
            # xgr.fit(x,y)
            # return xgr
            rfr = RandomForestRegressor()
            rfr.fit(x,y)
            return rfr
        except Exception as e:
            raise FlightPriceException(e, sys)
        
    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transform_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transform_test_path)
            

            x_train , y_train = train_arr[:,:-1],train_arr[:,2]
            x_test , y_test = test_arr[:,:-1],test_arr[:,2]


            model = self.train_model(x= x_train,y=y_train)

            yhat_train = model.predict(x_train)
            r2_train_score = r2_score(y_true=y_train,y_pred=yhat_train)

            yhat_test = model.predict(x_test)
            r2_test_score = r2_score(y_true=y_test,y_pred=yhat_test)

            if r2_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f"model is not good as it is not able to give expected accracy : {self.model_trainer_config.expected_accuracy} model actual accuracy : {r2_test_score}")


            diff = abs(r2_train_score - r2_test_score)

            if diff >self.model_trainer_config.overfitting_threshold:
                raise Exception(f"train model and test score diff : {diff} is more than overfitting threshold  {self.model_trainer_config.overfitting_threshold} ")
            
            
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,r2_train_score=r2_train_score,r2_test_score=r2_test_score)
            
            return model_trainer_artifact


        except Exception as e:
            raise FlightPriceException(e, sys)
        