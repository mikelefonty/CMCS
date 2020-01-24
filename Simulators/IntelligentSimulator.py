"""
Questa classe implementa un simulatore intelligente. Estende il generico Simulator, effettuando la
simulazione mediante l'utilizzo di Agenti Intelligenti.
"""

import sys
sys.path.append("../")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from Simulators.Simulator import *
from Agents.Intelligent_Agents import *
from keras.models import load_model


class IntelligentSim(Simulator):

    def create_env(self, env_file):
        """
        Crea ed inizializza le strutture dati necessarie per la simulazione.
        In particolare crea l'insieme degli agenti intelligenti.
        L'ambiente iniziale viene caricato dal file env_file
        :param env_file: Path dell'ambiente iniziale da caricare.
        :return:
        """

        M = read_matrix_from_file(env_file)
        agents_pos = get_agents_in_env(M)

        "Carico il modello della rete neurale"
        nn_path = "../FinalModels/model_k_7_final_" + self.movement + ".h5"
        nn = load_model(nn_path)

        self.env = np.zeros_like(M)

        "Creo gli agenti intelligenti"
        for ag_id in range(len(agents_pos)):
            self.env[agents_pos[ag_id][0], agents_pos[ag_id][1]] = ag_id + 1
            self.agents_list.append(
                Intelligent_Agent(nn,ag_id + 1, self.k, M, agents_pos[ag_id][0], agents_pos[ag_id][1], self.movement,
                                  self.stochastic_sim,self.save_actions_path,self.save_neigh_path))

    def __init__(self, env_file, k, strategy="random", show_anim=False, movement="distance", stochastic_sim=False,seed=None,
                 save_env_path="./risultati_sim.csv",
                 save_actions_path="./azioni_sim.csv",
                 save_measure_path="./misure_sim.csv",
                 save_neigh_path="./neighbours_sim.csv",
                 save_meta_path="./metadata_sim.csv"
                 ):
        """
        Crea un simulatore intelligente, utilizzando i parametri passati all'interno del costruttore.
        :param env_file: Path del file in cui è contenuto l'ambiente da simulare.
        :param k: Ampiezza del vicinato da estrarre.
        :param strategy: Strategia con cui selezionare gli agenti nel corso di una iterazione. (Random/Sequenziale)
        :param show_anim: Se True, viene mostrata sullo schermo un'animazione della simulazione
        :param movement: Funzione da usare per scegliere la direzione (density,distance,combine)
        :param stochastic_sim: Se True, viene effettuata una simulazione stocastica.
        :param seed: Seme da usare per inizializzare il RNG.
        :param save_env_path: Path del file su cui salvare il contenuto dell'ambiente
        :param save_actions_path: Path del file sui cui salvare le azioni
        :param save_measure_path: Path del file su cui salvare le misure di clustering
        :param save_neigh_path: Path del file sui cui salvare i vicinati estratti.
        :param save_meta_path: Path del file su cui salvare i meta-dati del simulatore.
        """
        super(IntelligentSim, self).__init__(env_file, k, strategy, show_anim, movement,stochastic_sim,seed,
                                             save_env_path,save_actions_path,save_measure_path,
                                             save_neigh_path,save_meta_path)

        self.sim_type = "Intelligent Simulator"
        self.save_metadata()
