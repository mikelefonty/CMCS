import sys
sys.path.append('../')
from Util.data_structures import Direction
from Util.matrix_functions import binarize_matrix
import math
import numpy as np
from Agent.agent import Agent
from Util.print_utils import beautify_print_direction

env = binarize_matrix(np.reshape(np.linspace(1, 25, 25), (5, 5)))

agent = Agent(30, 3, 3)
env[3, 3] = 30

print('Environment:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.UP, env)
env[agent.x, agent.y] = 30
print('Move UP:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.UP, env)
env[agent.x, agent.y] = 30
print('Move UP:\n', env)


env[agent.x, agent.y] = 1
agent.move(Direction.UP_LEFT, env)
env[agent.x, agent.y] = 30
print('Move UP_LEFT:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.DOWN, env)
env[agent.x, agent.y] = 30
print('Move DOWN:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.UP_RIGHT, env)
env[agent.x, agent.y] = 30
print('Move UP_RIGHT:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.DOWN_RIGHT, env)
env[agent.x, agent.y] = 30
print('Move DOWN_RIGHT:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.RIGHT, env)
env[agent.x, agent.y] = 30
print('Move RIGHT:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.DOWN_LEFT, env)
env[agent.x, agent.y] = 30
print('Move DOWN_LEFT:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.UP_RIGHT, env)
env[agent.x, agent.y] = 30
print('Move UP_RIGHT:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.LEFT, env)
env[agent.x, agent.y] = 30
print('Move LEFT:\n', env)

env[agent.x, agent.y] = 1
agent.move(Direction.NONE, env)
env[agent.x, agent.y] = 30
print('Move NONE:\n', env)

# --------------------------------------------------------------------------------------------------------------------
print(100*"-")
print()

size = 81
m = int(math.sqrt(size))
k = 5
seed = 42

np.random.seed(seed)

M = np.reshape(np.linspace(1, size, size), (m, m))
random_indexes = np.random.uniform(low=0, high=1, size=(M.shape)) <= 0.3
M = np.multiply(random_indexes, M)
print(M)

agent= Agent(50,5,4)
direction= agent.next_direction(M,k,True)
beautify_print_direction(direction)

