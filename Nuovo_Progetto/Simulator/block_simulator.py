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
logger = tf.get_logger()
logger.setLevel(logging.ERROR)


class BlockSimulator:

    def __init__(self,env_file,constants_path=None,show_anim=True,seed=42,use_random_selection=False,neigh_size=5,
    use_stochastic_sim = True,log_path = ".",log_file="risultati_standard_sim",use_nn = False,num_blocks = 1):

        if constants_path:
            self.constants = Constant_Reader(constants_path)
        else:
            self.constants = Constant_Reader()

        self.use_nn = use_nn

        self.log_path = log_path
        self.log_file = log_file

        self.radius = self.constants.get_radius()
        self.min_pts = self.constants.get_min_pts()
        
        self.env_file = env_file
        self.env = read_env_from_file(env_file)



        self.neigh_size = neigh_size
        self.seed = seed
        self.use_stochastic_sim = use_stochastic_sim

        np.random.seed(self.seed)
        
        self.use_random_selection = use_random_selection

        self.env_rows, self.env_cols = self.env.get_environment_dimensions()


        if use_nn:
            assert 2<=self.neigh_size <= 11, 'La dimensione del neighborhood deve essere compresa in [2,11]'
            print(f'Using my_model_{self.neigh_size + (self.neigh_size %2==0)}.h5')
            self.model = keras.models.load_model(f'../Modelli/my_model_{self.neigh_size + (self.neigh_size %2==0)}.h5')
        
        self.agents = {}
        
        for i in self.env.get_agents_id_list():
            x,y = self.env.get_agent_position(i)

            if use_nn:
                 self.agents[i] = SmartAgent(i,x,y,self.model)
            else:
                self.agents[i] = Agent(i,x,y)

        if self.log_file:
            self.logger_clusters = Logger(self.constants,self.log_path,self.log_file+'_clusters',['Iterazione','Cluster','Positions'],append=False)
            self.logger_measures = Logger(self.constants,self.log_path,self.log_file+'_measures',['Iterazione','Misura'],append=False)
            self.logger_matrix = Logger(self.constants,self.log_path,self.log_file+'_matrix',['Iterazione','Ambiente'],append=False)
            self.logger_meta = Logger(self.constants,self.log_path,self.log_file+'_meta',['Nome_Ambiente','Numero_Righe','Numero_Colonne','Raggio_Vicinato',
                                                                            'Tipo_Simulatore','Numero_Iterazioni',
                                                                            'Scelta_Agenti','Strategia_Simulazione'],append=False)
            

            self.logger_matrix.add_row({'Iterazione':0,'Ambiente':np.copy(self.env.get_env_matrix())})
            self.logger_clusters.add_row({'Iterazione':0,'Cluster':{},'Positions':self.env.get_agents_dict()})
     
        self.show_anim = show_anim
        
        if show_anim:
            self.debug_sym = Simulator_Debug(self.constants,self.env_rows,self.env_cols)

        self.blocks = []
        self.num_blocks = num_blocks
        assert 1<=self.num_blocks <= self.env.get_number_of_agents(),"Il numero di blocchi deve essere <= del numero di agenti e  >= 1"

        if self.use_nn:
            self.sim_type = 'Simulatore a blocchi Smart'
        else:
            self.sim_type = 'Simulatore a blocchi Standard'

       

    def __divide_into_blocks(self,agents_list):
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
        #print(self.blocks)
    

    def simulate(self,n_iters,verbose=0):
        

        if self.log_file:

            if self.use_nn:
                sim_type = 'Block_Smart'
            else:
                sim_type = 'Block_Standard'

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
               
        
            self.__divide_into_blocks(agents_order)
            

            for (_,(start,stop)) in enumerate(self.blocks):
                
                
                if self.use_nn:                
                    env_blocks = np.zeros((stop-start,self.neigh_size,self.neigh_size,1))
                    
                    
                    for idx in range(start,stop):
                      
                        current_agent = self.agents[agents_order[idx-1]]

                      
                        neigh =  binarize_matrix(extract_neighborhood(self.env.get_env_matrix(),
                            self.neigh_size, current_agent.get_current_position()[0], current_agent.get_current_position()[1]))
                        neigh[self.neigh_size // 2,self.neigh_size //2 ] = -1
                        
                        env_blocks[idx-start] = np.reshape(np.array(neigh,dtype=float),(self.neigh_size,self.neigh_size,1))

                    direction_distribution = np.around(self.model.predict(env_blocks),3)


                else:
                    direction_distribution = np.zeros((stop-start,1,9))
                    for idx in range(start,stop):
                        
                        current_agent = self.agents[agents_order[idx-1]]
                        #print('Calcolo direzione per agente ',current_agent.get_id())
                        direction_distribution[idx-start,:] = current_agent.next_direction(self.env.get_env_matrix(),self.neigh_size,verbose=verbose)


                for idx in range(start,stop):
                 
                  
                    current_agent = self.agents[agents_order[idx-1]]
                    #print('Muovo agente ',current_agent.get_id())
                    current_direction_distribution = np.reshape(direction_distribution[idx-start,:],(1,9))
                    if self.use_stochastic_sim:
                        best_direction = sample_direction(current_direction_distribution)
                    else:
                        best_direction = Direction(np.argmax(current_direction_distribution))

                    self.env.move_agent(current_agent.get_id(),current_agent.move(best_direction,self.env.get_env_matrix()))
                  

                """
                c,_ = DBSCAN(self.env.get_env_matrix(),self.env.get_agents_dict(),self.radius,self.min_pts)
                if self.show_anim:
                    self.debug_sym.update(self.env.get_agents_dict(),
                                    new_title=f'Blocco {b+1} / {self.num_blocks} Iterazione {i+1}/{n_iters}\nNumero totale di clusters = {len(c.keys())}',
                                    clusters = c)
                """
               

            
            c,_ = DBSCAN(self.env.get_env_matrix(),self.env.get_agents_dict(),self.radius,self.min_pts)
            
            if self.show_anim:
                self.debug_sym.update(self.env.get_agents_dict(),
                                    new_title=f'{self.sim_type}\nRaggio {self.neigh_size} Iterazione {i+1}/{n_iters}\nNumero totale di clusters = {len(c.keys())}',
                                    clusters = c)
            
            if self.log_file:
                self.logger_measures.add_row({'Iterazione':i+1,'Misura':len(c.keys())})
                self.logger_matrix.add_row({'Iterazione':i+1,'Ambiente':np.copy(self.env.get_env_matrix())})
                self.logger_clusters.add_row({'Iterazione':0,'Cluster':c,'Positions':self.env.get_agents_dict()})

        
        if self.log_file:
            self.logger_clusters.save_results()
            self.logger_matrix.save_results()
            self.logger_measures.save_results()
