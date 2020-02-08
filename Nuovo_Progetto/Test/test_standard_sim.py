import sys
sys.path.append('../')
from Simulator.standard_simulator import Simulator
from Simulator.block_simulator import BlockSimulator
from Util.environment_IO import create_environment
import tensorflow as tf

create_environment(40,40,80,'../EnvSet/prova_env.txt')
#with tf.device('CPU:0'):
sim = BlockSimulator('../EnvSet/prova_env.txt',use_nn=False,
show_anim=True,seed=42,use_random_selection=True,neigh_size=7,use_stochastic_sim=True, log_file='risultati_sim',num_blocks=10)
sim.simulate(100,verbose=0)