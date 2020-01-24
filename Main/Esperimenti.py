"""
Questo file contiene il main per effettuare gli esperimenti atti a confrontare
i risultati dell'esecuzione dei simulatori Target e Intelligent.

Per lanciare l'applicazione:

 Esperimenti.py [-h] [-v] [--fun {distance,density,combine}]
                      [-k {3,4,5,6,7}] [--strat {sequential,random}]
                      [-seed SEED] [-show] [-r RUN] [--deterministic]
                      env n_iters path

positional arguments:
  env                   Path to the environment file
  n_iters               Number of iterations
  path                  Path of the folder which will contain the results of
                        the simulation

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show detailed informations
  --fun {distance,density,combine}, -f {distance,density,combine}
                        Function used to choose the agent movement (default =
                        density)
  -k {3,4,5,6,7}        Neighborhood's size (default = 7)
  --strat {sequential,random}, -s {sequential,random}
                        Specify how the agents are selected during simulation
                        (default = random)
  -seed SEED            Seed used for random numbers generator (default = 42)
  -show, --show_anim    Show the animation of the current simulation
  -r RUN, --run RUN     Number of runs for the experiment (default=1)
  --deterministic, -d   Perform a deterministic simulation instead of a
                        stochastic one


I plot risultanti sono ottenuti eseguendo i simulatori
per un numero di volte specificato dal parametro run.

Ad ogni run il valore del seed per il random number generator viene incrementato di 2 per ottenere valori
random diversi dall'esperimento precedente.

I plot mostrati sono i grafici medi dei risultati ottenuti nelle varie run.
I plot nella cartella log_plot sono grafici in scala logaritmica per entrambi gli assi cartesiani.

Per ogni run si producono i seguenti file:
1)Azioni degli agenti con relative probabilità
2)Cambiamento dell'ambiente nel corso delle iterazioni
3)Misure di clusters
4) Metadati del simulatore con il setting usato per l'esperimento
5)Vicini estratti da ogni agente nel corso della simulazione
6)Plot, in scala sia lineare che logaritmica, che mostra come varia la misura di cluster al variare delle iterazioni.
"""

import sys
sys.path.append("../")
import subprocess
from Utils.Util import *
import os
import argparse


def get_simulators_args(args,i,seed):
    """
    Crea gli argomenti da utilizzare per lanciare il main dei simulatori target e intelligent.
    Lancia quindi i main dei due simulatori presi in esame.

    :param args: Argomenti ricevuti da riga di comando
    :param i: Numero dell'iterazione
    :param seed: Seme da usare per RNG
    :return:
    """
    env_path = args.env
    results_path = args.path
    sim_type_value = "det" if args.deterministic else "stoc"
    strat_value = args.strat
    k_value = str(args.k)
    if not seed:
        seed_value = -1
    else:
        seed_value = seed

    if args.verbose and args.show_anim:
        return (["python", "./IntelligentMain.py", str(env_path),
                        str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
                        "-v", "-seed", str(seed_value), "-t", sim_type_value, "--strat",
                        strat_value, "-k", k_value, "-f", args.fun, "-show"],

        ["python", "./TargetMain.py", str(env_path),
         str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
         "-v", "-seed", str(seed_value), "-t", sim_type_value, "--strat",
         strat_value, "-k", k_value, "-f", args.fun, "-show"])

    elif args.verbose and not args.show_anim:
        return (["python", "./IntelligentMain.py", str(env_path),
          str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
          "-v", "-seed", str(seed_value), "-t", sim_type_value, "--strat",
          strat_value, "-k", k_value, "-f", args.fun],

         ["python", "./TargetMain.py", str(env_path),
          str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
          "-v", "-seed", str(seed_value), "-t", sim_type_value, "--strat",
          strat_value, "-k", k_value, "-f", args.fun])

    elif not args.verbose and args.show_anim:
        return (["python", "./IntelligentMain.py", str(env_path),
          str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
          "-seed", str(seed_value), "-t", sim_type_value, "--strat",
          strat_value, "-k", k_value, "-f", args.fun, "-show"],

         ["python", "./TargetMain.py", str(env_path),
          str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
          "-seed", str(seed_value), "-t", sim_type_value, "--strat",
          strat_value, "-k", k_value, "-f", args.fun, "-show"])

    else:
        return (["python", "./IntelligentMain.py", str(env_path),
                        str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
                        "-seed", str(seed_value), "-t", sim_type_value, "--strat",
                        strat_value, "-k", k_value, "-f", args.fun],

        ["python", "./TargetMain.py", str(env_path),
         str(args.n_iters), "{}/run_{}".format(results_path, i + 1),
         "-seed", str(seed_value), "-t", sim_type_value, "--strat",
         strat_value, "-k", k_value, "-f", args.fun])


