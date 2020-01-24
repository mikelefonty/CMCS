"""
Questa classe implementa la struttura di un generico simulatore, senza l'utilizzo di alcuna rete
neurale. Le performances di questo simulatore, dovranno poi essere confrontate con quelle di un
simulatore che utilizza al suo interno una NN.
"""

import sys

sys.path.append("../")
from Agents.Agent import *
import csv


def save_dict_to_file(d, fields, path="prova.csv"):
    """
    Salva un generico dizionario all'interno di un file, il cui percorso è indicato da path.
    :param d: Dizionario da salvare
    :param fields: Campi di cui è composto il dizionario
    :param path: Percorso del file su cui salvare il dizionario
    :return: None
    """
    df = DataFrame(d, columns=fields)

    df.to_csv(path, index=None, mode="w", header=True)


def create_dict(fields):
    """
    Crea un generico dizionario, avente come campi fields.
    :param fields: Lista che contiene i nomi dei campi di cui sarà composto il dizionario.
    :return: Dizionario con campi "fields"
    """
    d = {}
    for field in fields:
        d[field] = []
    return d


class Simulator:

    def save_env_to_file(self, iter, cluster_measure):
        """
        Salva l'ambiente della simulazione su file
        :param iter: Iterazione corrente
        :param cluster_measure: Misura del cluster ottenuta al termine dell'iterazione iter
        :return: None
        """
        with open(self.save_env_path, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames, delimiter=",")
            writer.writerow({"Iteration": iter, "Environment": "\n%s" % self.env})

        with open(self.save_measure_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.field_measure, quoting=csv.QUOTE_NONE, escapechar=" ", )
            writer.writerow({"Iteration": iter, "Measure": float("%.3f" % cluster_measure)})

    def save_metadata(self):
        """
        Salva i metadati della simulazione su file.
        Nello specifico, i metadati contengono i seguenti campi:
        1)Simulatore usato (Intelligent/Target)
        2)Strategia usata per selezionare gli agenti durante la simulazione (Random/Sequenziale)
        3)Ampiezza del vicinato da estrarre (k)
        4)Funzione da usare per calcolare la direzione (density,distance,combine)
        5)Numero di righe dell'ambiente
        6)Numero di colonne dell'ambiente
        7)Numero di agenti
        8)Seed eventualmente utilizzato
        9)Ambiente iniziale.
        :return: None
        """

        with open(self.save_meta_path, "w") as f:

            writer = csv.DictWriter(f, fieldnames=self.field_meta, delimiter=",")
            writer.writeheader()
            if self.stochastic_sim:
                stoc = "Stochastic"
            else:
                stoc = "Deterministic"

            writer.writerow({"sim_type": self.sim_type,
                             "stoc/det": stoc,
                             "strategy": self.strategy,
                             "start_env": "\n%s" % self.env,
                             "k": self.k,
                             "function": self.movement,
                             "n_agents": len(self.agents_list),
                             "env_row": self.n_rows,
                             "env_cols": self.n_cols,
                             'seed': self.seed})

    def create_env(self, env_file):
        """
        Legge l'ambiente presente in env_file ed inizializza le strutture dati necessarie per la simulazione.
        Crea in particolare l'insieme degli Agenti (Non intelligenti).
        :param env_file: Path del file in cui è salvato l'ambiente.
        :return: None
        """
        M = read_matrix_from_file(env_file)
        agents_pos = get_agents_in_env(M)

        self.env = np.zeros_like(M)
        for ag_id in range(len(agents_pos)):
            self.env[agents_pos[ag_id][0], agents_pos[ag_id][1]] = ag_id + 1
            self.agents_list.append(
                Agent(ag_id + 1, self.k, M, agents_pos[ag_id][0], agents_pos[ag_id][1], self.movement,
                      self.stochastic_sim, self.save_actions_path, self.save_neigh_path))

    def save_env_to_dict(self,iter):
        """
        Salva l'ambiente corrente all'interno del dizionario interno env_dict.
        :param iter: Numero dell'iterazione corrente
        :return: None
        """
        self.env_dict["Iteration"].append(iter)
        self.env_dict["Environment"].append("\n%s" % self.env)

    def save_measure_to_dict(self,iter, cluster_measure):
        """
        Salva la misura di cluster corrente all'interno del dizionario measure_dict.
        :param iter: Iterazione corrente
        :param cluster_measure: Misura di clustering corrente.
        :return: None
        """
        self.measure_dict["Iteration"].append(iter)
        self.measure_dict["Measure"].append(float("%.3f" % (cluster_measure)))

    def __init__(self, env_file, k, strategy="random", show_anim=False, movement="distance", stochastic_sim=False,
                 seed=None, save_env_path="./risultati_sim.csv",
                 save_actions_path="./azioni_sim.csv",
                 save_measure_path="./misure_sim.csv",
                 save_neigh_path="./neighbours_sim.csv",
                 save_meta_path="./metadata_sim.csv",
                 ):

        """
        Inizializza un generico simulatore.
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

        assert movement == "density" or movement == "distance" or movement == "combine", "Movement can be [density / distance/combine]"

        self.sim_type = "Target Simulator"
        self.stochastic_sim = stochastic_sim

        self.agents_list = []
        self.env = None

        self.movement = movement
        self.k = k

        if strategy == "sequential":
            self.strategy = "sequential"
        else:
            self.strategy = "random"

        self.show_anim = show_anim
        self.seed = seed

        self.save_env_path = save_env_path
        self.save_actions_path = save_actions_path
        self.save_measure_path = save_measure_path
        self.save_neigh_path = save_neigh_path
        self.save_meta_path = save_meta_path

        self.fieldnames = ['Iteration', 'Environment']

        self.field_measure = ['Iteration', 'Measure']
        self.field_neigh = ['Iteration', 'AgentID', "Neighbours"]
        self.field_actions = ['Iter', 'ID', 'Action', 'P(UP)', 'P(DOWN)', 'P(LEFT)',
                              'P(RIGHT)',
                              'P(UP_LEFT)',
                              'P(UP_RIGHT)', 'P(DOWN_LEFT)', 'P(DOWN_RIGHT)', 'P(NONE)']

        self.field_meta = ['sim_type', 'stoc/det', 'strategy', 'k', 'function', 'n_agents', 'env_row', 'env_cols',
                           'seed', 'start_env']

        self.act_dict = create_dict(self.field_actions)
        self.measure_dict = create_dict(self.field_measure)
        self.neigh_dict = create_dict(self.field_neigh)
        self.env_dict = create_dict(self.fieldnames)

        self.create_env(env_file)

        self.n_rows = self.env.shape[0]
        self.n_cols = self.env.shape[1]
        self.save_env_to_dict(0)
        self.save_measure_to_dict(0, compute_cluster_measure(self.agents_list, k=min(5, self.k)))
        self.save_metadata()

    def init_animations(self):
        """
        Inizializza le strutture dati utilizzate per mostrare a video l'animazione della simulazione.
        :return:
        """
        plt.ion()
        fig, ax = plt.subplots()

        y_l = []
        x_l = range(self.n_cols)
        for i in range(self.n_cols):
            y_l.append(0)
        plt.plot(x_l, y_l)

        y_l = []
        x_l = range(self.n_cols)
        for i in range(self.n_cols):
            y_l.append(-(self.n_rows - 1))

        plt.plot(x_l, y_l)

        y_l = range(-self.n_rows + 1, 1)
        x_l = []
        for i in range(self.n_rows):
            x_l.append(0)

        plt.plot(x_l, y_l)

        y_l = range(-self.n_rows + 1, 1)
        x_l = []
        for i in range(self.n_rows):
            x_l.append(self.n_cols - 1)

        plt.plot(x_l, y_l)

        plt.plot(x_l, y_l)
        plt.xticks(range(0, self.n_cols))
        plt.yticks(range(-self.n_rows, 1))
        plt.ylim([-self.n_rows, 1])
        plt.xlim([-1, self.n_cols])
        plt.grid()

        x = []
        y = []
        ids = []
        for agent in self.agents_list:
            x.append(-agent.x)
            y.append(agent.y)
            ids.append(agent.id)

        sc = ax.scatter(y, x)
        ann = []

        stoc_or_det_simulation = "Deterministic"
        if self.stochastic_sim:
            stoc_or_det_simulation = "Stochastic"

        for (i, curr_id) in enumerate(ids):
            ann.append(ax.annotate(curr_id, (y[i] + 0.2, x[i] - 0.1)))
        ax.set_title("%s\n%s Simulation with %s agents k = %s Function = %s" % (
            self.sim_type, stoc_or_det_simulation, len(self.agents_list), self.k, self.movement))

        plt.draw()
        return sc, ax, x, y, ids, ann

    def update_world(self, n_iters):
        """
        Esegue una simulazione di n_iters iterazioni.
        :param n_iters: Numero di iterazioni da eseguire.
        :return:
        """

        np.random.seed(self.seed)
        if self.show_anim:
            scatter, ax, x, y, ids, ann = self.init_animations()
            plt.pause(0.3)

        for i in range(n_iters):

            print("Iteration %d/%d" % (i + 1, n_iters))
            if self.strategy == "random":
                np.random.shuffle(self.agents_list)

            if not self.show_anim:
                for agent in self.agents_list:
                    "L'agente sceglie la direzione"
                    direction, self.act_dict, self.neigh_dict = agent.manage_iteration(self.act_dict, self.neigh_dict)
                    "Sposto l'agente e modifico l'ambiente"
                    agent.move(self.env, direction)

            else:
                for (j, agent) in enumerate(self.agents_list):
                    "L'agente sceglie la direzione"
                    direction, self.act_dict, self.neigh_dict = agent.manage_iteration(self.act_dict, self.neigh_dict)
                    "Sposto l'agente e modifico l'ambiente"
                    agent.move(self.env, direction)

                    "Mostro a schermo l'animazione, aggiornando in modo opportuno lo scatter plot"
                    x[j] = -agent.x
                    y[j] = agent.y
                    ids[j] = agent.id

                for annotation in ann:
                    annotation.remove()
                ann.clear()
                for (j, curr_id) in enumerate(ids):
                    ann.append(ax.annotate(curr_id, (y[j] + 0.2, x[j] - 0.1)))
                scatter.set_offsets(np.c_[y, x])

                stoc_or_det_simulation = "Deterministic"
                if self.stochastic_sim:
                    stoc_or_det_simulation = "Stochastic"

                ax.set_title(
                    "%s\n%s Simulation with %s agents k = %s Function = %s\nIteration %s/%s  Cluster Measure %.3f" %
                    (
                        self.sim_type, stoc_or_det_simulation, len(self.agents_list), self.k, self.movement, i + 1,
                        n_iters,
                        float("%.3f" % (compute_cluster_measure(self.agents_list, k=5)))))#k=min(5, self.k))))))
                plt.pause(0.3)

            "Aggiorno i dizionari"
            self.save_env_to_dict(i+1)
            self.save_measure_to_dict(i+1,compute_cluster_measure(self.agents_list, k=5))#k=min(5, self.k)

        "Al termine di tutte le iterazioni, salvo su file i contenuti dei vari dizionari"
        save_dict_to_file(self.neigh_dict,self.field_neigh,self.save_neigh_path)
        save_dict_to_file(self.act_dict, self.field_actions, self.save_actions_path)
        save_dict_to_file(self.env_dict,self.fieldnames,self.save_env_path)
        save_dict_to_file(self.measure_dict,self.field_measure,self.save_measure_path)

        if self.show_anim:
            plt.waitforbuttonpress()

