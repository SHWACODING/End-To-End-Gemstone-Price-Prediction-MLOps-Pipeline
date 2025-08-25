import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
import kagglehub

from GemstonePricePred.logger.logging import logging
from GemstonePricePred.exception.exception import customexception


@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts", "raw.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")

        try:
            # Download dataset from Kaggle
            dataset_path = kagglehub.dataset_download("dhanrajcodes/gemstone-price")
            logging.info(f"Dataset downloaded at: {dataset_path}")

            # Load CSV (the dataset only has one file: "gemstone.csv")
            data = pd.read_csv(os.path.join(dataset_path, "gemstone.csv"))
            logging.info("Dataset loaded into pandas DataFrame")

            # Save raw data
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Raw dataset saved in artifacts folder")

            # Train-test split
            logging.info("Train Test Split Started.")
            train_data, test_data = train_test_split(data, test_size=0.25, random_state=42)
            logging.info("Train Test Split Completed.")

            # Save train/test datasets
            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Data Ingestion Part Completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.error("Error during Data Ingestion", exc_info=True)
            raise customexception(e, sys)


if __name__ == "__main__":
    DI = DataIngestion()
    DI.initiate_data_ingestion()
