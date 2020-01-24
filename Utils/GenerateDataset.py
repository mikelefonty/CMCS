"""
Questo file viene usato per generare un dataset a partire dai tasks creati precedentemente.
Un dataset è un insieme di coppie (X,T), dove X è una generica matrice e T è la distribuzione di
probabilità delle azioni associata alla matrice X
"""
from Utils.Util_Directions import *


def create_dataset(tasks):
    X = []
    T_prob = []

    for task in tasks:
        X.append(task.matrix)
        T_prob.append(task.probabilities)

    X = np.array(X)
    T_prob = np.array(T_prob)

    print(X.shape)
    print(T_prob.shape)
    print(tasks[0])
    print(tasks[1])
    return X, T_prob


if __name__ == "__main__":
    k = 7
    fun_type = "combine"
    load_path = "../TasksData/tasks"
    interval_print = 1000

    print("Loading tasks")
    tasks = load_object("%s_%s_k_%s.pkl" % (load_path, fun_type, k))

    np.random.seed(33)
    np.random.shuffle(tasks)

    X, T = create_dataset(tasks)
    print("Saving Tasks")
    save_object(X, "../Dataset/X_%s_k_%s.pkl" % (fun_type, k))
    print("Saved X")
    save_object(T, "../Dataset/T_%s_k_%s.pkl" % (fun_type, k))
    print("Saved T")
    print("END")
