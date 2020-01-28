import sys
sys.path.append('../')
from Simulator_Output.simulator_debug import Simulator_Debug
from CONSTANTS.constant_reader import Constant_Reader


constants = Constant_Reader("../CONSTANTS/costanti.json")

title = 'Prova di debug:\nIterazione numero '
n_iter = 0
sim = Simulator_Debug(constants,12,8,title=title+str(n_iter))
sim.update({'1':(0,0),'22':(2,1),'33':(4,1)},title+str(n_iter))
n_iter+=1
sim.update({'22':(2,2)},title+str(n_iter))
n_iter+=1
sim.update({'22':(2,3)},title+str(n_iter))
n_iter+=1
sim.update({'22':(2,4)},title+str(n_iter))
n_iter+=1
sim.update({'22':(2,5)},title+str(n_iter))
n_iter+=1
sim.update({'44':(5,3),'22':(2,6)},title+str(n_iter))
n_iter+=1
sim.update({'44':(6,4),'1':(10,7)},title+str(n_iter))
n_iter+=1
sim.update({'1':(10,7)},title+str(n_iter))

