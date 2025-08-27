import os
import sys
import pickle
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from GemstonePricePred.utils.utils import load_object
from GemstonePricePred.logger.logging import logging
from GemstonePricePred.exception.exception import customexception


class ModelEvaluation:
    def __init__(self):
        print("Init... Model Evaluation Stage")
        logging.info("Model Evaluation Sarted")
    
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        
        mae = mean_absolute_error(actual, pred)
        
        r2 = r2_score(actual, pred)
        
        logging.info("Evaluation Metrics Captured!!!")
        
        return rmse, mae, r2
    
    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = (test_array[:, :-1], test_array[:, -1])
            
            model_path = os.path.join("artifacts", "model.pkl")
            
            model = load_object(model_path)

            # mlflow.set_registry_uri("")

            logging.info("Model Has Been Registered.")

            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            print(tracking_url_type_store)

            with mlflow.start_run():
                prediction = model.predict(X_test)
                (rmse, mae, r2) = self.eval_metrics(y_test, prediction)
                
                mlflow.log_metric("RMSE", rmse)
                mlflow.log_metric("MAE", mae)
                mlflow.log_metric("R2", r2)

                # Take a single row from X_test as example
                input_example = pd.DataFrame([X_test[0]], columns=[f"feature_{i}" for i in range(X_test.shape[1])])

                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(model, name="model", registered_model_name="ml_model")
                else:
                    mlflow.sklearn.log_model(model, name="model", input_example=input_example)

        
        except Exception as e:
            raise customexception(e, sys)

