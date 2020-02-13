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



def append_time_string(s):
    now = datetime.now()
    str_time =  now.strftime("%d_%m_%Y_%H_%M_%S")
    return s + "_" + str_time

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    
    parser.add_argument("env", type=str, help="Name of the environment file (The file must be in the EnvironmentsSet folder) ")
    parser.add_argument("-k", type=int, choices=range(2,12), help="Neighborhood's size (default = 7)", default=7)
    parser.add_argument("n_iters", type=int, help="Number of iterations")
    
    parser.add_argument("--rand_strat", action="store_true",
                        help="Use a random selection of the agents during the simulation")
    parser.add_argument("--stoc",action="store_true" ,help="Perform a stochastic simulation (otherwise it will be done a deterministic simulation)")
                                                                           

    parser.add_argument("-v", "--verbose", type=int, choices=[0,1,2],default=0, help="Show detailed informations")
    parser.add_argument("-seed", type=int, help="Seed used for random numbers generator (default = 42)", default=42)
    parser.add_argument("-show", "--show_anim", action="store_true",
                        help="Show the animation of the current simulation")
    parser.add_argument("--path", type=str,
                        help="Path of the file which will contain the results of the simulation (All the results will be saved into the Results Folder)")
    
    parser.add_argument("--res_name", type=str,
                        help="Name of the file which will contain the results of the simulation (All the results will be saved into the Results Folder)")

    parser.add_argument("--replay", action="store_true",
                        help="Execute (another time) the animation of the all simulation")
    try:

        constants = Constant_Reader()
        env_dir = constants.get_env_directory()
        ris_dir = constants.get_result_directory()

        args = parser.parse_args()

        env_path = args.env

        if args.path:
            results_path = ris_dir+"/"+args.path
        else:
            results_path = ris_dir+"/"

        if not args.res_name:
            result_name = append_time_string('result')
        else:
            result_name = args.res_name
        
        if not os.path.exists(env_dir+"/"+env_path):
            raise FileNotFoundError("The environment file {} does not exist".format(env_path))
        
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

        if args.verbose>0:
            print("-Using the env stored in {}".format(env_path))
            print("-Using the neighborhood of size {}".format(args.k))
            print("-Simulating for {} iterations".format(args.n_iters))
            if args.stoc:
                print("-Performing a stochastic simulation")
            else:
                print("-Performing a deterministic simulation")

            if args.rand_strat:
                print("-Agents are selected in a randomic way")
            else:
                print("-Agents are selected in a sequential way")


            if seed:
                print("-Using {} as seed".format(seed))
            else:
                print("-Not using a seed")

            if args.show_anim:
                print("-Showing the simulation")
            else:
                print("-Not showing the simulation")

            print("-The results will be saved into the {} folder".format(results_path))


        result_name_std = result_name+'_std'
        result_name_smart = result_name+'_smart'
        
        standard_sim = Simulator(env_dir+"/"+env_path,use_nn=False,
        show_anim=args.show_anim,seed=seed,use_random_selection=args.rand_strat,neigh_size=args.k,
        use_stochastic_sim=args.stoc, log_path=results_path, log_file=result_name_std)

        standard_sim.simulate(args.n_iters,verbose=args.verbose)

        if args.replay:
            replicate_simulation_from_file(results_path+"/"+result_name_std)
        
        
        smart_sim = Simulator(env_dir+"/"+env_path,use_nn=True,
        show_anim=args.show_anim,seed=seed,use_random_selection=args.strat,neigh_size=args.k,
        use_stochastic_sim=args.stoc, log_path=results_path, log_file=result_name_smart)


        smart_sim.simulate(args.n_iters,verbose=args.verbose)

        if args.replay:
            replicate_simulation_from_file(results_path+"/"+result_name_smart)

        df_std = pd.read_json(results_path+"/"+result_name_std+"_measures.json")
        df_smart = pd.read_json(results_path+"/"+result_name_smart+"_measures.json")
        
        plt.figure()

        df_meta = pd.read_json(results_path+"/"+result_name_std+"_meta.json")
        
        title_template = 'Confronto Simulatore Standard vs Smart\n Ambiente : {} {}x{}\nNeigh_Size = {} Selezione agenti: {}\n Simulazione {}'.format(
            df_meta.iloc[0]['Nome_Ambiente'],df_meta.iloc[0]['Numero_Righe'],
            df_meta.iloc[0]['Numero_Colonne'],
            df_meta.iloc[0]['Raggio_Vicinato'],df_meta.iloc[0]['Scelta_Agenti'],df_meta.iloc[0]['Strategia_Simulazione']
        )


        plt.title(title_template)
        
        
        plt.plot(df_std['Iterazione'],df_std['Misura'],label='Simulatore Standard')
        plt.plot(df_smart['Iterazione'],df_smart['Misura'],label='Simulatore Smart')
       

        plt.legend(loc='best')
        plt.xlabel('Numero di Iterazioni')
        plt.ylabel('Numero di Clusters')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(results_path+"/"+result_name+"_confronto_plot.png",bbox='tight')
        
        
    
    except Exception as e:
        print(e)
