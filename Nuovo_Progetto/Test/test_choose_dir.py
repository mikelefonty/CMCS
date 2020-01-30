import math
import numpy as np
from Decide_Direction.decide_direction import choose_direction
import sys
sys.path.append('../')


size = 81
m = int(math.sqrt(size))
k = 5
M = np.reshape(np.linspace(1, size, size), (m, m))
random_indexes = np.random.uniform(low=0, high=1, size=(M.shape)) <= 0.7
M = np.multiply(random_indexes, M)

choose_direction(M, m//2, m//2, k, True)
