import sys
import json
sys.path.append("../")
import os

class Constant_Reader:

    def __init__(self,path="./aux.json"):
        self.path = path
        self.constants = {}
        self.parse()
       
    def parse(self):
        with open(self.path) as f:
            self.constants = json.load(f)    

    def get_figsize(self):
        return (self.constants['FIGSIZE_x'],self.constants['FIGSIZE_y'])

    def get_delay(self):
        return self.constants["DELAY"]
    
    def get_eps(self):
        return self.constants['EPS']

    def get_title_size(self):
        return self.constants['TITLE_SIZE']
    
    def get_marker_size(self):
        return self.constants['MARKER_SIZE']
    
    def get_text_size(self):
        return self.constants['TEXT_SIZE']