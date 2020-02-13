import sys
sys.path.append("../")
import numpy as np
from Util.data_structures import Direction

print('All Directions:')
for d in Direction:
    print(f'{str(d)} --> {d.value}')
print()
print('Max number of directions: ',Direction.get_n_directions())

print(50*'-')
M = np.reshape(np.linspace(1,25,num=25,dtype=int),(5,5))
print('Matrice considerata\n',M)
print(f'Centro della matrice: (2,2) = {M[2,2]}')

print(f'UP vector: {Direction.UP.direction2pair()}: Get {M[2+Direction.UP.direction2pair()[0],2+Direction.UP.direction2pair()[1]]}')
print(f'DOWN vector: {Direction.DOWN.direction2pair()}: Get {M[2+Direction.DOWN.direction2pair()[0],2+Direction.DOWN.direction2pair()[1]]}')

print(f'LEFT vector: {Direction.LEFT.direction2pair()}: Get {M[2+Direction.LEFT.direction2pair()[0],2+Direction.LEFT.direction2pair()[1]]}')

print(f'RIGHT vector: {Direction.RIGHT.direction2pair()}: Get {M[2+Direction.RIGHT.direction2pair()[0],2+Direction.RIGHT.direction2pair()[1]]}')

print(f'UP_LEFT vector: {Direction.UP_LEFT.direction2pair()}: Get {M[2+Direction.UP_LEFT.direction2pair()[0],2+Direction.UP_LEFT.direction2pair()[1]]}')

print(f'UP_RIGHT vector: {Direction.UP_RIGHT.direction2pair()}: Get {M[2+Direction.UP_RIGHT.direction2pair()[0],2+Direction.UP_RIGHT.direction2pair()[1]]}')
print(f'DOWN_LEFT vector: {Direction.DOWN_LEFT.direction2pair()}: Get {M[2+Direction.DOWN_LEFT.direction2pair()[0],2+Direction.DOWN_LEFT.direction2pair()[1]]}')
print(f'DOWN_RIGHT vector: {Direction.DOWN_RIGHT.direction2pair()}: Get {M[2+Direction.DOWN_RIGHT.direction2pair()[0],2+Direction.DOWN_RIGHT.direction2pair()[1]]}')

print(f'NONE vector: {Direction.NONE.direction2pair()}: Get {M[2+Direction.NONE.direction2pair()[0],2+Direction.NONE.direction2pair()[1]]}')