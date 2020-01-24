"""
Questo file contiene la funzione che crea l'architettura della rete neurale.

"""


import sys
sys.path.append("../")
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D
from keras.utils import plot_model


def build_model_2(X,  drop_rate, conv1_hidd, conv2_hidd, dense1_hidd,
                  dense2_hidd,plots_file=None):

    """
    Crea l'architettura della rete neurale.
    Architettura:
        Input->Conv->Conv->Flatten->Dense->Dense->Dropout->Output.
    Ottimizzatore:
        Adam

    :param X: Tensore di input
    :param drop_rate: Dropout rate
    :param drop_rate_conv: Dropout rate per convolutional layers
    :param conv1_hidd: Numero di hidden units nel primo conv layer
    :param conv2_hidd: Numero di hidden units nel secondo conv layer
    :param dense1_hidd: Numero di hidden units nel primo dense layer
    :param dense2_hidd: Numero di hidden units nel secondo dense layer
    :param plots_file: Se diverso da None, salva,nel path specificato,
                          un diagramma in pydot rappresentante il modello .
    :return: model : Modello di NN
    """
    input_shape = (X.shape[1], X.shape[2], 1)
    input = Input(shape=input_shape)
    conv1 = Conv2D(conv1_hidd, kernel_size=(3, 3), activation="relu", padding="same")(input)
    conv2 = Conv2D(conv2_hidd, kernel_size=(3, 3), activation="relu", padding="same")(conv1)

    flatten = Flatten()(conv2)

    dense1 = Dense(dense1_hidd, activation="relu")(flatten)

    dense2 = Dense(dense2_hidd, activation="relu")(dense1)
    dropout_2 = Dropout(drop_rate)(dense2)
    out = Dense(9, activation="softmax")(dropout_2)
    model = Model(inputs=input, outputs=out)
    model.summary()

    optimizer = keras.optimizers.Adam()
    if plots_file:
        plot_model(model, to_file=plots_file, show_shapes=True)
    model.compile(loss=keras.losses.mean_squared_error,
                  optimizer=optimizer)
    return model
