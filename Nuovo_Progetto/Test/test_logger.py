import sys
sys.path.append('../')
from Logger.logger import Logger
from CONSTANTS.constant_reader import Constant_Reader
import numpy as np


constant = Constant_Reader('../CONSTANTS/costanti.json')
logger = Logger(constant,'prova_logger',['id','matrix','Neigh_Size'])
logger.add_row({'id':1,'matrix':np.zeros((3,3),dtype=int),'Neigh_Size':4})
logger.add_row({'id':2,'matrix':np.zeros((3,3),dtype=int),'Neigh_Size':6})
logger.save_results()
print(logger.get_results())

print("NEW LOGGER...")
print("Append il precedente dataset")

logger = Logger(constant,'prova_logger',['id','matrix','Neigh_Size'],append=True)
logger.add_row({'id':7,'matrix':np.ones((3,3),dtype=int),'Neigh_Size':4})
logger.save_results()
print(logger.get_results())
print(logger.get_results()['matrix'][2])