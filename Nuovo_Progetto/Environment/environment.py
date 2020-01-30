import sys
sys.path.append('../')
import numpy as np

class Environment:

    def __init__(self,n_rows,n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.env_matrix = np.zeros((n_rows,n_cols),dtype=int) #Rappresentazione matriciale dell'ambiente: 
                                                    # - se M[x,y] <= 0 => cella vuota, 
                                                    # - se M[x,y] = n > 0 => in (x,y) c'è l'agente con id n 
        self.env_dict = {} #Dizionario del tipo id:(x,y) => l'agente id è in posizione (x,y)
    
    def add_agents(self,agents_dict):
        for key in agents_dict.keys():
            
            assert isinstance(key,int)
            assert key > 0
            
            if key not in self.env_dict: 
                self.env_dict[key] = agents_dict[key]
                self.env_matrix[agents_dict[key][0],agents_dict[key][1]] = key
            else:
                print(f'{key} is already in the dict ')
            
    def remove_agent(self,agent_key):
        if agent_key in self.env_dict.keys():
            self.env_matrix[self.env_dict[agent_key][0],self.env_dict[agent_key][1]] = 0
            del self.env_dict[agent_key]

    def get_env_matrix(self):
        return self.env_matrix

    def get_agent_position(self,agent_id):
        return self.env_dict[agent_id]

    def get_agents_id_list(self):
        agents_list = []
        for agent in self.env_dict.keys():
            agents_list.append(agent)
        return agents_list
    
    def get_number_of_agents(self):
        return len(self.get_agents_id_list())
    
    def move_agent(self,agent_id,new_pos):
        if agent_id in self.env_dict.keys():
            self.env_matrix[self.env_dict[agent_id][0],self.env_dict[agent_id][1]] = 0
            self.env_matrix[new_pos[0],new_pos[1]] = agent_id
            self.env_dict[agent_id] = new_pos
        
    