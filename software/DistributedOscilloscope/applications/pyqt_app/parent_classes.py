from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QDial
from .colors import Colors
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFrame


class Button(QtGui.QPushButton):

    def __init__(self, button_name, idx, unique_ADC_name):
        super().__init__(button_name)
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        self.setCheckable(True)
        self.clicked.connect(self.action)
        """If unique_ADC_name is None it means that the certain channel
        is no enabled therefore the widget is disabled"""
        if(unique_ADC_name is None):
            self.setEnabled(False)

    def action(self):
        pass

    def set_active(self, active):
        if(self.isChecked() != active):
            """negation because its off when its checked"""
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
        """self.setMaximumSize(130, 30)"""
        """If unique_ADC_name is None it means that the certain channel
        is no enabled therefore the widget is disabled"""
        if(unique_ADC_name is None):
            self.setEnabled(False)


class Dial_Box(QtGui.QWidget):

    def __init__(self, idx, unique_ADC_name, dial_name, layout='horizontal'):
        super().__init__()
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        if layout == "horizontal":
            self.layout = QtGui.QHBoxLayout()
        else:
            self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)

        self.frame = QFrame()
        self.frame.setLayout(self.layout)
        #self.frame.setStyleSheet("border:0px solid rgb(200, 200, 200); ")

        self.dial= QDial()
        self.label = QLabel(dial_name)
        self.box = QSpinBox()

        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dial)
        self.layout.addWidget(self.box)

        self.dial.valueChanged.connect(self.value_change_dial)
        self.box.valueChanged.connect(self.value_change_box)
        """If unique_ADC_name is None it means that the certain channel
        is no enabled therefore the widget is disabled"""
        if(unique_ADC_name is None):
            self.frame.setEnabled(False)

    def value_change_dial(self):
        pass

    def value_change_box(self):
        pass

    def set_value(self, value):
        pass

    def get_value(self):
        return self.dial.value()


class Slider_Box(QtGui.QWidget):

    def __init__(self, idx, unique_ADC_name, slider_name, layout='horizontal'):
        super().__init__()
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        if layout == "horizontal":
            self.layout = QtGui.QHBoxLayout()
        else:
            self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.slider = QSlider(Qt.Horizontal)
        self.label = QLabel(slider_name)
        self.box = QSpinBox()
        self.layout.addWidget(self.box)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.slider.valueChanged.connect(self.value_change_slider)
        self.box.valueChanged.connect(self.value_change_box)
        """If unique_ADC_name is None it means that the certain channel
        is no enabled therefore the widget is disabled"""
        if(unique_ADC_name is None):
            self.setEnabled(False)

    def value_change_slider(self):
        pass

    def value_change_box(self):
        pass

    def set_value(self, value):
        self.slider.setValue(value)
        self.box.setValue(value)

    def get_value(self):
        return self.slider.value()


class Box(QtGui.QWidget):

    def __init__(self, idx, unique_ADC_name, box_name, layout='horizontal',
                 signal_connect='valueChanged'):
        super().__init__()
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        if layout == "horizontal":
            self.layout = QtGui.QHBoxLayout()
        else:
            self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.box = QSpinBox()
        self.label = QLabel(box_name)
        self.layout.addWidget(self.box)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        getattr(self.box, signal_connect).connect(self.value_change)
        #self.box.valueChanged.connect(self.value_change)
        #self.box.editingFinished.connect(self.value_change)
        """If unique_ADC_name is None it means that the certain channel
        is no enabled therefore the widget is disabled"""
        if(unique_ADC_name is None):
            self.setEnabled(False)

    def value_change(self):
        pass

    def set_value(self, value):
        self.box.setValue(value)

    def get_value(self):
        return self.box.value()
