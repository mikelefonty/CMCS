import sys
sys.path.append('../')
from Simulator.standard_simulator import Simulator
from Simulator.block_simulator import BlockSimulator
from Util.environment_IO import create_environment
import tensorflow as tf

#create_environment(30,30,40,'./prova_env.txt')
#with tf.device('CPU:0'):
sim = Simulator('prova_env.txt',use_nn=True,
show_anim=False,seed=42,use_random_selection=True,neigh_size=7,use_stochastic_sim=True, log_file='risultati_sim')
sim.simulate(100,verbose=0)