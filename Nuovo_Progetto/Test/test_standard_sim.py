import sys
sys.path.append('../')
from Simulator.standard_simulator import Simulator
from Util.environment_IO import create_environment

create_environment(70,70,100,'./prova_env.txt')
sim = Simulator('prova_env.txt',show_anim=True,seed=None,use_random_selection=True,neigh_size=7,log_file='risultati_sim')
sim.simulate(20)