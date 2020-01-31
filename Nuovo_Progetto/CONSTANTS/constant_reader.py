"""
Questo file contiene l'implementazione della classe Constant_Reader. 
Il suo compito è quello di effettuare il parsing del file json contenente le varie costanti necessarie per
la simulazione.
"""


import os
import sys
import json
sys.path.append("../")


class Constant_Reader:

    """
    Crea l'oggetto ed effettua il parsing del file path. Salva in una struttura dati interna il risultato di tale operazione.
    """

    def __init__(self, path="./costanti.json"):
        self.path = path
        self.constants = {}
        self.__parse()

    """
    Effettua il parsing del file json avente percorso self.path.
    """

    def __parse(self):
        with open(self.path) as f:
            self.constants = json.load(f)

    """
    Restituisce il valore della costante FIGSIZE: dimensione della finestra che contiene l'animazione della simulazione.
    """

    def get_figsize(self):
        return (self.constants['FIGSIZE_x'], self.constants['FIGSIZE_y'])

    """
    Restituisce il valore della costante DELAY: tempo che intercorre tra una iterazione e la successiva nel corso dell'animazione.
    """

    def get_delay(self):
        return self.constants["DELAY"]

    """
    Restituisce il valore della costante EPS: 
    """

    def get_eps(self):
        return self.constants['EPS']

    """
    Restituisce il valore della costante TITLE_SIZE
    """

    def get_title_size(self):
        return self.constants['TITLE_SIZE']

    """
    Restituisce il valore della costante MARKER_SIZE
    """

    def get_marker_size(self):
        return self.constants['MARKER_SIZE']

    """
    Restituisce il valore della costante TEXT_SIZE
    """

    def get_text_size(self):
        return self.constants['TEXT_SIZE']

    def get_result_directory(self):
        return self.constants['RESULT_DIRECTORY']
