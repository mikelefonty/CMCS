"""
Questo file contiene varie funzioni di utilità utilizzate per la simulazione.
"""

import sys
sys.path.append('../')
from Simulator_Output.simulator_debug import Simulator_Debug
from CONSTANTS.constant_reader import Constant_Reader
import pandas as pd 
import itertools
import numpy as np
import os

def convert_dictionary(d):
    result_dict = {}
    for key,item in d.items():
        result_dict[int(key)] = item
    return result_dict


def replicate_simulation_from_file(file_path):

    """
    Questa funzione permette di replicare l'animazione della simulazione a partire dai file
    che hanno prefisso "file_path"
    """
    constants = Constant_Reader()

    if not os.path.exists(file_path+'_meta.json'):
        raise  FileNotFoundError(f'{file_path+"_meta.json"} non esiste!!')
        
    df = pd.read_json(file_path+'_meta.json')
  
    
    n_rows= df.iloc[0]['Numero_Righe']
    n_cols = df.iloc[0]['Numero_Colonne']
    n_iters = df.iloc[0]['Numero_Iterazioni']
    sim_type = df.iloc[0]['Tipo_Simulatore']
    k = df.iloc[0]['Raggio_Vicinato']
    ambiente = df.iloc[0]['Nome_Ambiente']

    sim = Simulator_Debug(constants,n_rows,n_cols)

    df_clusters =  pd.read_json(file_path+'_clusters.json')
    
    c = convert_dictionary(df_clusters.iloc[0]['Cluster'])
    p = convert_dictionary(df_clusters.iloc[0]['Positions'])
    

    sim.update(p,clusters=c,new_title=f'{sim_type} su {ambiente}\nRaggio = {k} Iterazione 0/{n_iters}\nNumero totale di clusters = {len(c.keys())}')

    for i in range(1,n_iters+1):
        c = convert_dictionary(df_clusters.iloc[i]['Cluster'])
        p = convert_dictionary(df_clusters.iloc[i]['Positions'])
    
        sim.update(p,clusters=c,new_title=f'{sim_type} su {ambiente}\nRaggio = {k} Iterazione {i}/{n_iters}\nNumero totale di clusters = {len(c.keys())}')

