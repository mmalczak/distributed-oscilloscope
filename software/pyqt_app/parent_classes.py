from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel
from colors import Colors
from PyQt5.QtCore import Qt


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



class Box(QtGui.QWidget):

    def __init__(self, idx, unique_ADC_name, box_name):
        super().__init__()
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        self.layout = QtGui.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.box = QSpinBox()
        self.label = QLabel(box_name)
        self.layout.addWidget(self.box)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.box.editingFinished.connect(self.value_change)
        """If unique_ADC_name is None it means that the certain channel
        is no enabled therefore the widget is disabled"""
        if(unique_ADC_name is None):
            self.setEnabled(False)


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


class ChannelLabel(QLabel):
    def __init__(self, channel_count):
        chan_disp = str(channel_count + 1)
        """+1 is beacuse channels are indexed from 0, but displayed from 1"""
        super().__init__("Channel " + chan_disp)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.setMaximumHeight(25)
        color = str((tuple(Colors().get_color(channel_count))))
        self.setStyleSheet("border: 1px solid rgb" + color + ";")
 
