# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(771, 367)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_13 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.label_13)
        self.gridLayout_cmds = QtWidgets.QGridLayout()
        self.gridLayout_cmds.setObjectName("gridLayout_cmds")
        self.Topic = QtWidgets.QLineEdit(self.frame)
        self.Topic.setObjectName("Topic")
        self.gridLayout_cmds.addWidget(self.Topic, 3, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_cmds.addWidget(self.label_5, 2, 3, 1, 1)
        self.MqttPort = QtWidgets.QLineEdit(self.frame)
        self.MqttPort.setObjectName("MqttPort")
        self.gridLayout_cmds.addWidget(self.MqttPort, 2, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_cmds.addItem(spacerItem, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_cmds.addWidget(self.label_4, 1, 3, 1, 1)
        self.FriendlyName = QtWidgets.QLineEdit(self.frame)
        self.FriendlyName.setObjectName("FriendlyName")
        self.gridLayout_cmds.addWidget(self.FriendlyName, 5, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_cmds.addWidget(self.label_2, 2, 0, 1, 1)
        self.FullTopic = QtWidgets.QLineEdit(self.frame)
        self.FullTopic.setEnabled(True)
        self.FullTopic.setObjectName("FullTopic")
        self.gridLayout_cmds.addWidget(self.FullTopic, 4, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_cmds.addWidget(self.label_3, 0, 3, 1, 1)
        self.password1 = QtWidgets.QLineEdit(self.frame)
        self.password1.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.password1.setObjectName("password1")
        self.gridLayout_cmds.addWidget(self.password1, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_cmds.addWidget(self.label, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout_cmds.addWidget(self.label_6, 3, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setEnabled(True)
        self.label_7.setObjectName("label_7")
        self.gridLayout_cmds.addWidget(self.label_7, 4, 3, 1, 1)
        self.MqttHost = QtWidgets.QLineEdit(self.frame)
        self.MqttHost.setObjectName("MqttHost")
        self.gridLayout_cmds.addWidget(self.MqttHost, 1, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.gridLayout_cmds.addWidget(self.label_9, 6, 3, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_cmds.addWidget(self.label_12, 0, 0, 1, 1)
        self.MqttPassword = QtWidgets.QLineEdit(self.frame)
        self.MqttPassword.setObjectName("MqttPassword")
        self.gridLayout_cmds.addWidget(self.MqttPassword, 7, 4, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.gridLayout_cmds.addWidget(self.label_8, 5, 3, 1, 1)
        self.MqttUser = QtWidgets.QLineEdit(self.frame)
        self.MqttUser.setObjectName("MqttUser")
        self.gridLayout_cmds.addWidget(self.MqttUser, 6, 4, 1, 1)
        self.ssid1 = QtWidgets.QLineEdit(self.frame)
        self.ssid1.setObjectName("ssid1")
        self.gridLayout_cmds.addWidget(self.ssid1, 1, 1, 1, 1)
        self.btn_save_conf = QtWidgets.QPushButton(self.frame)
        self.btn_save_conf.setEnabled(False)
        self.btn_save_conf.setObjectName("btn_save_conf")
        self.gridLayout_cmds.addWidget(self.btn_save_conf, 10, 4, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setObjectName("label_11")
        self.gridLayout_cmds.addWidget(self.label_11, 10, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setObjectName("label_10")
        self.gridLayout_cmds.addWidget(self.label_10, 7, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_cmds.addItem(spacerItem1, 9, 0, 1, 1)
        self.backlog = QtWidgets.QLineEdit(self.frame)
        self.backlog.setInputMask("")
        self.backlog.setText("")
        self.backlog.setObjectName("backlog")
        self.gridLayout_cmds.addWidget(self.backlog, 10, 1, 1, 3)
        self.verticalLayout_2.addLayout(self.gridLayout_cmds)
        self.lay_button = QtWidgets.QVBoxLayout()
        self.lay_button.setObjectName("lay_button")
        self.btn_send_conf = QtWidgets.QPushButton(self.frame)
        self.btn_send_conf.setEnabled(True)
        self.btn_send_conf.setObjectName("btn_send_conf")
        self.lay_button.addWidget(self.btn_send_conf)
        self.verticalLayout_2.addLayout(self.lay_button)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.ssid1, self.password1)
        Dialog.setTabOrder(self.password1, self.MqttHost)
        Dialog.setTabOrder(self.MqttHost, self.MqttPort)
        Dialog.setTabOrder(self.MqttPort, self.Topic)
        Dialog.setTabOrder(self.Topic, self.FullTopic)
        Dialog.setTabOrder(self.FullTopic, self.FriendlyName)
        Dialog.setTabOrder(self.FriendlyName, self.MqttUser)
        Dialog.setTabOrder(self.MqttUser, self.MqttPassword)
        Dialog.setTabOrder(self.MqttPassword, self.backlog)
        Dialog.setTabOrder(self.backlog, self.btn_save_conf)
        Dialog.setTabOrder(self.btn_save_conf, self.btn_send_conf)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Device configuration"))
        self.label_13.setText(_translate("Dialog", "Device Configuration"))
        self.label_5.setText(_translate("Dialog", "Port"))
        self.label_4.setText(_translate("Dialog", "Host"))
        self.label_2.setText(_translate("Dialog", "Password1:"))
        self.label_3.setText(_translate("Dialog", "MQTT"))
        self.label.setText(_translate("Dialog", "SSID1:"))
        self.label_6.setText(_translate("Dialog", "Topic"))
        self.label_7.setText(_translate("Dialog", "FullTopic"))
        self.label_9.setText(_translate("Dialog", "User (optional)"))
        self.label_12.setText(_translate("Dialog", "WIFI"))
        self.label_8.setText(_translate("Dialog", "FriendlyName"))
        self.btn_save_conf.setText(_translate("Dialog", "Save backlog cmd to config"))
        self.label_11.setText(_translate("Dialog", "Backlog CMD:"))
        self.label_10.setText(_translate("Dialog", "Password (optional)"))
        self.backlog.setToolTip(_translate("Dialog", "Maximum 30 commands!"))
        self.backlog.setPlaceholderText(_translate("Dialog", "devicename tasmotadevice; topic testtopic; ssid1 wfissid"))
        self.btn_send_conf.setText(_translate("Dialog", "Send configuration to device"))
