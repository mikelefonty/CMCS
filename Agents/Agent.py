"""
Questa classe implementa la struttura di un generico Agente (non intelligente).
Lo scopo principale di un agente, è quello di calcolare la distribuzione di probabilità
delle varie azioni, in modo da decidere quale sia l'azione da compiere durante l'iterazione corrente.
La scelta delle azioni da intraprendere si basa esclusivamente sul contenuto del vicinato di ampiezza k.

"""

import sys

sys.path.append("../")
from Utils.Util_Directions import *
import csv
from pandas import *


class Agent:

    def __init__(self, id, k, binary_env, x, y, movement, stochastic,
                 save_actions_path, save_neigh_path):
        """
        Costruttore di un Agente.

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

        self.k = k
        self.binary_env = binary_env

        self.x = x
        self.y = y
        self.n_rows = self.binary_env.shape[0]
        self.n_cols = self.binary_env.shape[1]
        self.id = id
        self.movement = movement
        self.stochastic = stochastic

        self.save_actions_path = save_actions_path

        self.field_actions = ['Iter', 'ID', 'Action', 'P(UP)', 'P(DOWN)', 'P(LEFT)',
                              'P(RIGHT)',
                              'P(UP_LEFT)',
                              'P(UP_RIGHT)', 'P(DOWN_LEFT)', 'P(DOWN_RIGHT)', 'P(NONE)']
        self.save_neigh_path = save_neigh_path
        self.field_neigh = ['Iteration', 'AgentID', "Neighbours"]

        "Indica l'ultima azione eseguita"
        self.last_action = None

        "Indica l'ultima distribuzione ottenuta"
        self.last_probs = None

        "Iterazione corrente"
        self.iter = 0

    def save_actions_to_file(self):
        """
        Salva le azioni intraprese nel corso delle varie iterazioni della simulazione su file.
        :return:
        """

        self.act_dict['Iter'] = [self.iter]
        self.act_dict['ID'] = [self.id]
        self.act_dict['Action'] = [str(self.last_action)]

        for i in range(N_DIRECTIONS):
            str_dir = str(Direction(i))
            self.act_dict['P(%s)' % (str_dir)] = [float("%.3f" % (self.last_probs[i]))]

        df = DataFrame(self.act_dict, columns=self.field_actions)

        csv = df.to_csv(self.save_actions_path, index=None, mode="a", header=False)

    def save_neighborhood_to_file(self, N):
        """
        Salva il neighborhood N su file
        :param N: Neighborhood da salvare
        :return:
        """
        with open(self.save_neigh_path, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.field_neigh, delimiter=",")
            writer.writerow(
                {"Iteration": self.iter, "AgentID": self.id, "Neighbours": "\n%s" % N})

    def save_actions_to_dict(self, act_dict):
        """
        Salva l'ultima azione eseguita all'interno del dizionario act_dict
        :param act_dict: Dizionario contenente la lista delle azioni eseguite.
        :return: Dizionario a cui è stata aggiunta l'ultima azione.
        """
        act_dict['Iter'].append(self.iter)
        act_dict['ID'].append(self.id)
        act_dict['Action'].append(str(self.last_action))

        for i in range(N_DIRECTIONS):
            str_dir = str(Direction(i))
            act_dict['P(%s)' % str_dir].append(float("%.3f" % (self.last_probs[i])))

        return act_dict

    def save_neighborhood_to_dict(self, N, neigh_dict):
        """
        Salva all'interno del dizionario l'ultimo vicinato estratto
        :param N: Vicinato da salvare
        :param neigh_dict: Dizionario su cui salvare il vicinato
        :return: Dizionario a cui è stato aggiunto il nuovo vicinato
        """
        neigh_dict["Iteration"].append(self.iter)
        neigh_dict["AgentID"].append(self.id)
        neigh_dict["Neighbours"].append("\n%s" % N)
        return neigh_dict

    def manage_info(self, N, direction_result, probs, act_dict, neigh_dict):
        """
        Aggiorna le strutture dati, in particolare i dizionari, in modo da memorizzare le informazioni
        riguardanti l'iterazione corrente.
        :param N: Vicinato estratto
        :param direction_result: Azione eseguita nell'iterazione corrente
        :param probs: Distribuzione di probababilità delle azioni nell'iterazione corrente
        :param act_dict: Dizionario contenente le azioni eseguite nel corso delle varie iterazioni.
        :param neigh_dict: Dizionario contenente i vicinati estratti nel corso della simulazione.
        :return: Dizionari act_dict e neigh_dict aggiornati con le ultime informazioni.
        """
        self.last_action = direction_result
        self.last_probs = probs
        self.iter += 1
        act_dict = self.save_actions_to_dict(act_dict)
        neigh_dict = self.save_neighborhood_to_dict(N, neigh_dict)
        return act_dict, neigh_dict

    def manage_iteration(self, act_dict, neigh_dict):
        """
        Gestisce una generica iterazione.
        Durante l'iterazione:
        1) Sceglie la direzione da seguire
        2) Aggiorna le strutture dati.
        :param act_dict: Dizionario delle azioni svolte nella simulazione
        :param neigh_dict: Dizionario dei vicinati estratti durante la simulazione.
        :return: Direzione scelta, Dizionari act_dict e neigh_dict aggiornati.
        """
        dir, probs, N = self.decide_direction()
        act_dict, neigh_dict = self.manage_info(N, dir, probs, act_dict, neigh_dict)
        return dir, act_dict, neigh_dict

    def decide_direction(self):
        """
        Estrae il neighborhood e sceglie di conseguenza l'azione da effettuare basandosi sulla
        distribuzione di probabilità calcolata.
        :return: Azione scelta, distribuzione di probabilità delle varie azioni, vicinato estratto.
        """
        N = extract_neighborhood(self.binary_env, self.k, self.x, self.y)

        if self.movement == "distance":
            direction, distances, probs = compute_direction_distance(N)

        elif self.movement == "density":
            direction, probs = compute_direction_density(N)

        elif self.movement == "combine":
            direction, probs = combine(N)

        if self.stochastic:
            direction_result = sample_next_action(probs)

        else:
            direction_result = direction

        return direction_result, probs, N

    def move(self, env, direction):
        """
        Esegue l'azione in direzione direction e modifica l'ambiente env in modo opportuno.
        :param env: Ambiente da modificare
        :param direction: Direzione in cui muoversi.
        :return: None (env viene modificato come side-effect)
        """
        new_x, new_y = get_new_position(self.x, self.y, self.n_rows, self.n_cols, direction)
        env[self.x, self.y] = 0
        env[new_x, new_y] = self.id
        self.binary_env[self.x, self.y] = 0
        self.binary_env[new_x, new_y] = 1
        self.x = new_x
        self.y = new_y
