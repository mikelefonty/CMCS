"""
Questo file contiene l'implementazione della funzione utilizzata per calcolare la distribuzione di 
probabilità della direzione da scegliere.
"""
import sys
sys.path.append('../')
from Util.matrix_functions import extract_neighborhood, extract_sub_matrix, binarize_matrix
import math
import numpy as np
from Util.data_structures import Direction
from Util.print_utils import beautify_print_direction


def choose_direction(M, x, y, k, verbose=False):

    direction_distribution = np.zeros((1, Direction.get_n_directions()))

    M_neigh = extract_neighborhood(M, k, x, y)
    
    """
    Vicinato completamente vuoto => Ogni direzione è equiprobabile
    """
    if np.sum(M_neigh) == -1:
        for d in Direction:
            if not d == Direction.NONE:
                direction_distribution[:,d.value] = 1
    
    else:
        center = k // 2
        for d in Direction:
            if not d == Direction.NONE:
                dx, dy = d.direction2pair()
                if M_neigh[center+dx, center+dy] <= 0:
                    if verbose:
                        print(d)
                        print(f'Neighborhood =\n{M_neigh}\n')

                    """
                    Estraggo la sottomatrice centrata nel punto medio della direzione d
                    """
                    M_sub = extract_sub_matrix(M_neigh, math.ceil(
                        k/2), math.ceil(k/2), center + math.ceil(k/4)*dx, center + math.ceil(k/4)*dy)

                    if verbose:
                        print(f'Sub Matrix considerata =\n{M_sub}\n')
                        print(
                            f'Matrice binaria ottenuta =\n{binarize_matrix(M_sub,thresh=1)}\n')
                        print(
                            f'Densità totale: {np.sum(binarize_matrix(M_sub,thresh=1))}\n')
                    direction_distribution[:, d.value] = np.sum(
                        binarize_matrix(M_sub, thresh=1))

        """
        Nessuna direzione è disponibile => Direzione = NONE con probabilità 1
        """
        if np.sum(direction_distribution) == 0:
            direction_distribution[:, Direction.NONE] = 1

    """
    Ottengo la distribuzione di probabilità richiesta
    """
    
    direction_distribution = np.around(direction_distribution / np.sum(direction_distribution),3)
    if verbose:
        print(f'Distribuzione ottenuta = \n')
        beautify_print_direction(direction_distribution)
        print()
    return direction_distribution


def sample_direction(probabilities):
    """
    Seleziona una azione effettuando il sampling dalla distribuzione contenuta in probabilities.
    :param probabilities: Vettore che rappresenta la distribuzione di probabilità
            da cui effettuare il sampling
    :return: action: Azione scelta.
    """
    sample = np.random.random()

    low = 0
    high = 0

    found_direction = False
    direction = -1

    i = 0
   
    "Effettua l'univariate sampling"
    while not found_direction and i < probabilities.shape[1]:

        prob = float(probabilities[:,i])
        
        low = high
        high = high + prob

        if low <= sample <= high:
            found_direction = True
            direction = Direction(i)

        else:
            i += 1

    if not found_direction:
        direction = Direction.NONE

    return direction
