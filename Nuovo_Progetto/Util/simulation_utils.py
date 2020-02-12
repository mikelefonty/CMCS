import sys
sys.path.append('../')
from Simulator_Output.simulator_debug import Simulator_Debug
from CONSTANTS.constant_reader import Constant_Reader
import pandas as pd 
import itertools
import numpy as np
import ast

def convert_dictionary(d):
    result_dict = {}
    for key,item in d.items():
        result_dict[int(key)] = item
    return result_dict


def replicate_simulation_from_file(file_path):

    constants = Constant_Reader()

    df = pd.read_json(constants.get_result_directory()+"/"+file_path+'_meta.json')
  
    
    n_rows= df.iloc[0]['Numero_Righe']
    n_cols = df.iloc[0]['Numero_Colonne']
    n_iters = df.iloc[0]['Numero_Iterazioni']


    sim = Simulator_Debug(constants,n_rows,n_cols)

    df_clusters =  pd.read_json(constants.get_result_directory()+"/"+file_path+'_clusters.json')
    
    c = convert_dictionary(df_clusters.iloc[0]['Cluster'])
    p = convert_dictionary(df_clusters.iloc[0]['Positions'])
    

    sim.update(p,clusters=c,new_title=f'Iterazione 0/{n_iters}\nNumero totale di clusters = {len(c.keys())}')

    for i in range(1,n_iters+1):
        c = convert_dictionary(df_clusters.iloc[i]['Cluster'])
        p = convert_dictionary(df_clusters.iloc[i]['Positions'])
    
        sim.update(p,clusters=c,new_title=f'Iterazione {i}/{n_iters}\nNumero totale di clusters = {len(c.keys())}')

