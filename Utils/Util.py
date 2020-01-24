"""
Questo file contiene funzione di utilità generale, utilizzate all'interno di altri file
per la costruzione dei vari simulatori.
"""
import sys

sys.path.append("../")
import numpy as np
from enum import IntEnum
import pickle
import csv
from matplotlib import pyplot as plt
from textwrap import wrap

"""
----------------STRUTTURE DATI----------------------------------
"""


class Direction(IntEnum):
    """
    Definisce l'insieme delle possibili azioni effettuabili da un generico agente.
    NONE indica che l'agente rimane fermo.
    """
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


N_DIRECTIONS = 9


class Task:
    """
    Definisce un generico Task T=(M,D,P), dove:
        M = Matrice binaria che rappresenta neighborhood
        D = Direzione avente maggiore probabilità
        P = Distribuzione di probabilità P(i) = prob. che l'agente esegua l'azione i
    """

    def __init__(self, matrix, direction, probabilities):
        self.matrix = matrix
        self.direction = direction
        self.probabilities = probabilities

    def __str__(self):
        text = ""
        text = text + "Matrix =\n" + str(self.matrix) + "\n"
        text = text + "Direction: " + str(self.direction) + "\n"
        text = text + "Probabilities: " + str(self.probabilities)
        return text


"""
-------------------END STRUTTURE DATI-------------------------------
"""

"""
------------------FUNZIONI-----------------------------------
"""


