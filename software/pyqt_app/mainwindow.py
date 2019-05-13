# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 1021, 671))
        self.graphicsView.setObjectName("graphicsView")
        self.vertical_settings_frame = QtWidgets.QFrame(self.centralwidget)
        self.vertical_settings_frame.setGeometry(QtCore.QRect(1050, 490, 441, 351))
        self.vertical_settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.vertical_settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.vertical_settings_frame.setObjectName("vertical_settings_frame")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.vertical_settings_frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 60, 401, 211))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.vertical_settings_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.vertical_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_settings_layout.setObjectName("vertical_settings_layout")
        self.trigger_settings_frame = QtWidgets.QFrame(self.centralwidget)
        self.trigger_settings_frame.setGeometry(QtCore.QRect(1050, 20, 210, 281))
        self.trigger_settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trigger_settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trigger_settings_frame.setObjectName("trigger_settings_frame")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.trigger_settings_frame)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(30, 30, 160, 201))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.triggers_settings_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.triggers_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.triggers_settings_layout.setObjectName("triggers_settings_layout")
        self.run_control_frame = QtWidgets.QFrame(self.centralwidget)
        self.run_control_frame.setGeometry(QtCore.QRect(1280, 20, 210, 281))
        self.run_control_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.run_control_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.run_control_frame.setObjectName("run_control_frame")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.run_control_frame)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 30, 160, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.run_control_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.run_control_layout.setContentsMargins(0, 0, 0, 0)
        self.run_control_layout.setObjectName("run_control_layout")
        self.horizontal_settings_frame = QtWidgets.QFrame(self.centralwidget)
        self.horizontal_settings_frame.setGeometry(QtCore.QRect(1050, 340, 441, 111))
        self.horizontal_settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.horizontal_settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontal_settings_frame.setObjectName("horizontal_settings_frame")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.horizontal_settings_frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 30, 381, 51))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.horizontal_settings_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.horizontal_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_settings_layout.setObjectName("horizontal_settings_layout")
        self.trigger_inputs_frame = QtWidgets.QFrame(self.centralwidget)
        self.trigger_inputs_frame.setGeometry(QtCore.QRect(10, 710, 201, 131))
        self.trigger_inputs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trigger_inputs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trigger_inputs_frame.setObjectName("trigger_inputs_frame")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.trigger_inputs_frame)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(20, 50, 151, 71))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.trigger_inputs_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.trigger_inputs_layout.setContentsMargins(0, 0, 0, 0)
        self.trigger_inputs_layout.setObjectName("trigger_inputs_layout")
        self.channel_inputs_frame = QtWidgets.QFrame(self.centralwidget)
        self.channel_inputs_frame.setGeometry(QtCore.QRect(229, 710, 801, 131))
        self.channel_inputs_frame.setAutoFillBackground(False)
        self.channel_inputs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.channel_inputs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.channel_inputs_frame.setObjectName("channel_inputs_frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.channel_inputs_frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 771, 101))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.channel_inputs_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.channel_inputs_layout.setContentsMargins(0, 0, 0, 0)
        self.channel_inputs_layout.setObjectName("channel_inputs_layout")
        self.trigger_settings_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.trigger_settings_label_2.setGeometry(QtCore.QRect(240, 700, 111, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.trigger_settings_label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.trigger_settings_label_2.setFont(font)
        self.trigger_settings_label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.trigger_settings_label_2.setAutoFillBackground(True)
        self.trigger_settings_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.trigger_settings_label_2.setObjectName("trigger_settings_label_2")
        self.trigger_settings_label_3 = QtWidgets.QLabel(self.centralwidget)
        self.trigger_settings_label_3.setGeometry(QtCore.QRect(30, 700, 161, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.trigger_settings_label_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.trigger_settings_label_3.setFont(font)
        self.trigger_settings_label_3.setAutoFillBackground(True)
        self.trigger_settings_label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.trigger_settings_label_3.setObjectName("trigger_settings_label_3")
        self.vertical_settings_label = QtWidgets.QLabel(self.centralwidget)
        self.vertical_settings_label.setGeometry(QtCore.QRect(1060, 480, 121, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.vertical_settings_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.vertical_settings_label.setFont(font)
        self.vertical_settings_label.setAutoFillBackground(True)
        self.vertical_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_settings_label.setObjectName("vertical_settings_label")
        self.trigger_settings_label = QtWidgets.QLabel(self.centralwidget)
        self.trigger_settings_label.setGeometry(QtCore.QRect(1060, 10, 121, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.trigger_settings_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.trigger_settings_label.setFont(font)
        self.trigger_settings_label.setAutoFillBackground(True)
        self.trigger_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trigger_settings_label.setObjectName("trigger_settings_label")
        self.horizontal_settings_label = QtWidgets.QLabel(self.centralwidget)
        self.horizontal_settings_label.setGeometry(QtCore.QRect(1060, 330, 141, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.horizontal_settings_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.horizontal_settings_label.setFont(font)
        self.horizontal_settings_label.setAutoFillBackground(True)
        self.horizontal_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontal_settings_label.setObjectName("horizontal_settings_label")
        self.trigger_settings_label_4 = QtWidgets.QLabel(self.centralwidget)
        self.trigger_settings_label_4.setGeometry(QtCore.QRect(1290, 10, 91, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.trigger_settings_label_4.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.trigger_settings_label_4.setFont(font)
        self.trigger_settings_label_4.setAutoFillBackground(True)
        self.trigger_settings_label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.trigger_settings_label_4.setObjectName("trigger_settings_label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.trigger_settings_label_2.setText(_translate("MainWindow", "Channel Inputs"))
        self.trigger_settings_label_3.setText(_translate("MainWindow", "External Trigger Input"))
        self.vertical_settings_label.setText(_translate("MainWindow", "Channel Settings"))
        self.trigger_settings_label.setText(_translate("MainWindow", "Trigger Settings"))
        self.horizontal_settings_label.setText(_translate("MainWindow", "Acquisition Settings"))
        self.trigger_settings_label_4.setText(_translate("MainWindow", "Run Control"))

from pyqtgraph import PlotWidget
