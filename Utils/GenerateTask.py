"""
Questo file viene usato per generare i tasks a partire dalle matrici generate precedentemente.
Un Task è una struttura che contiene:
1)Matrice
2)Direzione da scegliere (la più probabile)
3)Distribuzione di probabilità delle azioni possibili.
"""

from Utils.Util_Directions import *

k = 7

"Funzione da usare per calcolare la direzione"
fun_type = "combine"

save_path = "../TasksData/tasks"
interval_print = 1000

print("Loading matrices")
matrices = load_object("../MatricesData/matrices_k_%s.pkl"%k)
print("Loaded")


tasks = []
n_matrices = len(matrices)
error = False

if fun_type == "distance":
    print("Creating Task with Distance Function")
    save_path = save_path + "_distance_k_"+str(k)+".pkl"
elif fun_type == "density":
    print("Creating Task with Density Function")
    save_path = save_path + "_density_k_"+str(k)+".pkl"

elif fun_type == "combine":
    print("Creating Task with Combine Function")
    save_path = save_path + "_combine_k_"+str(k)+".pkl"

else:
    print("ERROR: FUN_TYPE ERRATO")
    error = True

if not error:
    for (i, m) in enumerate(matrices):

        "Per ogni matrice genero il relativo task"

        if fun_type == "distance":

            direction, distances, probs = compute_direction_distance(m)

        elif fun_type == "density":

            direction, probs = compute_direction_density(m)

        elif fun_type == "combine":
            direction, probs = combine(m)

        tasks.append(Task(m, direction, probs))

        if (i + 1) % interval_print == 0:
            print("(%.2f%% )Created %s/%s tasks" % (((i + 1) * 100 / n_matrices), i + 1, n_matrices))

    print("Created %s Tasks" % (len(matrices)))
    save_object(tasks, save_path)
    print("END")
