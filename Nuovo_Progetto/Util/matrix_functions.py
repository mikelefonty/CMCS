"""
Questo file contiene le funzioni di utilità che permettono di lavorare con le matrici/sotto-matrici.
"""

import numpy as np
import sys
sys.path.append("../")


def extract_neighborhood(M, k, x, y):
    """
    Data una matrice M, estrae da M una sottomatrice N (neighborhood) centrato in (x,y) di dimensione kxk
    La matrice N è composta in modo tale che N[k//2,k//2] = -1

    :param M: Matrice da cui estrarre il neighborhood
    :param k: Ampiezza del neighborhood
    :param x: Indice di riga in cui centrare l'estrazione del neighborhood
    :param y: Indice di colonna in cui centrare l'estrazione del neighborhood
    :return: N : Matrice binaria del neighborhood
    """
    assert (k > 0) and (k <= min(M.shape[0], M.shape[1])), " Wrong k: k must be in [1,%s] k=%s " % (
        min(M.shape[0], M.shape[1]), k)

    N = np.zeros((k, k), dtype=int)
    x_center = k // 2
    y_center = k // 2

    for i in range(k):
        for j in range(k):
            N[i, j] = M[(x + i - x_center) % M.shape[0],
                        (y - y_center + j) % M.shape[1]]
    N[x_center, y_center] = -1
    return N


def binarize_matrix(M, thresh=0.5):
    """
    Rende la matrice M binaria.
    Per ogni elemento m:
     - se m < thresh -> m = 0
     - se m >= thresh -> m = 1
    """
    
    N = np.zeros(M.shape)
    N[M >= thresh] = 1
    return N


def create_binary_matrix(k, prob_gen_1=0.5):
    """
    Crea una matrice binaria kxk.
    La probabilità che una cella M_{ij} = 1 è pari a prob_gen_1
    :param k: Ampiezza della matrice M
    :param prob_gen_1: Probabilità che un elemento M_{ij} = 1
    :return: M: Matrice binaria kxk
    """
    assert (prob_gen_1 <= 1) and (prob_gen_1 >= 0)

    M = np.random.randn(k, k) % 1
    for (i, row) in enumerate(M):
        for (j, m) in enumerate(row):
            if m <= prob_gen_1:
                M[i, j] = 1
            else:
                M[i, j] = 0

    M[k // 2, k // 2] = -1
    return M


def extract_sub_matrix(A, m, n, cx, cy):
    """
    Estrae una sottomatrice di A di dimensione AL PIU' m x n, centrata in (cx,cy).
    L'operazione non viene fatta utilizzando l'aritmetica modulare!
    """
    assert 0<=cx<A.shape[0]
    assert 0<=cy<A.shape[1]    
    B = np.zeros(A.shape)
    B = A[max(0, cx - (m // 2)): min(cx + (m//2) + (m % 2 > 0), A.shape[0]),
          max(0, cy - (n // 2)):  min(cy + (n // 2) + (n % 2 > 0), A.shape[1])]
    return B
