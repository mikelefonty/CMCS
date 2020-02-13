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

    def __init__(self, path="../CONSTANTS/costanti.json"):
        self.path = path
        self.constants = {}
        self.__parse()


    def __parse(self):
        
        """
        Effettua il parsing del file json avente percorso self.path.
        """
        with open(self.path) as f:
            self.constants = json.load(f)


    def get_figsize(self):
        
        """
        Restituisce il valore della costante FIGSIZE: dimensione della finestra che contiene l'animazione della simulazione.
        """
        return (self.constants['FIGSIZE_x'], self.constants['FIGSIZE_y'])



    def get_delay(self):
        """
        Restituisce il valore della costante DELAY: tempo che intercorre tra una iterazione e la successiva nel corso dell'animazione.
        """
        return self.constants["DELAY"]

   

    def get_eps(self):
        """
        Restituisce il valore della costante EPS: 
        """
        return self.constants['EPS']



    def get_title_size(self):
        """
        Restituisce il valore della costante TITLE_SIZE
        """
        return self.constants['TITLE_SIZE']

  

    def get_marker_size(self):
        """
        Restituisce il valore della costante MARKER_SIZE
        """
        return self.constants['MARKER_SIZE']

   

    def get_text_size(self):
        """
        Restituisce il valore della costante TEXT_SIZE
        """
        return self.constants['TEXT_SIZE']

    def get_result_directory(self):
        """
        Restituisce il valore della costante RESULT_DIRECTORY
        """
        return self.constants['RESULT_DIRECTORY']

    def get_colors(self):
        """
        Restituisce il valore della costante COLORS
        """
        return self.constants['COLORS']
    
    def get_radius(self):
        """
        Restituisce il valore della costante RADIUS
        """
        return self.constants['RADIUS']
    
    def get_min_pts(self):
        """
        Restituisce il valore della costante MIN_PTS
        """
        return self.constants['MIN_PTS']

    def get_env_directory(self):
        """
        Restituisce il valore della costante ENV_DIRECTORY
        """
        return self.constants['ENV_DIRECTORY']