def create_matrix(k):
    """
    Crea una matrice binaria di ampiezza kxk.
    La probabilità che una cella abbia valore 1 = 0.5
    :param k: Ampiezza della matrice
    :return: M = Matrice binaria kxk
    """
    M = np.random.randn(k, k) % 1
    for (i, row) in enumerate(M):
        for (j, m) in enumerate(row):
            if m <= 0.5:
                M[i, j] = 0
            else:
                M[i, j] = 1

    M[k // 2, k // 2] = -1
    return M


def create_matrix_with_probs(k, prob_gen_1):
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


def extract_neighborhood(M, k, x, y):
    """
    Data una matrice M, estrae da M una sottomatrice binaria N (neighborhood) centrato in (x,y) di dimensione kxk
    La matrice N è composta in modo tale che N[k//2,k//2] = -1

    :param M: Matrice da cui estrarre il neighborhood
    :param k: Ampiezza del neighborhood
    :param x: Indice di riga in cui centrare l'estrazione del neighborhood
    :param y: Indice di colonna in cui centrare l'estrazione del neighborhood
    :return: N : Matrice binaria del neighborhood
    """
    assert (k > 0) and (k <= min(M.shape[0], M.shape[1])), " Wrong k: k must be in [1,%s] k=%s " % (
        min(M.shape[0], M.shape[1]), k)
    N = np.zeros((k, k), dtype=float)
    x_center = k // 2
    y_center = k // 2

    for i in range(k):
        for j in range(k):
            N[i, j] = M[(x + i - x_center) % M.shape[0], (y - y_center + j) % M.shape[1]]
    N[x_center, y_center] = -1
    return N


def compute_distance(x, y):
    """
    Calcola la distanza tra due vettori x,y utilizzando come metrica la norma 2
    :param x: Vettore
    :param y: Vettore
    :return: Distanza al quadrato dei vettori x,y
    """
    d = np.sum((x - y) ** 2)
    return d


def get_new_position(x, y, n_row, n_col, direction):
    """
    Data la direzione direction, calcola la nuova posizione dell'agente che si sposta da (x,y) nella
    direzione direction.
    NOTA: L'agente non viene mosso.

    :param x: Ascissa del punto iniziale
    :param y: Ordinata del punto iniziale
    :param n_row: Numero di righe dell'ambiente
    :param n_col: Numero di colonne dell'ambiente
    :param direction: Direzione in cui muoversi.
    :return: (x',y'): Nuova posizione dell'agente.
    """
    x_new = x
    y_new = y

    if direction == Direction.UP:
        x_new = (x - 1) % n_row
    elif direction == Direction.DOWN:
        x_new = (x + 1) % n_row
    elif direction == Direction.LEFT:
        y_new = (y - 1) % n_col
    elif direction == Direction.RIGHT:
        y_new = (y + 1) % n_col
    elif direction == Direction.UP_LEFT:
        x_new = (x - 1) % n_row
        y_new = (y - 1) % n_col
    elif direction == Direction.UP_RIGHT:
        x_new = (x - 1) % n_row
        y_new = (y + 1) % n_col
    elif direction == Direction.DOWN_LEFT:
        x_new = (x + 1) % n_row
        y_new = (y - 1) % n_col
    elif direction == Direction.DOWN_RIGHT:
        x_new = (x + 1) % n_row
        y_new = (y + 1) % n_col

    return x_new, y_new


def read_matrix_from_file(path):
    """
    Legge dal file una matrice e la carica in memoria
    :param path: Path del file da cui leggere la matrice
    :return: Matrice M letta da file.
    """
    with open(path, 'r') as f:
        l = [[int(num) for num in line.split(' ')] for line in f]
        matrix = np.array(l)
    return matrix


def get_agents_in_env(environment):
    """
    Dato un ambiente environment, estrae la lista degli agenti presenti nell'ambiente
    :param environment: Matrice che rappresenta l'ambiente
    :return: Lista agents, contenente la posizione (x,y) degli agenti nell'ambiente
    """
    agents = []
    for i in range(environment.shape[0]):
        for j in range(environment.shape[1]):
            if environment[i, j] == 1:
                agents.append((i, j))
    return agents


def generate_new_environment(n_rows, n_cols, n_agents, save_path):
    """
    Crea un nuovo ambiente di dimensione (n_rows x n_cols), in cui sono presenti n_agents agenti.
    L'ambiente viene salvato in save_path.
    :param n_rows: Numero di righe dell'ambiente
    :param n_cols: Numero di colonne dell'ambiente
    :param n_agents: Numero di agenti all'interno dell'ambiente
    :param save_path: Path del file in cui salvare l'ambiente.
    :return: Ambiente env
    """
    env = np.zeros((n_rows, n_cols))
    n_agents_generated = 0

    while n_agents_generated < n_agents:

        x = np.random.randint(0, n_rows)
        y = np.random.randint(0, n_cols)

        if env[x, y] == 0:
            env[x, y] = 1
            n_agents_generated += 1

    with open(save_path, "w") as f:
        np.savetxt(f, env, fmt="%d")

    return env


def compute_cluster_measure(agents, k=5):
    """
    Calcola una misura per calcolare quanto gli agenti siano clusterizzati all'interno dell'ambiente.
    Utilizza una finestra di ampiezza k, centrata in ogni agente presente nella lista agents.
    Dato un agente ed il suo vicinato di ampiezza kxk, calcola il numero di agenti presenti
    nel suo vicinato, compreso l'agente in esame.

    :param agents: Lista contenente la posizione (x,y) di tutti gli agenti nell'ambiente
    :param k: Ampiezza della finestra centrata su ogni agente
    :return: measure: Misura di clustering, mediata sul numero di agenti
    """
    measure = 0
    for agent in agents:
        N = extract_neighborhood(agent.binary_env, k, agent.x, agent.y)
        measure += (np.sum(N) + 1)
    return measure / len(agents)


def count_up(M):
    """
    Conta il numero di agenti presenti nella direzione UP
    :param M: Matrice binaria
    :return: Numero di agenti in UP
    """
    k = M.shape[0]
    M_up = M[:k // 2, :]
    return float(np.sum(M_up))


def count_down(M):
    """
    Conta il numero di agenti presenti nella direzione DOWN
    :param M: Matrice binaria
    :return: Numero di agenti in DOWN
    """
    k = M.shape[0]
    M_down = M[k // 2 + 1:, :]
    return float(np.sum(M_down))


def count_left(M):
    """
    Conta il numero di agenti presenti nella direzione LEFT
    :param M: Matrice binaria
    :return: Numero di agenti in LEFT
    """
    k = M.shape[0]
    M_left = M[:, :k // 2]
    return float(np.sum(M_left))


def count_right(M):
    """
    Conta il numero di agenti presenti nella direzione RIGHT
    :param M: Matrice binaria
    :return: Numero di agenti in RIGHT
    """
    k = M.shape[0]
    M_right = M[:, k // 2 + 1:]
    return float(np.sum(M_right))


def count_up_left(M):
    """
    Conta il numero di agenti presenti nella direzione UP_LEFT
    :param M: Matrice binaria
    :return: Numero di agenti in UP_LEFT
    """
    k = M.shape[0]
    M_up_left = M[:k // 2 + 1, :k // 2 + 1]
    return float(np.sum(M_up_left)) + 1


def count_up_right(M):
    """
    Conta il numero di agenti presenti nella direzione UP_RIGHT
    :param M: Matrice binaria
    :return: Numero di agenti in UP_RIGHT
    """
    k = M.shape[0]
    M_up_right = M[:k // 2 + 1, k // 2:]
    return float(np.sum(M_up_right)) + 1


def count_down_left(M):
    """
    Conta il numero di agenti presenti nella direzione DOWN_LEFT
    :param M: Matrice binaria
    :return: Numero di agenti in DOWN_LEFT
    """
    k = M.shape[0]
    M_down_left = M[k // 2:, :k // 2 + 1]
    return float(np.sum(M_down_left)) + 1


def count_down_right(M):
    """
    Conta il numero di agenti presenti nella direzione DOWN_RIGHT
    :param M: Matrice binaria
    :return: Numero di agenti in DOWN_RIGHT
    """
    k = M.shape[0]
    M_down_right = M[k // 2:, k // 2:]
    return float(np.sum(M_down_right)) + 1


def analyze_neighbors(M):
    """
    Analizza il neighborhood M nelle varie direzioni possibili.
    Per ogni direzione, restituisce il numero di agenti presenti.
    :param M: Matrice binaria
    :return: n_up, n_down, n_left, n_right, n_up_left, n_up_right, n_down_left, n_down_right
    """
    n_up = count_up(M)
    n_down = count_down(M)
    n_left = count_left(M)
    n_right = count_right(M)
    n_up_left = count_up_left(M)
    n_up_right = count_up_right(M)
    n_down_left = count_down_left(M)
    n_down_right = count_down_right(M)
    return n_up, n_down, n_left, n_right, n_up_left, n_up_right, n_down_left, n_down_right


def sample_next_action(probabilities):
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
    while not found_direction and i < len(probabilities):

        prob = float(probabilities[i])

        low = high
        high = high + prob

        if low <= sample <= high:
            found_direction = True
            direction = Direction(i)

        else:
            i += 1

    if not found_direction:
        direction = Direction(i - 1)

    return direction


def pad_matrix(M, pad):
    """
    Applica il padding di zeri ad una matrice M.
    :param M: Matrice a cui effettuare il padding
    :param pad: Dimensione del padding da effettuare
    :return: P: Matrice di dimensione (pad,pad), risultato del padding
    """
    assert pad >= min(M.shape[0], M.shape[1])
    k = M.shape[0]
    P = np.zeros((pad, pad))

    n = M.shape[0]
    m = M.shape[1]

    if k % 2 == 1:
        pn = int(np.ceil((pad - n) / 2.0))
        pm = int(np.floor((pad - m) / 2.0))

    else:
        pn = int(np.ceil((pad - n) / 2.0)) - 1
        pm = int(np.floor((pad - m) / 2.0))

    P[pn:pn + n, pm:pm + m] = M
    return P


def save_object(obj, filename):
    """
    Salva un generico oggetto in un file .pickle
    :param obj: Oggetto da salvare
    :param filename: Path del file in cui salvare l'oggetto
    :return: None
    """
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    """
    Carica un oggetto dal file.
    :param filename: Path del file da cui caricare l'oggetto
    :return: obj: Oggetto caricato
    """
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


def read_measure_file(measure_path):
    """
    Legge il file csv in cui sono contenute le misure effettuate durante una simulazione.
    Restituisce una lista contenente le misure.
    :param measure_path: File da cui leggere le misure
    :return: measures: Lista contenente le misure lette dal file.
    """
    with open(measure_path, newline='') as f:
        reader = csv.DictReader(f)
        measures = []
        for row in reader:
            measures.append(float(row['Measure']))

        return measures


def plot_measures(measures_target=None, measures_nn=None, save_path=None, log_scale=False, title=None):
    """
    Effettua il plotting su un grafico delle misure al variare delle iterazioni.
    :param measures_target: Booleano. Se True crea il grafico delle misure per il simulatore target
    :param measures_nn: Booleano. Se True crea il grafico delle misure per il simulatore con NN
    :param save_path: Path del file in cui salvare il grafico.
                        Se save_path = None, allora il grafico viene mostrato a schermo.
    :param log_scale: Booleano. Se true, il grafico viene prodotto in doppia scala logaritmica.
    :param title: Titolo del grafico.
    :return: None
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if log_scale:
        if measures_target is not None:
            ax.loglog(measures_target, label="Measure Target")
        if measures_nn is not None:
            ax.loglog(measures_nn, label="Measure NN")

    else:
        if measures_target is not None:
            ax.plot(measures_target, label="Measure Target")
        if measures_nn is not None:
            ax.plot(measures_nn, label="Measure NN")

    plt.xlabel("Iterations")
    plt.ylabel("Cluster Measure")
    plt.grid(True)
    plt.tight_layout()
    plt.legend(loc="best")

    if title:
        title = ax.set_title("\n".join(wrap(title, 60)))
        title.set_y(1.05)
        fig.subplots_adjust(top=0.8)

    if save_path:
        fig.savefig(save_path)
    else:
        fig.show()
        fig.waitforbuttonpress()