if __name__ == "__main__":
    results_path = "../Proviamo"
    runs = 2
    seed = 42
    env = "../Environments/env_20x20_100agents.txt"
    sim_type = "Deterministic"
    fun = "density"
    k = 7
    strat = "random"
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed informations")
    parser.add_argument("--fun", "-f", choices=["distance", "density", "combine"], type=str,
                        help="Function used to choose the agent movement (default = density)"
                        , default="density")
    parser.add_argument("env", type=str, help="Path to the environment file ")
    parser.add_argument("-k", type=int, choices=[3, 4, 5, 6, 7], help="Neighborhood's size (default = 7)", default=7)
    parser.add_argument("n_iters", type=int, help="Number of iterations")
    parser.add_argument("--strat", "-s", type=str, choices=["sequential", "random"], default="random",
                        help="Specify how the agents are selected during simulation (default = random)")
    parser.add_argument("-seed", type=int, help="Seed used for random numbers generator (default = 42)", default=None)
    parser.add_argument("-show", "--show_anim", action="store_true",
                        help="Show the animation of the current simulation")
    parser.add_argument("-r", "--run", type=int, default=1, help="Number of runs for the experiment (default=1)")
    parser.add_argument("path", type=str,
                        help="Path of the folder which will contain the results of the simulation")

    parser.add_argument("--deterministic","-d",action="store_true",help="Perform a deterministic "
                                                                        "simulation instead of a stochastic one")

    try:

        args = parser.parse_args()

        env_path = args.env
        results_path = args.path
        runs = args.run
        if not os.path.exists(env_path):
            raise FileNotFoundError("The environment file {} does not exists".format(env_path))

        if not os.path.exists(results_path):
            if args.verbose:
                print("The folder {} does not exist".format(results_path))
            os.makedirs(results_path)
            if args.verbose:
                print("Folder {} created".format(results_path))

        if args.seed and args.seed >= 0:
            seed = args.seed
        else:
            seed = None

        if args.verbose:
            print("-Using the env stored in {}".format(env_path))
            print("-Updating the agents using the {} function".format(args.fun))
            print("-Using the neighborhood of size {}".format(args.k))
            print("-Simulating for {} iterations".format(args.n_iters))
            if not args.deterministic:
                print("-Performing a stochastic simulation")
            else:
                print("-Performing a deterministic simulation")

            print("-Agents are selected in a {} way".format(args.strat))
            if seed:
                print("-Using {} as seed".format(seed))
            else:
                print("-Not using a seed")

            if args.show_anim:
                print("-Showing the simulation")
            else:
                print("-Not showing the simulation")
            print("-Doing {} runs".format(args.run))
            print("-The results will be saved into the {} folder".format(args.path))


        for i in range(runs):

            param_int,param_target = get_simulators_args(args,i,seed)

            subprocess.run(param_int)
            subprocess.run(param_target)

            if seed:
                seed += 2

        plots_path = results_path+"/plots"
        log_plots_path = results_path+"/log_plots"

        if not os.path.exists(plots_path):
            os.makedirs(plots_path)
        if not os.path.exists(log_plots_path):
            os.makedirs(log_plots_path)

        measures_nn = []
        measures_target = []

        for i in range(runs):
            mis_file_nn = "{}/run_{}/misure_cluster_sim_nn.csv".format(results_path,i+1)
            measures_nn.append(read_measure_file(mis_file_nn))

            mis_file_target = "{}/run_{}/misure_cluster_sim_target.csv".format(results_path, i + 1)
            measures_target.append(read_measure_file(mis_file_target))

        measures_nn_mean = np.mean(measures_nn,axis=0)
        measures_target_mean = np.mean(measures_target,axis=0)

        sim_type = "Deterministic" if args.deterministic else "Stochastic"
        plot_title = "Simulating the env: {}\n{} simulation, Function={}\n{} selection, k={}".format(
                    env_path,sim_type , args.fun, args.strat, args.k)

        plot_measures(None,measures_nn_mean,"{}/plot_nn_mean_{}_runs.png".format(plots_path,runs),False,plot_title)
        plot_measures(measures_target_mean,None,"{}/plot_target_mean_{}_runs.png".format(plots_path,runs),False,plot_title)
        plot_measures(measures_target_mean,measures_nn_mean,"{}/plot_all_{}_runs.png".format(plots_path,runs),False,plot_title)

        plot_measures(None,measures_nn_mean,"{}/plot_nn_mean_{}_runs_log.png".format(log_plots_path,runs),True,plot_title)
        plot_measures(measures_target_mean,None,"{}/plot_target_mean_{}_runs_log.png".format(log_plots_path,runs),True,plot_title)
        plot_measures(measures_target_mean,measures_nn_mean,"{}/plot_all_{}_runs_log.png".format(log_plots_path,runs),True,plot_title)

    except FileNotFoundError as e:
        print(e.args)
