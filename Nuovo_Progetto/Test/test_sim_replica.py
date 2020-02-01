import sys
sys.path.append('../')
from Simulator.standard_simulator import Simulator
from Util.environment_IO import create_environment
from Util.simulation_utils import replicate_simulation_from_file


path = 'risultati_sim'


create_environment(14,14,5,'./prova_env.txt')

sim = Simulator('prova_env.txt',show_anim=True,seed=None,use_random_selection=True,neigh_size=7,log_file=path)
sim.simulate(30) 



replicate_simulation_from_file(path)