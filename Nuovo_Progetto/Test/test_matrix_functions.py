import sys
sys.path.append("../")
import numpy as np
from Util.matrix_functions import extract_neighborhood,create_binary_matrix,binarize_matrix,extract_sub_matrix

M = np.reshape(range(49),(7,7))
print(f"Matrix M =\n{M}")

print(f'Vicinato 3x3 di (3,3) estratto\n {extract_neighborhood(M,3,3,3)}')
print(f'Vicinato 3x3 di (0,3) estratto\n {extract_neighborhood(M,3,0,3)}')
print(f'Vicinato 3x3 di (0,0) estratto\n {extract_neighborhood(M,3,0,0)}')
print(f'Vicinato 3x3 di (0,6) estratto\n {extract_neighborhood(M,3,0,6)}')

print(50*'-')
print()

N = create_binary_matrix(5)
print(f'Matrice binaria generata con prob = 0.5:\n{N}')
N = create_binary_matrix(5,0.9)
print(f'Matrice binaria generata con prob = 0.9:\n{N}')
N = create_binary_matrix(5,0.1)
print(f'Matrice binaria generata con prob = 0.1:\n{N}')
N = create_binary_matrix(5,1)
print(f'Matrice binaria generata con prob = 1:\n{N}')
N = create_binary_matrix(5,0)
print(f'Matrice binaria generata con prob = 0:\n{N}')
print(50*'-')
print()

np.random.seed(42)
M = np.random.uniform(low=0,high=1,size=(5,5))
print(f'Random Matrix:\n{M}')
print(f'Matrice Binaria con Threshold = 0.5:\n{binarize_matrix(M)}')
print(f'Matrice Binaria con Threshold = 0.9:\n{binarize_matrix(M,thresh=0.9)}')
print(f'Matrice Binaria con Threshold = 0.3:\n{binarize_matrix(M,thresh=0.3)}')
print(50*'-')
print()

M = np.reshape(np.linspace(1,25,num=25,dtype=int),(5,5))
print('Matrice considerata\n',M)
print(f'Sottomatrice 3x3 di M(2,2) = 13\n{extract_sub_matrix(M,3,3,2,2)}')
print(f'Sottomatrice 3x3 di M(1,2) = 8\n{extract_sub_matrix(M,3,3,1,2)}')
print(f'Sottomatrice 3x3 di M(0,2) = 3\n{extract_sub_matrix(M,3,3,0,2)}')
try:
    print(f'Sottomatrice 3x3 di M(0,12) = ??\n{extract_sub_matrix(M,3,3,0,12)}')
except:
    print("Sottomatrice 3x3 di M(0,12) = ??\nAssertion Error: OK!")

try:
    print(f'Sottomatrice 3x3 di M(12,0) = ??\n{extract_sub_matrix(M,3,3,12,0)}')
except:
    print("Sottomatrice 3x3 di M(12,0) = ??\nAssertion Error: OK!")