"""
Questo file contiene l'implementazione della struttura dati Logger, il cui scopo è esclusivamente il
salvataggio di informazioni all'interno dei file
"""

import sys
sys.path.append('../')
import pandas as pd
from CONSTANTS.constant_reader import Constant_Reader
import os


class Logger:

    def __init__(self,constants,result_path,result_name,columns,append=False):
        """
        Costruisce un oggetto Logger.
            -constants : Oggetto di tipo ConstantReader
            - result_path: Path della cartella in cui salvare i file (relativo rispetto alla costante RESULT_DIR)
            - result_name : Nome del file in cui salvare i risultati.
        """ 
        assert isinstance(constants,Constant_Reader)
        assert isinstance(result_path,str)
        
        self.constants = constants #Struttura dati di tipo ConstantReader
        
        if not os.path.isdir(constants.get_result_directory()):
            os.makedirs(constants.get_result_directory())
        
        self.result_path= constants.get_result_directory() + "/"+result_path #Path della cartella in cui salvare i risultati
        self.result_name = result_name+".json"   #Nome del file json in cui salvare i risultati

        
        self.columns = columns #Nomi delle colonne del DataFrame da salvare nel file json
        self.append = append

        if not append:
            self.results_df = pd.DataFrame(columns=self.columns)
        else:
            self.results_df = pd.read_csv(self.result_path+"/"+self.result_name)
        

    def get_column_names(self):
        return list(self.results_df.columns)
    
    def add_row(self,row):
        self.results_df = self.results_df.append(pd.Series(row,index=self.results_df.columns),ignore_index=True)
    
    def save_results(self):
        self.results_df.to_json(self.result_path+"/"+self.result_name)

    def get_results(self):
        return self.results_df
 


