"""
Questo file contiene l'implementazione del Block Simulator.
"""

import sys
sys.path.append('../')
import numpy as np 
from Logger.logger import Logger
from Simulator_Output.simulator_debug import Simulator_Debug
from Agent.agent import Agent
from Agent.smart_agent import SmartAgent
from Environment.environment import Environment
from Util.environment_IO import read_env_from_file
from CONSTANTS.constant_reader import Constant_Reader
from Util.data_structures import Direction
from Util.print_utils import beautify_print_direction
from Decide_Direction.decide_direction import sample_direction
from Clustering.dbscan import DBSCAN 
import tensorflow as tf
from tensorflow import keras
from Util.matrix_functions import extract_neighborhood,binarize_matrix
import os
import logging
from .standard_simulator import Simulator
logger = tf.get_logger()
logger.setLevel(logging.ERROR)


class BlockSimulator(Simulator):

    def __init__(self,env_file,constants_path=None,show_anim=True,seed=42,use_random_selection=False,neigh_size=7,
    use_stochastic_sim = True,log_path = ".",log_file="risultati_standard_sim",use_nn = False,num_blocks = 1):
        """
        Crea l'oggetto Block Simulator.
        Stessi parametri della classe padre Simulator, più 
            - num_blocks : numero di blocchi in cui dividere la lista degli agenti
        """
        super().__init__(env_file,constants_path,show_anim,seed,use_random_selection,use_stochastic_sim,
        neigh_size,log_path,log_file,use_nn)

        self.blocks = []
        self.num_blocks = num_blocks
        assert 1<=self.num_blocks <= self.env.get_number_of_agents(),"Il numero di blocchi deve essere <= del numero di agenti e  >= 1"


    def __divide_into_blocks(self,agents_list):
        """
        Divide in self.num_blocks blocchi la lista agents_list.
        Ogni blocco è rappresentato da una coppia (start,stop).
        Ciò significa che all'interno del blocco sono presenti tutti gli agenti aventi
        ID in [start,stop)
        """
        self.blocks.clear()
        N = len(agents_list)
        start = 1
        stop = 1
        modulus = N % self.num_blocks
        block_size = N // self.num_blocks

        for _ in range(self.num_blocks):
            stop = start + block_size + (modulus > 0)
            self.blocks.append( (start,stop))
            modulus -= 1
            start = stop
    

    def simulate(self,n_iters,verbose=0):
        """
        Esegue n_iters_iterazioni di simulazione
        """

        if self.log_file:

            if self.use_nn:
                sim_type = f'Block_Smart {self.num_blocks} blocchi'
            else:
                sim_type = f'Block_Standard {self.num_blocks} blocchi'

            if self.use_random_selection:
                sim_agent_sel = 'random'
            else:
                sim_agent_sel = 'sequential'

            if self.use_stochastic_sim:
                sim_strategy = 'stochastic'
            else:
                sim_strategy = 'deterministic'

            self.logger_meta.add_row({'Nome_Ambiente':self.env_file,'Numero_Righe':self.env_rows,'Numero_Colonne':self.env_cols,
                                    'Raggio_Vicinato':self.neigh_size,
                                    'Tipo_Simulatore':sim_type,'Numero_Iterazioni':n_iters,
                                    'Scelta_Agenti':sim_agent_sel,
                                    'Strategia_Simulazione':sim_strategy
                                    })
                                    
            self.logger_meta.save_results()

        if self.show_anim:
            self.debug_sym.update(self.env.get_agents_dict())



        agents_order = (self.env.get_agents_id_list())
        
       
        #CICLO DELLE ITERAZIONI
        for i in range(n_iters):
            
            if self.show_anim and i ==0:
                c,_ = DBSCAN(self.env.get_env_matrix(),self.env.get_agents_dict(),self.radius,self.min_pts)
                self.debug_sym.update(self.env.get_agents_dict(),
                                    new_title=f'{self.sim_type}\nSituazione iniziale\nNumero totale di clusters = {len(c.keys())}',
                                    clusters = c)

            if not self.show_anim:
                print(f'Iterazione {i+1}/{n_iters}')

            if i == 0 and not self.use_random_selection:
               agents_order = sorted(agents_order)

            if self.use_random_selection:   
                np.random.shuffle(agents_order)
               
            #DIVIDE IN BLOCCHI LA LISTA DELL' ORDINE DEGLI AGENTI
            self.__divide_into_blocks(agents_order)
            
            #PER OGNI BLOCCO:
            for (_,(start,stop)) in enumerate(self.blocks):
                
                #Se si usa un simulatore SMART:
                if self.use_nn:

                    #Tensore contenente i vari vicinati degli agenti del blocco.
                    # Serve come input alla rete, la quale produce in output il tensore con le 
                    # distribuzioni di probabilità delle direzioni                
                    env_blocks = np.zeros((stop-start,self.neigh_size,self.neigh_size,1))
                    

                    """
                    Per ogni agente all'interno del blocco corrente:
                        - Seleziona agente dalla lista degli ordini.
                        - Estrae il vicinato
                        - Rende binario la matrice del vicinato
                        - Aggiunge questo risultato nella riga corrente del tensore env_block
                    """                    
                    for idx in range(start,stop):  
                        current_agent = self.agents[agents_order[idx-1]]

                        neigh =  binarize_matrix(extract_neighborhood(self.env.get_env_matrix(),
                            self.neigh_size, current_agent.get_current_position()[0], current_agent.get_current_position()[1]))
                        neigh[self.neigh_size // 2,self.neigh_size //2 ] = -1
                        
                        env_blocks[idx-start] = np.reshape(np.array(neigh,dtype=float),(self.neigh_size,self.neigh_size,1))


                    """
                    Una volta costruito il tensore, il simulatore lo dà in input al
                    modello di rete neurale, ottenendo la distribuzione cercata
                    """

                    direction_distribution = np.around(self.model.predict(env_blocks),3)

                else:
                    """
                    SE non si usa un simulatore smart:
                    - per ogni agente del blocco, calcola la distribuzione delle direzioni e salvale in un tensore di output.
                    """
                    direction_distribution = np.zeros((stop-start,1,9))

                    for idx in range(start,stop):                        
                        current_agent = self.agents[agents_order[idx-1]]
                        direction_distribution[idx-start,:] = current_agent.next_direction(self.env.get_env_matrix(),self.neigh_size,verbose=verbose)


                """
                Una volta ottenute le varie distribuzioni per ogni agente, 
                aggiorna l'ambiente, muovendo i vari agenti
                """
                for idx in range(start,stop):
                
                    current_agent = self.agents[agents_order[idx-1]]
                    current_direction_distribution = np.reshape(direction_distribution[idx-start,:],(1,9))
                    if self.use_stochastic_sim:
                        best_direction = sample_direction(current_direction_distribution)
                    else:
                        best_direction = Direction(np.argmax(current_direction_distribution))

                    self.env.move_agent(current_agent.get_id(),current_agent.move(best_direction,self.env.get_env_matrix()))
                
            """
            Al termine della iterazione, usa DBSCAN per misurare il numero di clusters.
                NOTA: DBSCAN CONSIDERA EVENTUALI AGENTI SOVRAPPOSTI, COME APPARTENENTI A CLUSTERS DIVERSI!!!
            """             
            c,_ = DBSCAN(self.env.get_env_matrix(),self.env.get_agents_dict(),self.radius,self.min_pts)
            
            if self.show_anim:
                self.debug_sym.update(self.env.get_agents_dict(),
                                    new_title=f'{sim_type}\nRaggio {self.neigh_size} Iterazione {i+1}/{n_iters}\nNumero totale di clusters = {len(c.keys())}',
                                    clusters = c)
            
            if self.log_file:
                self.logger_measures.add_row({'Iterazione':i+1,'Misura':len(c.keys())})
                self.logger_matrix.add_row({'Iterazione':i+1,'Ambiente':np.copy(self.env.get_env_matrix())})
                self.logger_clusters.add_row({'Iterazione':0,'Cluster':c,'Positions':self.env.get_agents_dict()})

        
        if self.log_file:
            self.logger_clusters.save_results()
            self.logger_matrix.save_results()
            self.logger_measures.save_results()
