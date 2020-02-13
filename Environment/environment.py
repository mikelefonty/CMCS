"""
Questo file contiene l'implementazione della struttura dati che rappresenta l'ambiente
"""

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
        """
        Aggiunge gli agenti richiesti all'interno dell'ambiente, se non già presenti
        """
        for key in agents_dict.keys():
            
            assert isinstance(key,int)
            assert key > 0
            
            if key not in self.env_dict: 
                self.env_dict[key] = agents_dict[key]
                self.env_matrix[agents_dict[key][0],agents_dict[key][1]] = key
            else:
                print(f'{key} is already in the dict ')
            
    def remove_agent(self,agent_key):
        """
        Rimuove l'agente con ID pari a agent_key, se presente
        """
        if agent_key in self.env_dict.keys():
            self.env_matrix[self.env_dict[agent_key][0],self.env_dict[agent_key][1]] = 0
            del self.env_dict[agent_key]

    def get_env_matrix(self):
        """
        Restituisce la matrice che rappresenta l'ambiente
        """
        return self.env_matrix

    def get_agent_position(self,agent_id):
        """
        Restituisce la posizione dell'agente agent_id
        """
        return self.env_dict[agent_id]

    def get_agents_id_list(self):
        """
        Restituisce una lista contenente tutti e soli gli ID degli agenti presenti nell'ambiente
        """
        agents_list = []
        for agent in self.env_dict.keys():
            agents_list.append(agent)
        return agents_list
    
    def get_number_of_agents(self):
        """
        Restituisce il numero totale di agenti presenti.
        """
        return len(self.get_agents_id_list())
    
    def move_agent(self,agent_id,new_pos):
        """
        Muove l'agente agent_id nella posizione new_pos, aggiornando in modo coerente le varie strutture dati
        """
        if agent_id in self.env_dict.keys():
            self.env_matrix[self.env_dict[agent_id][0],self.env_dict[agent_id][1]] = 0
            self.env_matrix[new_pos[0],new_pos[1]] = agent_id
            self.env_dict[agent_id] = new_pos
    
    def get_environment_dimensions(self):
        """
        Restituisce il numero di righe e colonne dell'ambiente
        """
        return self.n_rows,self.n_cols
    
    def get_agents_dict(self):
        """
        Restituisce una copia del dizionario utilizzato per rappresentare lo stato dell'ambiente.
        """
        agent_dict = {}
        for agent_id,agent_pos in self.env_dict.items():
            agent_dict[agent_id] = agent_pos
        return agent_dict
    