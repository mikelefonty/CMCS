"""
Questa classe estende la classe Agent ed implementa il cosiddetto Agente Intelligente.
Esso per decidere la direzione e calcolare la distribuzione di probabilità di intraprendere le azioni possibili,
utilizza una rete neurale già addestrata in precedenza.
"""

import sys

sys.path.append("../")
from Agents.Agent import *


class Intelligent_Agent(Agent):

    def __init__(self, nn, id, k, binary_env, x, y, movement, stochastic, save_actions_path, save_neigh_path):
        """
        Costruttore di un Agente Intelligente. Aggiunge all'interno di un agente una rete neurale nn.
        :param nn: Rete Neurale usata per le predizioni.
        :param id: ID univoco dell'agente
        :param k: Ampiezza del vicinato da estrarre
        :param binary_env: Rappresentazione binaria dell'ambiente. (1= è presente un agente, 0 = cella vuota)
        :param x: Indice di riga in cui è presente l'agente
        :param y: Indice della colonna in cui è presente l'agente.
        :param movement: Funzione da utilizzare per calcolare la direzione (density,distance,combine)
        :param stochastic: Se True, la direzione viene scelta in modo stocastico, basandosi sulla distribuzione di probabilità.
                           Altrimenti, viene scelta la direzione con probabilità maggiore. In caso di parità viene scelta a caso.
        :param save_actions_path: Path del file su cui salvare le azioni.
        :param save_neigh_path: Path del file su cui salvare i vicinati estratti nel corso della simulazione.
        """
        super(Intelligent_Agent, self).__init__(id, k, binary_env, x, y, movement, stochastic, save_actions_path,
                                                save_neigh_path)

        self.nn = nn

    def decide_direction(self):
        """
        Decide l'azione da compiere, basandosi sulla predizione della rete neurale incorporata
        all'interno del proprio "stato interno".
        :return: Direzione scelta, distribuzione di probabilità, vicinato estratto.
        """
        N = extract_neighborhood(self.binary_env, self.k, self.x, self.y)
        probs = np.reshape(self.nn.predict(np.reshape(pad_matrix(N, 7), (1, 7, 7, 1))), (-1, 1))

        if self.stochastic:
            direction_res = sample_next_action(probs)
        else:
            direction_res = Direction(np.random.choice(np.flatnonzero(probs == probs.max())))

        return direction_res, probs, N
