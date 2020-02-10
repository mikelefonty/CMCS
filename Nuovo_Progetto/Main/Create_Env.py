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

from Util.environment_IO import create_environment
import argparse
import os
from CONSTANTS.constant_reader import Constant_Reader


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed informations")
    parser.add_argument("path", type=str, help="Path of the folder in which to save the new environment")
    parser.add_argument("name",type=str,help="Name of the file of the environment")
    parser.add_argument("rows", type=int, help="Number of rows of the new environment")
    parser.add_argument("cols", type=int, help="Number of columns of the environment")
    parser.add_argument("n_agents", type=int, help="Number of agents to be created")

    args = parser.parse_args()

    constants = Constant_Reader()
    env_path = constants.get_env_directory() + "/"+args.path
    if args.verbose:
        print("Executing {}".format(__file__))
        print("The environment will be saved into the {} folder".format(env_path))
       
        print("\nCreating the environment")

    if not os.path.exists(env_path):
        if args.verbose:
            print("The folder {} does not exist...".format(env_path))
            print("Creating the folder {}".format((env_path)))
        os.makedirs(env_path)

        if args.verbose:
            print("Folder {} created".format(env_path))

    create_environment(args.rows,args.cols,args.n_agents,f'{env_path}/{args.name}.txt')
    
    print("{} created successfully".format(args.name))
