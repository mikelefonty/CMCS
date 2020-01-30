import sys
sys.path.append('../')
import numpy as np
from Environment.environment import Environment

def read_env_from_file(path):
    """
    Legge dal file una matrice e la carica in memoria
    :param path: Path del file da cui leggere la matrice
    :return: Matrice M letta da file.
    """
    n_rows = 0
    n_cols = 0

    with open(path, 'r') as f:

        current_line = 1
        l = []
        for line in f:
            if current_line == 1:
                n_rows = int(line)
                
            elif current_line == 2:
                n_cols = int(line)
            else:
                line_splitted = list(line.split(' '))
                line_int = [int(num)for num in line_splitted]
                l.append(line_int)
            
            current_line+=1
        
        matrix = np.array(l)
        print(matrix)
        """
        l.append([int(num) for num in line.split(' ')] for line in f.readline()])
        l = [[int(num) for num in line.split(' ')] for line in f]

        matrix = np.array(l)
       """
    #matrix = np.zeros((n_rows,n_cols))
    my_id = 1
   
    env = Environment(n_rows,n_cols)

    for row in range(n_rows):
        for col in range(n_cols):
            if matrix[row,col] > 0:
                #print(f'Adding agent {my_id} at position ({row},{col})')
                env.add_agents({my_id:(row,col)})
                my_id += 1
                
    return env

def create_environment(n_rows, n_cols, n_agents, save_path):
    """
    Crea un nuovo ambiente di dimensione (n_rows x n_cols), in cui sono presenti n_agents agenti.
    L'ambiente viene salvato in save_path.
    :param n_rows: Numero di righe dell'ambiente
    :param n_cols: Numero di colonne dell'ambiente
    :param n_agents: Numero di agenti all'interno dell'ambiente
    :param save_path: Path del file in cui salvare l'ambiente.
    :return: Ambiente env
    """
    env = np.zeros((n_rows, n_cols))
    n_agents_generated = 0

    while n_agents_generated < n_agents:

        x = np.random.randint(0, n_rows)
        y = np.random.randint(0, n_cols)

        if env[x, y] == 0:
            env[x, y] = 1
            n_agents_generated += 1

    with open(save_path, "w") as f:
        f.write(str(n_rows)+"\n")
        f.write(str(n_cols)+"\n")
        np.savetxt(f, env, fmt="%d")

    return env