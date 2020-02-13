import sys
sys.path.append('../')
from Simulator.standard_simulator import Simulator
from Simulator.block_simulator import BlockSimulator
from Util.environment_IO import create_environment
from CONSTANTS.constant_reader import Constant_Reader
from Util.simulation_utils import replicate_simulation_from_file
import pandas as pd 
from matplotlib import pyplot as plt
import argparse
import os
from datetime import datetime
from Util.simulation_utils import replicate_simulation_from_file

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("path", type=str,
                        help="Path of the file which will contain the results of the simulation (All the results will be saved into the Results Folder)")
    
    parser.add_argument("res_name", type=str,
                        help="Name of the file which will contain the results of the simulation (All the results will be saved into the Results Folder)")

  
    try:

        constants = Constant_Reader()
        env_dir = constants.get_env_directory()
        ris_dir = constants.get_result_directory()

        args = parser.parse_args()
 
        results_path = ris_dir+"/"+args.path
        result_name = args.res_name
        print(results_path+"/"+result_name)
       
        replicate_simulation_from_file(results_path+"/"+result_name)
    
    except Exception as e:
        print(e)
