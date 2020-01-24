"""
Questo file serve per generare in modo casuale un ambiente di dimensioni (N x M)
con K agenti al suo interno.


Per avviarlo lanciare:

    python CreateNewEnv.py [-h] [-v] path rows cols n_agents

positional arguments:
  path           Path of the folder in which to save the new environment
  rows           Number of rows of the new environment
  cols           Number of columns of the environment
  n_agents       Number of agents to be created

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show detailed informations

"""


import sys

sys.path.append("../")

from Utils.Util import *
import argparse
import os


def create_env_filename(name, ext, verbose=False):
    """
    Crea un filename del tipo name(i)ext, se nella directory vi sono
    (i-1) file con nome name
    :param name: Nome del file
    :param ext: Estensione, già con punto (esempio: .txt)
    :param verbose: Mostra informazioni di debug
    :return: filename nel formato name(i)ext oppure nameext, se il file non è già esistente.
    """
    stop = False
    counter = 1
    if not os.path.exists(name + ext):
        return name + ext

    else:
        if verbose:
            print(name + ext+" already exists...")
        while not stop:
            if os.path.exists(name + "(" + str(counter) + ")" + ext):
                if verbose:
                    print(name + "(" + str(counter) + ")" + ext+" already exists...")
                counter += 1
            else:
                stop = True
    return name + "(" + str(counter) + ")" + ext


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed informations")
    parser.add_argument("path", type=str, help="Path of the folder in which to save the new environment")
    parser.add_argument("rows", type=int, help="Number of rows of the new environment")
    parser.add_argument("cols", type=int, help="Number of columns of the environment")
    parser.add_argument("n_agents", type=int, help="Number of agents to be created")

    args = parser.parse_args()

    if args.verbose:
        print("Executing {}".format(__file__))
        print("The environment will be saved into the {} folder".format(args.path))
        print("The environment will be a {} x {} matrix with {} agents inside".format(
            args.rows, args.cols, args.n_agents))

        print("\nCreating the environment")

    if not os.path.exists(args.path):
        if args.verbose:
            print("The folder {} does not exist...".format(args.path))
            print("Creating the folder {}".format((args.path)))
        os.makedirs(args.path)

        if args.verbose:
            print("Folder {} created".format(args.path))

    env_name = args.path + "/env_{}x{}_{}agents".format(args.rows, args.cols, args.n_agents)

    env_name = create_env_filename(env_name, ".txt",args.verbose)
    generate_new_environment(args.rows, args.cols, args.n_agents, env_name)
    if args.verbose:
        print("{} created successfully".format(env_name))
