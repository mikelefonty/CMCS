from Util.matrix_functions import extract_neighborhood, extract_sub_matrix, binarize_matrix
import math
import numpy as np
from Util.data_structures import Direction
from Util.print_utils import beautify_print_direction
import sys
sys.path.append('../')


def choose_direction(M, x, y, k, verbose=False):

    direction_distribution = np.zeros((1, Direction.get_n_directions()))

    M_neigh = extract_neighborhood(M, k, x, y)
    center = k // 2
    for dir in Direction:
        if not dir.value == Direction.NONE:
            dx, dy = dir.direction2pair()
            if M_neigh[center+dx, center+dy] <= 0:
                if verbose:
                    print(dir)
                    print(f'Neighborhood =\n{M_neigh}\n')

                M_sub = extract_sub_matrix(M_neigh, math.ceil(
                    k/2), math.ceil(k/2), center + math.ceil(k/4)*dx, center + math.ceil(k/4)*dy)

                if verbose:
                    print(f'Sub Matrix considerata =\n{M_sub}\n')
                    print(
                        f'Matrice binaria ottenuta =\n{binarize_matrix(M_sub,thresh=1)}\n')
                    print(
                        f'Densità totale: {np.sum(binarize_matrix(M_sub,thresh=1))}\n')
                direction_distribution[:, dir.value] = np.sum(
                    binarize_matrix(M_sub, thresh=1))

    if np.sum(direction_distribution) == 0:
        direction_distribution[:, Direction.NONE] = 1

    direction_distribution = direction_distribution / np.sum(direction_distribution)
    if verbose:
        print(f'Distribuzione ottenuta = \n')
        beautify_print_direction(direction_distribution)
        print()
    return direction_distribution
