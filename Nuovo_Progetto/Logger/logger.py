import sys
sys.path.append('../')
import pandas as pd
from CONSTANTS.constant_reader import Constant_Reader
import os


class Logger:

    def __init__(self,constants,result_path,columns,append=False):
        assert isinstance(constants,Constant_Reader)
        assert isinstance(result_path,str)
        
        self.constants = constants
        
        if not os.path.isdir(constants.get_result_directory()):
            os.makedirs(constants.get_result_directory())
        
        self.result_path= constants.get_result_directory() + "/"+result_path+".csv"
        
        #print(self.result_path)
        
        self.columns = columns
        self.append = append

        if not append:
            self.results_df = pd.DataFrame(columns=self.columns)
        else:
            self.results_df = pd.read_csv(self.result_path)

        #print(self.results_df)
        #print(list(self.results_df.columns))
        

    def get_column_names(self):
        return list(self.results_df.columns)
    
    def add_row(self,row):
        self.results_df = self.results_df.append(pd.Series(row,index=self.results_df.columns),ignore_index=True)
    
    def save_results(self):
        self.results_df.to_csv(self.result_path,index=False)

    def get_results(self):
        return self.results_df
 


