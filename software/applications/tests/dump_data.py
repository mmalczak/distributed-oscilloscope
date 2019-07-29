from data_serialization import save_object
from data_serialization import read_object
from GUI import *


class GUI_dumped:
    def __init__(self, GUI):
        self.available_ADCs = GUI.available_ADCs
        self.GUI_name = GUI.GUI_name

def dump_data_fun(GUI):
    gui_dumped = GUI_dumped(GUI)
    save_object(gui_dumped)
