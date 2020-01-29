"""
Questo file contiene le strutture dati utilizzate nel corso del progetto.
"""
from enum import IntEnum
import sys
sys.path.append("../")

"""
Definisce l'insieme delle possibili azioni effettuabili da un generico agente.
NONE indica che l'agente rimane fermo.
"""


class Direction(IntEnum):

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7
    NONE = 8

    def __str__(self):
        value = self.value
        string_rep = ""
        if value == 0:
            string_rep = "UP"
        elif value == 1:
            string_rep = "DOWN"
        elif value == 2:
            string_rep = "LEFT"
        elif value == 3:
            string_rep = "RIGHT"
        elif value == 4:
            string_rep = "UP_LEFT"
        elif value == 5:
            string_rep = "UP_RIGHT"
        elif value == 6:
            string_rep = "DOWN_LEFT"
        elif value == 7:
            string_rep = "DOWN_RIGHT"
        elif value == 8:
            string_rep = "NONE"

        return string_rep

    @staticmethod
    def get_n_directions():
        return len(list(map(lambda c: c.value, Direction)))

    def direction2pair(self):
        value = self.value
        direction_pair = (0,0)
        if value == 0: #UP
           direction_pair = (-1,0)
        elif value == 1: #DOWN
            direction_pair = (1,0)
        elif value == 2: #LEFT
            direction_pair = (0,-1)
        elif value == 3: #RIGHT
            direction_pair = (0,1)
        elif value == 4: #UP_LEFT
            direction_pair = (-1,-1)
        elif value == 5:#UP_RIGHT
            direction_pair = (-1,1)
        elif value == 6: #DOWN_LEFT
            direction_pair = (1,-1)
        elif value == 7: #DOWN_RIGHT
            direction_pair = (1,1)
        elif value == 8:#NONE
            direction_pair = (0,0)

        return direction_pair
