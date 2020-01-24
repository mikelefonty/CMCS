"""
Questo file contiene il main per eseguire la fase di validazione del modello di NN

----------NON AVVIARE PER EVITARE DI ALLENARE ULTERIORMENTE LA RETE GIA' ESISTENTE!!!!!!--------
"""

from NeuralNetwork.Build_NN import *
from Utils.Util_Directions import *
from keras.models import load_model


if __name__ == "__main__":
    fun_type = "density"
    k= 7
    X = load_object("../Dataset/X_%s_k_7.pkl"%fun_type)
    T = load_object("../Dataset/T_%s_k_7.pkl"%fun_type)

    X_empty = X[0]
    X_full = X[1]

    X = np.reshape(X, (X.shape[0], k,k ,1))

    print(X.shape)
    print(T.shape)
    print(T[0])
    np.random.shuffle([X[2:], T[2:]])

    train_test_split = 100000
    train_valid_split = 300000

    X_dev = X[:-train_test_split]
    T_dev = T[:-train_test_split]

    X_tr = X_dev[:-train_valid_split]
    T_tr = T_dev[:-train_valid_split]

    X_val = X_dev[-train_valid_split:]
    T_val = T_dev[-train_valid_split:]

    print(T_tr.shape)
    out_size = 9
    input_shape = (X.shape[1], X.shape[2], 1)

    filepath = "../Checkpoints/model_k_%s_valid_%s.h5"%(k,fun_type)
    plots_file = '../Plots/model3.png'

    # PARAMETRI NN!!!!!!!

    drop_rate = 0.2
    conv1_hidd = 256
    conv2_hidd = 128
    dense1_hidd = 256
    dense2_hidd = 128

    n_epochs = 200

    model = build_model_2(X, drop_rate, conv1_hidd, conv2_hidd,
                          dense1_hidd,
                          dense2_hidd,
                          "../Plots/architettura_nn.png")
    model.summary()

    es = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)
    # checkpoint

    checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss',
                                                 verbose=1, save_best_only=True, mode='min')
    
    history = model.fit(X_tr, T_tr, epochs=n_epochs, batch_size=1000, validation_data=(X_val, T_val),
                        verbose=1,
                        callbacks=[es, checkpoint])
                        
    model = load_model("../Checkpoints/model_k_7_valid_density.h5")
    print(model.evaluate(X[-train_test_split:],T[-train_test_split:]))
