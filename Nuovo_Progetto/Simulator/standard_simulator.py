import sys
sys.path.append('../')
import numpy as np 
from Logger.logger import Logger
from Simulator_Output.simulator_debug import Simulator_Debug
from Agent.agent import Agent
from Environment.environment import Environment
from Util.environment_IO import read_env_from_file
from CONSTANTS.constant_reader import Constant_Reader
from Util.data_structures import Direction
from Util.print_utils import beautify_print_direction
from Decide_Direction.decide_direction import sample_direction
from Clustering.dbscan import DBSCAN 

class Simulator:

    def __init__(self,env_file,constants_path=None,show_anim=True,seed=42,use_random_selection=False,neigh_size=5,use_stochastic_sim = True):

        if constants_path:
            self.constants = Constant_Reader(constants_path)
        else:
            self.constants = Constant_Reader()

        
        self.radius = self.constants.get_radius()
        self.min_pts = self.constants.get_min_pts()
        
        self.env = read_env_from_file(env_file)



        self.neigh_size = neigh_size
        self.seed = seed
        self.use_stochastic_sim = use_stochastic_sim

        np.random.seed(self.seed)
        
        self.use_random_selection = use_random_selection

        self.env_rows, self.env_cols = self.env.get_environment_dimensions()
      
        print(self.env.get_env_matrix())
        
        self.agents = {}
        for i in self.env.get_agents_id_list():
            x,y = self.env.get_agent_position(i)
            self.agents[i] = Agent(i,x,y)

        for _,agent in self.agents.items():
            print(f'Agent {agent.get_id()} --> {agent.get_current_position()}')

        print(self.env_rows,self.env_cols)

        self.logger = Logger(self.constants,'prova_all',['Iterazione','Misura','Tipo_Simulatore','Dimensione_Neigh','Environment_Usato',
                                        'Environment_Inizio_Iterazione','Environment_Fine_Iterazione',
                                        'Dizionario_Azioni_Agenti'],append=False)
        
        self.logger.save_results()

        self.show_anim = show_anim
        if show_anim:
            self.debug_sym = Simulator_Debug(self.constants,self.env_rows,self.env_cols)
        


    def simulate(self,n_iters):
        
        if self.show_anim:
            self.debug_sym.update(self.env.get_agents_dict())

        agents_order = (self.env.get_agents_id_list())
        
        for i in range(n_iters):
            
           
            if i == 0 and not self.use_random_selection:
               agents_order = sorted(agents_order)

            if self.use_random_selection:   
                np.random.shuffle(agents_order)
               
            
            for agent in agents_order:
             
                direction_distribution = self.agents[agent].next_direction(self.env.get_env_matrix(),self.neigh_size,verbose=False)

                if self.use_stochastic_sim:
                    best_direction = sample_direction(direction_distribution)
                else:
                    best_direction = Direction(np.argmax(direction_distribution))
               
             
                self.env.move_agent(agent,self.agents[agent].move(best_direction,self.env.get_env_matrix()))
            
            c,_ = DBSCAN(self.env.get_env_matrix(),self.env.get_agents_dict(),self.radius,self.min_pts)
            self.debug_sym.update(self.env.get_agents_dict(),
                                new_title=f'Iterazione {i+1}/{n_iters}\nNumero totale di clusters = {len(c.keys())}',
                                clusters = c)
