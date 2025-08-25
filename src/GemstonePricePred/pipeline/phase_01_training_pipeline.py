from GemstonePricePred.logger.logging import logging
from GemstonePricePred.exception.exception import customexception
import pandas as pd

from GemstonePricePred.components.stage_01_data_ingestion import DataIngestion 
from GemstonePricePred.components.stage_02_data_transformation import DataTransformation
from GemstonePricePred.components.stage_03_model_trainer import ModelTrainer
# from GemstonePricePred.components.model_evaluation import ModelEvaluation


obj=DataIngestion()

train_data_path, test_data_path = obj.initiate_data_ingestion()

data_transformation = DataTransformation()

train_arr, test_arr = data_transformation.initate_data_transformation(train_data_path, test_data_path)


model_trainer_obj = ModelTrainer()
model_trainer_obj.initate_model_training(train_arr, test_arr)

# model_eval_obj = ModelEvaluation()
# model_eval_obj.initiate_model_evaluation(train_arr,test_arr)