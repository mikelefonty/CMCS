"""
Questo file contiene le funzioni utilizzabili per calcolare la direzione da scegliere per ogni agente.
"""

import sys
sys.path.append("../")
from Utils.Util import *
import random


"""
----------------------DENSITA'--------------------------------------
"""


def compute_direction_density(M):
    """
    Calcola la direzione basandosi sulla densità
    :param M: Matrice binaria dell'ambiente.
    :return: direction: Direzione più probabile, probabilities: Distribuzione di probabilità
    """
    k = M.shape[0]

    x = k // 2
    y = k // 2

    """
    Conta il numero di agenti nel suo vicinato
    """
    n_up, n_down, n_left, n_right, n_up_left, \
    n_up_right, n_down_left, n_down_right = analyze_neighbors(M)

    n_neighbors = n_up + n_down + n_left + n_right + \
                  n_up_left + n_up_right + n_down_left + n_down_right

    possible_directions = 8

    """
    Dizionario binario: Il generico elemento d:1 indica che la direzione d è libera.
    """
    possible_directions_dict = {Direction.UP: 1, Direction.DOWN: 1, Direction.LEFT: 1, Direction.RIGHT: 1,
                                Direction.UP_LEFT: 1, Direction.UP_RIGHT: 1, Direction.DOWN_LEFT: 1,
                                Direction.DOWN_RIGHT: 1}

    """
    Contiene la distribuzione di probabilità di poter prendere una determinata direzione.
    """
    probabilities = np.zeros(9)

    """
    Controlla quali direzioni sono libere
    """
    # Controllo UP
    if M[x - 1, y] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.UP] = 0
    else:
        probabilities[Direction.UP.value] = n_up / (k * (k // 2))

    # controllo DOWN
    if M[x + 1, y] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.DOWN] = 0
    else:
        probabilities[Direction.DOWN.value] = n_down / (k * (k // 2))
    # Controllo LEFT
    if M[x, y - 1] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.LEFT] = 0
    else:
        probabilities[Direction.LEFT.value] = n_left / (k * (k // 2))

    # Controllo RIGHT
    if M[x, y + 1] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.RIGHT] = 0
    else:
        probabilities[Direction.RIGHT.value] = n_right / (k * (k // 2))

    # Controllo UP_LEFT
    if M[x - 1, y - 1] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.UP_LEFT] = 0
    else:
        probabilities[Direction.UP_LEFT.value] = n_up_left / ((k // 2 + 1) ** 2 - 1)

    # Controllo UP_RIGHT
    if M[x - 1, y + 1] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.UP_RIGHT] = 0
    else:
        probabilities[Direction.UP_RIGHT.value] = n_up_right / ((k // 2 + 1) ** 2 - 1)

    # Controllo DOWN_LEFT
    if M[x + 1, y - 1] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.DOWN_LEFT] = 0
    else:
        probabilities[Direction.DOWN_LEFT.value] = n_down_left / ((k // 2 + 1) ** 2 - 1)

    # Controllo DOWN_RIGHT
    if M[x + 1, y + 1] == 1:
        possible_directions -= 1
        possible_directions_dict[Direction.DOWN_RIGHT] = 0
    else:
        probabilities[Direction.DOWN_RIGHT.value] = n_down_right / ((k // 2 + 1) ** 2 - 1)

    """
    Se possible_directions è pari a 0, significa che l'agente deve stare fermo.
    Direzione obbligata è NONE.
    """
    if possible_directions == 0:
        direction = Direction.NONE
        probabilities[Direction.NONE.value] = 1

    else:

        if n_neighbors == 0:
            """
            L'agente ha il vicinato completamente vuoto.
            Sceglie a caso una direzione diversa da NONE.
            """
            rnd_dir = np.random.randint(0, N_DIRECTIONS-1)
            direction = Direction(rnd_dir)
            for prob_dir in range(N_DIRECTIONS-1):
                probabilities[prob_dir] = 1 / (N_DIRECTIONS - 1)

        else:
            """
            Esiste almeno una direzione disponibile ed esiste almeno un agente nel vicinato.
            """
            sum_probs = np.sum(probabilities)

            if sum_probs == 0:
                """
                Esistono posizioni libere in cui andare ma le zone in quelle direzioni 
                sono tutte completamente vuote.
                L'agente sceglie a caso tra una di esse con la stessa probabilità
                """

                candidate_directions = []

                for curr_dir in possible_directions_dict:
                    if possible_directions_dict[curr_dir] == 1:
                        candidate_directions.append(curr_dir)

                num_dirs = len(candidate_directions)
                for curr_dir in candidate_directions:
                    probabilities[curr_dir.value] = 1. / num_dirs

                direction = Direction(random.choice(candidate_directions).value)

            else:
                """
                Il valore di sum_probs è diverso da zero, quindi posso usarlo per normalizzare
                probabilities.
                """
                probabilities = probabilities / sum_probs
                direction = Direction(int(np.argmax(probabilities)))

    return direction, probabilities


"""
------------------------DISTANZA---------------------------------------------
"""


def compute_direction_distance(N):
    """
    Sceglie la direzione d che minimizza la distanza media con gli altri agenti presenti nel vicinato.
    :param N: Matrice del neighborhood
    :return: direzione migliore, vettore delle distanze, distribuzione di probabilità
    """
    agents_pos_x = []
    agents_pos_y = []

    available_directions = []

    """
    Vettore di che contiene la distanza dagli altri agenti nel vicinato, 
    se l'agente si sposta nella direzione d, diversa da NONE.
    Inizialmente le distanze sono poste a +infinito.
    """
    distances = np.zeros(N_DIRECTIONS - 1) + np.inf

    probabilities = np.zeros(N_DIRECTIONS)

    k = N.shape[0]

    """
    Costruisce le liste con le posizioni degli agenti nel vicinato.
    """
    for i in range(k):
        for j in range(k):
            if N[i, j] > 0:
                agents_pos_x.append(i)
                agents_pos_y.append(j)

    if len(agents_pos_x) == 0:
        """
        Non vi sono agenti nel vicinato.
        L'agente sceglie una direzione a caso, diversa da NONE.
        """
        rnd_dir = np.random.randint(0, N_DIRECTIONS - 1)
        for prob_dir in range(N_DIRECTIONS - 1):
            probabilities[prob_dir] = 1 / (N_DIRECTIONS - 1)
        return Direction(rnd_dir), distances, probabilities

    for i in range(N_DIRECTIONS - 1):
        """
        Esiste almeno un agente nel vicinato.
        Data una generica direzione d, l'agente ottiene le coordinate della nuova posizione nel caso
        scegliesse di spostarsi lungo d.
        Se non è percorribile, cioè è già occupata da un altro agente, allora la elimina dalle scelte possibili.
        """
        new_x, new_y = get_new_position(k // 2, k // 2, k, k, Direction(i))
        if N[new_x, new_y] == 0:  # or N[new_x, new_y] == -1:
            available_directions.append(Direction(i))

    if len(available_directions) == 0:
        """
        Se non vi sono direzioni disponibili, sono cioè già tutte occupate, allora la direzione scelta è 
        NONE, con probabilità 1.
        """
        probabilities[Direction.NONE.value] = 1
        return Direction.NONE, distances, probabilities

    for direction in available_directions:
        """
        Per ogni direzione disponibile d, calcola la distanza media tra l'agente in esame e
        gli altri agenti del vicinato.
        L'agente sceglie di muoversi nella direzione d, con probabilità
        P(d) = 1 / [(distanza_lungo_d) **2]
        """
        new_x, new_y = get_new_position(k // 2, k // 2, k, k, direction)
        curr_dist = 0

        for i in range(len(agents_pos_x)):
            x = np.reshape(np.array([new_x, new_y]), (-1, 1))
            y = np.reshape(np.array([agents_pos_x[i], agents_pos_y[i]]), (-1, 1))
            d = compute_distance(x, y)
            curr_dist += d

        d = curr_dist / len(agents_pos_x)

        distances[direction.value] = d
        probabilities[direction.value] = 1 / (d ** 2)

    """
    La direzione migliore è quella che minimizza la distanza media.
    """
    return Direction(np.argmin(distances)), distances, probabilities / np.sum(
        probabilities)


"""
-----------------------------COMBINE--------------------------------------
"""


def combine(N):
    """
    Sceglie la direzione, combinando equamente le tecniche di densità e distanza.
    :param N: Matrice del neighborhood
    :return: Direzione migliore,distribuzione di probabilità
    """

    """
    Calcola distanza e densità
    """
    dir_dist,_, probs_dist = compute_direction_distance(N)
    dir_dens,probs_dens = compute_direction_density(N)

    """
    La probabilità risultante è la media delle probabilità risultanti da
    densità e distanza.
    """
    probs_res = (probs_dist+probs_dens) / 2
    probs_res /= np.sum(probs_res)
    dir_res = Direction(np.argmax(probs_res))
    return dir_res,probs_res
