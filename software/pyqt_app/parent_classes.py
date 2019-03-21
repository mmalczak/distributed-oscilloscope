from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel


class Button(QtGui.QPushButton):

    def __init__(self, button_name, idx, unique_ADC_name):
        super().__init__(button_name)
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        self.setCheckable(True)
        self.clicked.connect(self.action)

    def action(self):
        pass
    
    def set_active(self, active):
        if(self.isChecked() != active): #negation because its off when its checked
            pass
        else:
            self.toggle()
    
    def is_active(self):
        return (not self.isChecked())


class Menu(QMenuBar):
    def __init__(self, idx, unique_ADC_name):
        super().__init__()
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
#        self.setMaximumSize(130, 30)


class Box(QtGui.QWidget):
    
    def __init__(self, idx, unique_ADC_name, box_name):
        super().__init__()
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        self.layout = QtGui.QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.box = QSpinBox()
        self.label = QLabel(box_name)
        self.layout.addWidget(self.box)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.box.editingFinished.connect(self.value_change)
    
    def value_change(self):
        pass
    
    def set_value(self, value):
        self.box.setValue(value)


class TriggerPolarity(Menu):
    
    def __init__(self, idx, unique_ADC_name):
        super().__init__(idx, unique_ADC_name)
        self.polarity = self.addMenu("Polarity")
        self.polarity.setTitle("Polarity")
        polarity_0 = self.polarity.addAction("0")
        polarity_0.setText("0")
        polarity_0.triggered.connect(self.action)
        polarity_1 = self.polarity.addAction("1")
        polarity_1.setText("1")
        polarity_1.triggered.connect(self.action)
    
    def set_value(self, value):
        self.polarity.setTitle("Polarity" + str(value))
    
    def action(self):
        pass




