"""
Questo file contiene il main per creare il modello finale di NN.

NON AVVIARE ALTRIMENTI SOVRASCRIVE LA RETE FINALE ESISTENTE!!!!!
"""

import sys
sys.path.append("../")
from NeuralNetwork.Build_NN import *
from Utils.Util_Directions import *
from keras.models import load_model
from matplotlib import pyplot as plt

if __name__ == "__main__":
    fun_type = "combine"

    k = 7
    X = load_object("../Dataset/X_%s_k_7.pkl" % fun_type)
    T = load_object("../Dataset/T_%s_k_7.pkl" % fun_type)

    X = np.reshape(X, (X.shape[0], k, k, 1))

    train_test_split = 100000

    X_dev = X[:-train_test_split]
    T_dev = T[:-train_test_split]

    X_test = X[-train_test_split:]
    T_test = T[-train_test_split:]

    out_size = 9
    input_shape = (X_dev.shape[1], X_dev.shape[2], 1)

    filepath = "../Checkpoints/model_k_%s_final_%s.h5" % (k, fun_type)
    plots_file = '../Plots/model3.png'

    # PARAMETRI NN!!!!!!!

    drop_rate = 0.2

    conv1_hidd = 256
    conv2_hidd = 128

    dense1_hidd = 256
    dense2_hidd = 128
    n_epochs = 200

    model = load_model(filepath)
    es = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)
    # checkpoint

    checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss',
                                                 verbose=1, save_best_only=True, mode='min')

    history = model.fit(X_dev, T_dev, epochs=n_epochs, batch_size=1000, validation_data=(X_test, T_test),
                        verbose=1,
                        callbacks=[es, checkpoint])

    plt.plot(history.history["loss"], label="Tr loss")
    plt.plot(history.history["val_loss"], label="Val loss")
    plt.legend(loc="best")
    plt.grid()
    plt.xlabel("Iterations")
    plt.ylabel("MSE")
    plt.tight_layout()
    plt.show()
