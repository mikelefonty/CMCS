"""
Questo file contiene l'implementazione di un generico agente smart.
"""

import sys
sys.path.append('../')
sys.path.append('./')
from .agent import Agent
import tensorflow as tf 
import numpy as np 
from Util.matrix_functions import extract_neighborhood,binarize_matrix,pad_matrix
from Decide_Direction.decide_direction import choose_direction
import os
import logging
logger = tf.get_logger()
logger.setLevel(logging.ERROR)


class SmartAgent(Agent):

    def __init__(self,agent_id,x,y,model):
        """
        Costruisce un agente smart.
        Oltre ai parametri necessari per istanziare un generico agente,
        si passa il modello di rete neurale da utilizzare per le future predizioni
        """
        super().__init__(agent_id,x,y)
        self.model = model

    def next_direction(self,env,k,verbose=0):
        """
        Calcola la distribuzione di probabilità della direzione da scegliere,
        mediante l'utilizzo della rete neurale.
        """
        
        neigh = binarize_matrix(extract_neighborhood(env,k,self.x,self.y))
        neigh[k//2,k//2] = -1

        if k%2 == 0:
            neigh = pad_matrix(neigh,k+1)
        pred = self.model.predict(np.reshape(np.array(neigh,dtype=float),(1,k + (k%2==0),k + (k%2==0),1)))
        
        if verbose >= 1:
            print('Agent ',self.id)
            print('REAL:\n',choose_direction(env,self.x,self.y,k,verbose>=2))
            print('PREDICTED: \n',np.around(pred,3))
            print()
        
        return pred
        
       