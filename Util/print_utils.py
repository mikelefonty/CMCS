import sys
sys.path.append('../')
from Util.data_structures import Direction
import numpy as np


def beautify_print_direction(direction_vector):
    """
    Questa funzione rende più comprensibile la stampa della distribuzione di probabilità delle direzioni.
    """
    print('Direction\tProbability\n')
    for (idx,d) in enumerate(direction_vector[0]):
        if idx <=3 or idx == 8:
            print(f'{str(Direction(idx))} \t\t{d}')
        else:
            print(f'{str(Direction(idx))} \t{d}')