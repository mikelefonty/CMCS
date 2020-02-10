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
import os
import logging
logger = tf.get_logger()
logger.setLevel(logging.ERROR)
#tf.logging.set_verbosity(tf.logging.ERROR)
class Simulator:

    def __init__(self,env_file,constants_path=None,show_anim=True,seed=42,use_random_selection=False,neigh_size=5,
    use_stochastic_sim = True,log_path = ".",log_file="risultati_standard_sim",use_nn = False):

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

        if self.use_nn:
            self.sim_type = 'Simulatore Smart'
        else:
            self.sim_type = 'Simulatore Standard'


    def simulate(self,n_iters,verbose=0):
        

        if self.log_file:

            if self.use_nn:
                sim_type = 'Smart'
            else:
                sim_type = 'Standard'

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
            
            if not self.show_anim:
                print(f'Iterazione {i+1}/{n_iters}')

            if i == 0 and not self.use_random_selection:
               agents_order = sorted(agents_order)

            if self.use_random_selection:   
                np.random.shuffle(agents_order)
               
            
            for agent in agents_order:
             
                direction_distribution = self.agents[agent].next_direction(self.env.get_env_matrix(),self.neigh_size,verbose=verbose)

                if self.use_stochastic_sim:
                    best_direction = sample_direction(direction_distribution)
                else:
                    best_direction = Direction(np.argmax(direction_distribution))
               
             
                self.env.move_agent(agent,self.agents[agent].move(best_direction,self.env.get_env_matrix()))
            

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
