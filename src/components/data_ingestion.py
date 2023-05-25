#Read the data from data sources

import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd


from sklearn.model_selection import train_test_split
from dataclasses import dataclass   # this is use for class variable

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
 
@dataclass
##  here we are decideding where the train, test,raw data will ingect/store
## the decorator(@dataclass) is using coz.....normally to define the variable inside the class we use init but here we are not using init 
## thats why decorator is needed., so here we can directly define the class varibles
class DataIngestionConfig:
    train_data_path: str =os.path.join('artifacts',"train.csv")  # all the output data will be stored in this artifacts folder on the given  path
                                    #train.csv is the file name
    test_data_path: str =os.path.join('artifacts',"test.csv")
    raw_data_path: str =os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    def intiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as frame')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False, header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False, header=True)

            logging.info("INgestion of the data completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path


            ) # return this coz it will use in data transformation


        except  Exception as e:
            raise CustomException  (e,sys)
        
if __name__=='__main__':
    obj=DataIngestion()
    train_data,test_data=obj.intiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_= data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
