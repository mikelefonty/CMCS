"""
Questo file contiene il main per eseguire il simulatore Intelligent.
Per utilizzarlo:

python IntelligentMain.py [-h] [-v] [--fun {distance,density,combine}]
                          [-k {3,4,5,6,7}] [--strat {sequential,random}]
                          [-seed SEED] [-show] [--type {det,stoc}]
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
  --type {det,stoc}, -t {det,stoc}
                        Perform a deterministic or a stochastic simulation
"""


import sys

sys.path.append("../")

import argparse
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from Simulators.IntelligentSimulator import *
from Simulators.Simulator import *


def append_time_string(s):
    now = datetime.now()
    str_time = now.strftime("%d_%m_%Y_%H_%M_%S")
    return s + "_" + str_time, str_time


if __name__ == "__main__":

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

    parser.add_argument("path", type=str,
                        help="Path of the folder which will contain the results of the simulation")

    parser.add_argument("--type", "-t", choices=["det","stoc"],default="stoc",help="Perform a deterministic or a "
                                                                           "stochastic simulation")

    try:

        args = parser.parse_args()
        if args.verbose:
            print("Intelligent Simulator")
        env_path = args.env
        results_path = args.path
        if not os.path.exists(env_path):
            raise FileNotFoundError("The environment file {} does not exists".format(env_path))

        if not os.path.exists(results_path):
            if args.verbose:
                print("The folder {} does not exist".format(results_path))
            os.makedirs(results_path)
            if args.verbose:
                print("Folder {} created".format(results_path))

        if not args.seed or args.seed < 0:
            seed = None
        else:
            seed = args.seed

        if args.verbose:
            print("-Using the env stored in {}".format(env_path))
            print("-Updating the agents using the {} function".format(args.fun))
            print("-Using the neighborhood of size {}".format(args.k))
            print("-Simulating for {} iterations".format(args.n_iters))
            if args.type == "stoc":
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
            print("-The results will be saved into the {} folder".format(args.path))

        save_env_path_nn = "env_change_sim_nn.csv"
        save_actions_path_nn = "azioni_sim_nn.csv"
        save_measure_path_nn = "misure_cluster_sim_nn.csv"
        save_neigh_path_nn = "neighbours_sim_nn.csv"
        save_meta_path_nn = "metadata_sim_nn.csv"

        stochastic_simulation = True
        if args.type=="det":
            stochastic_simulation = False

        save_measure_plot_nn = "result_plot_nn.png"
        save_measure_plot_nn_log = "result_plot_nn_log.png"
        if not os.path.exists(results_path):
            os.makedirs(results_path)


        measures_nn = []

        sim_nn = IntelligentSim(env_path, args.k, strategy=args.strat, show_anim=args.show_anim,
                                movement=args.fun, stochastic_sim=stochastic_simulation, seed=seed,
                                save_env_path=results_path + "/" + save_env_path_nn,
                                save_meta_path=results_path + "/" + save_meta_path_nn,
                                save_measure_path=results_path + "/" + save_measure_path_nn,
                                save_actions_path=results_path + "/" + save_actions_path_nn,
                                save_neigh_path=results_path + "/" + save_neigh_path_nn
                                )

        sim_nn.update_world(args.n_iters)
        measures_nn = read_measure_file(results_path + "/" + save_measure_path_nn)
        # measures_nn.append(m)

        sim_type = ""
        if stochastic_simulation:
            sim_type = "Stochastic"
        else:
            sim_type = "Deterministic"

        plot_title = "Simulating the env: {}\n{} simulation, Function={}\n{} selection, k={}".format(
            args.env, sim_type, args.fun, args.strat, args.k
        )

        plot_measures(None, measures_nn, results_path + "/" + save_measure_plot_nn,False, plot_title)
        plot_measures(None, measures_nn, results_path + "/" + save_measure_plot_nn_log,True, plot_title)
    except FileNotFoundError as e:
        print(e.args)
