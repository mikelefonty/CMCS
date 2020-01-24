"""
Questo file viene utilizzato per generare matrici casuali di dimensione 7x7.
Le matrici binarie sono generate in modo tale che il numero di 1 presenti al loro interno sia controllabile.
In particolare, sia n = 10% del numero totale di matrici di generare.
Il programma genera n matrici in cui
la probabilità di avere una cella pari a 1 varia in {0.05,0.1,0.2,0.3,0.4, 0.5,
                      0.6, 0.7, 0.8, 0.9}
"""
from Utils.Util import *

if __name__ == "__main__":

    n_matrices = 1000000
    np.random.seed(42)
    size = 7

    "Lista delle matrici generate"
    matrices = []

    k = size // 2
    interval_print = 100

    "Lista che contiene le probabilità di avere una cella pari a 1"
    probs_1 = [0.05, 0.10, 0.20, 0.30, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    M = create_matrix_with_probs(size, 0)

    matrices.append(M)
    M = create_matrix_with_probs(size, 1)

    matrices.append(M)

    n_matrices -= 2
    n_generated = 2

    matrices_probs = {'0.05': [], '0.1': [], '0.2': [], '0.3': [], '0.4': [], '0.5': [],
                      '0.6': [], '0.7': [], '0.8': [], '0.9': []}

    n_matrices_per_prob = int(n_matrices * 1 / 10)

    for prob in probs_1:
        i = 0

        while i < n_matrices_per_prob:
            "Genero n_matrices_per_prob matrici 7x7 in cui la probabilità di avere 1 è pari a probs_1[i]"
            matrix_equals = False
            M = create_matrix_with_probs(size, prob)

            if not matrix_equals:
                "Se non ho già generato questa matrice, la salvo all'interno della lista matrices"
                i += 1
                matrices.append(M)
                matrices_probs[str(prob)].append(M)
                n_generated += 1

                if (i + 1) % interval_print == 0:
                    print("(%.2f%% )Created %s/%s matrices" % (((i + 1) * 100 / n_matrices), i + 1, n_matrices))

    "Salva le matrici generate"
    save_object(matrices, "../MatricesData/matrices_k_%s.pkl" % size)
    print("END")
