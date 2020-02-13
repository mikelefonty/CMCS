"""
Questo file contiene l'implementazione di un generico agente.
"""
import sys
sys.path.append('../')
from Util.matrix_functions import pad_matrix, extract_neighborhood, binarize_matrix
import numpy as np
from tensorflow import keras
from Decide_Direction.decide_direction import choose_direction
from Util.data_structures import Direction


class Agent:

    def __init__(self, agent_id, x, y):
        self.id = agent_id
        self.x = x
        self.y = y

    def get_id(self):
        """
        Restituisce l'ID dell'agente
        """
        return self.id

    def get_current_position(self):
        """
        Restituisce la posizione corrente dell'agente
        """
        return (self.x, self.y)

    def move(self, direction, env):
        """
        Sposta l'agente nella direzione indicata all'interno dell'ambiente env

        """

        assert isinstance(direction, Direction)

        n_rows = env.shape[0]
        n_cols = env.shape[1]

        dx, dy = direction.direction2pair()
        self.x = (self.x + dx) % n_rows
        self.y = (self.y + dy) % n_cols
        return self.x, self.y

    def next_direction(self, env, k, verbose=0):
        """
        Dati l'ambiente corrente ed il raggio del vicinato,
        calcola la distribuzione di probabilità della direzione successiva.
        """
        return choose_direction(env, self.x, self.y, k, verbose >= 2)
