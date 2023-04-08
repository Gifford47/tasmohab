# Form implementation generated from reading ui file 'tasmohabUI.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1074, 864)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setToolTipDuration(-1)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.txt_user = QtWidgets.QLineEdit(self.groupBox)
        self.txt_user.setMaximumSize(QtCore.QSize(150, 16777215))
        self.txt_user.setObjectName("txt_user")
        self.gridLayout_3.addWidget(self.txt_user, 1, 1, 1, 1)
        self.btn_get_serial = QtWidgets.QPushButton(self.groupBox)
        self.btn_get_serial.setObjectName("btn_get_serial")
        self.gridLayout_3.addWidget(self.btn_get_serial, 3, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 2, 1, 1)
        self.txt_pass = QtWidgets.QLineEdit(self.groupBox)
        self.txt_pass.setMaximumSize(QtCore.QSize(150, 16777215))
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.txt_pass.setObjectName("txt_pass")
        self.gridLayout_3.addWidget(self.txt_pass, 2, 1, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 0, 0, 1, 1)
        self.cmb_baud = QtWidgets.QComboBox(self.groupBox)
        self.cmb_baud.setObjectName("cmb_baud")
        self.cmb_baud.addItem("")
        self.cmb_baud.addItem("")
        self.gridLayout_6.addWidget(self.cmb_baud, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_6, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.txt_ip = QtWidgets.QLineEdit(self.groupBox)
        self.txt_ip.setMaximumSize(QtCore.QSize(150, 16777215))
        self.txt_ip.setObjectName("txt_ip")
        self.gridLayout_3.addWidget(self.txt_ip, 0, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cmb_ports = QtWidgets.QComboBox(self.groupBox)
        self.cmb_ports.setObjectName("cmb_ports")
        self.gridLayout_2.addWidget(self.cmb_ports, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.btn_serport_refr = QtWidgets.QPushButton(self.groupBox)
        self.btn_serport_refr.setObjectName("btn_serport_refr")
        self.gridLayout_2.addWidget(self.btn_serport_refr, 0, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 3, 1, 1)
        self.btn_get_http = QtWidgets.QPushButton(self.groupBox)
        self.btn_get_http.setEnabled(True)
        self.btn_get_http.setObjectName("btn_get_http")
        self.gridLayout_3.addWidget(self.btn_get_http, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setMaximumSize(QtCore.QSize(200, 40))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/img/img/tasmota_logo.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 4, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.verticalLayout_9.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 0, 3, 1, 1)
        self.lbl_firmware = QtWidgets.QLabel(self.groupBox_4)
        self.lbl_firmware.setObjectName("lbl_firmware")
        self.gridLayout_5.addWidget(self.lbl_firmware, 0, 1, 1, 1)
        self.lbl_dev_firmware = QtWidgets.QLabel(self.groupBox_4)
        self.lbl_dev_firmware.setText("")
        self.lbl_dev_firmware.setObjectName("lbl_dev_firmware")
        self.gridLayout_5.addWidget(self.lbl_dev_firmware, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 0, 2, 1, 1)
        self.lbl_dev_module = QtWidgets.QLabel(self.groupBox_4)
        self.lbl_dev_module.setText("")
        self.lbl_dev_module.setObjectName("lbl_dev_module")
        self.gridLayout_5.addWidget(self.lbl_dev_module, 1, 3, 1, 1)
        self.lbl_dev_name = QtWidgets.QLabel(self.groupBox_4)
        self.lbl_dev_name.setText("")
        self.lbl_dev_name.setObjectName("lbl_dev_name")
        self.gridLayout_5.addWidget(self.lbl_dev_name, 1, 2, 1, 1)
        self.btn_dev_details = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_dev_details.setEnabled(True)
        self.btn_dev_details.setObjectName("btn_dev_details")
        self.gridLayout_5.addWidget(self.btn_dev_details, 1, 4, 1, 1)
        self.lbl_dev_hostname = QtWidgets.QLabel(self.groupBox_4)
        self.lbl_dev_hostname.setText("")
        self.lbl_dev_hostname.setObjectName("lbl_dev_hostname")
        self.gridLayout_5.addWidget(self.lbl_dev_hostname, 1, 0, 1, 1)
        self.lbl_dev_stat_2 = QtWidgets.QLabel(self.groupBox_4)
        self.lbl_dev_stat_2.setObjectName("lbl_dev_stat_2")
        self.gridLayout_5.addWidget(self.lbl_dev_stat_2, 0, 0, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout_5)
        self.verticalLayout_9.addWidget(self.groupBox_4)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.txt_config_file_path = QtWidgets.QLineEdit(self.groupBox_2)
        self.txt_config_file_path.setObjectName("txt_config_file_path")
        self.gridLayout_4.addWidget(self.txt_config_file_path, 0, 1, 1, 1)
        self.btn_load_object = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_load_object.setObjectName("btn_load_object")
        self.gridLayout_4.addWidget(self.btn_load_object, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_set_dev_conf = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_set_dev_conf.setEnabled(False)
        self.btn_set_dev_conf.setObjectName("btn_set_dev_conf")
        self.horizontalLayout.addWidget(self.btn_set_dev_conf)
        self.btn_gen_rules = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_gen_rules.setEnabled(False)
        self.btn_gen_rules.setObjectName("btn_gen_rules")
        self.horizontalLayout.addWidget(self.btn_gen_rules)
        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_4)
        self.verticalLayout_9.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_3.setToolTip("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.lbl_location = QtWidgets.QLabel(self.groupBox_3)
        self.lbl_location.setObjectName("lbl_location")
        self.gridLayout_11.addWidget(self.lbl_location, 0, 0, 1, 1)
        self.txt_location = QtWidgets.QLineEdit(self.groupBox_3)
        self.txt_location.setObjectName("txt_location")
        self.gridLayout_11.addWidget(self.txt_location, 0, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_11)
        self.cb_sel_all = QtWidgets.QCheckBox(self.groupBox_3)
        self.cb_sel_all.setObjectName("cb_sel_all")
        self.verticalLayout_6.addWidget(self.cb_sel_all)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_3)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 972, 86))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_8.addWidget(self.scrollArea)
        self.verticalLayout_6.addLayout(self.verticalLayout_8)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setToolTipDuration(-1)
        self.label_11.setStatusTip("")
        self.label_11.setWhatsThis("")
        self.label_11.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.label_11.setObjectName("label_11")
        self.gridLayout_10.addWidget(self.label_11, 0, 0, 1, 1)
        self.cmb_outp_format = QtWidgets.QComboBox(self.groupBox_3)
        self.cmb_outp_format.setMaximumSize(QtCore.QSize(200, 16777215))
        self.cmb_outp_format.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cmb_outp_format.setObjectName("cmb_outp_format")
        self.gridLayout_10.addWidget(self.cmb_outp_format, 0, 1, 1, 1)
        self.btn_edittmpl = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_edittmpl.setObjectName("btn_edittmpl")
        self.gridLayout_10.addWidget(self.btn_edittmpl, 1, 2, 1, 1)
        self.cmb_template = QtWidgets.QComboBox(self.groupBox_3)
        self.cmb_template.setMaximumSize(QtCore.QSize(200, 16777215))
        self.cmb_template.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cmb_template.setObjectName("cmb_template")
        self.gridLayout_10.addWidget(self.cmb_template, 1, 1, 1, 1)
        self.btn_refr_obj_data = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_refr_obj_data.setEnabled(False)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.btn_refr_obj_data.setFont(font)
        self.btn_refr_obj_data.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btn_refr_obj_data.setAutoFillBackground(False)
        self.btn_refr_obj_data.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.btn_refr_obj_data.setObjectName("btn_refr_obj_data")
        self.gridLayout_10.addWidget(self.btn_refr_obj_data, 1, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_10.setObjectName("label_10")
        self.gridLayout_10.addWidget(self.label_10, 1, 0, 1, 1)
        self.btn_helpfullurls = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_helpfullurls.setObjectName("btn_helpfullurls")
        self.gridLayout_10.addWidget(self.btn_helpfullurls, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_10, 7, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.verticalLayout_9.addWidget(self.groupBox_3)
        self.verticalLayout_3.addWidget(self.frame)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_13.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.config_txtbrowser = QtWidgets.QTextBrowser(self.tab_2)
        self.config_txtbrowser.setReadOnly(False)
        self.config_txtbrowser.setObjectName("config_txtbrowser")
        self.verticalLayout.addWidget(self.config_txtbrowser)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.btn_show_json_obj = QtWidgets.QPushButton(self.tab_2)
        self.btn_show_json_obj.setObjectName("btn_show_json_obj")
        self.gridLayout_9.addWidget(self.btn_show_json_obj, 0, 0, 1, 1)
        self.btn_save_config = QtWidgets.QPushButton(self.tab_2)
        self.btn_save_config.setObjectName("btn_save_config")
        self.gridLayout_9.addWidget(self.btn_save_config, 0, 2, 1, 1)
        self.btn_show_json_config = QtWidgets.QPushButton(self.tab_2)
        self.btn_show_json_config.setObjectName("btn_show_json_config")
        self.gridLayout_9.addWidget(self.btn_show_json_config, 0, 1, 1, 1)
        self.btn_gen_fin_objts = QtWidgets.QPushButton(self.tab_2)
        self.btn_gen_fin_objts.setEnabled(False)
        self.btn_gen_fin_objts.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.btn_gen_fin_objts.setObjectName("btn_gen_fin_objts")
        self.gridLayout_9.addWidget(self.btn_gen_fin_objts, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_9)
        self.gridLayout_13.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.label_12 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_16.addWidget(self.label_12, 0, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_16.addWidget(self.label_13, 0, 1, 1, 1)
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.txt_thing_file = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_thing_file.sizePolicy().hasHeightForWidth())
        self.txt_thing_file.setSizePolicy(sizePolicy)
        self.txt_thing_file.setObjectName("txt_thing_file")
        self.gridLayout_18.addWidget(self.txt_thing_file, 1, 1, 1, 1)
        self.lbl_thing_file = QtWidgets.QLabel(self.tab_3)
        self.lbl_thing_file.setObjectName("lbl_thing_file")
        self.gridLayout_18.addWidget(self.lbl_thing_file, 1, 0, 1, 1)
        self.txt_item_file = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_item_file.sizePolicy().hasHeightForWidth())
        self.txt_item_file.setSizePolicy(sizePolicy)
        self.txt_item_file.setObjectName("txt_item_file")
        self.gridLayout_18.addWidget(self.txt_item_file, 2, 1, 1, 1)
        self.lbl_item_file = QtWidgets.QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_item_file.sizePolicy().hasHeightForWidth())
        self.lbl_item_file.setSizePolicy(sizePolicy)
        self.lbl_item_file.setObjectName("lbl_item_file")
        self.gridLayout_18.addWidget(self.lbl_item_file, 2, 0, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_18, 1, 0, 1, 1)
        self.btn_save_final_via_rest = QtWidgets.QPushButton(self.tab_3)
        self.btn_save_final_via_rest.setEnabled(False)
        self.btn_save_final_via_rest.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.btn_save_final_via_rest.setObjectName("btn_save_final_via_rest")
        self.gridLayout_16.addWidget(self.btn_save_final_via_rest, 4, 1, 1, 1)
        self.btn_save_final_to_file = QtWidgets.QPushButton(self.tab_3)
        self.btn_save_final_to_file.setEnabled(False)
        self.btn_save_final_to_file.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.btn_save_final_to_file.setObjectName("btn_save_final_to_file")
        self.gridLayout_16.addWidget(self.btn_save_final_to_file, 4, 0, 1, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.cmb_oh_ips = QtWidgets.QComboBox(self.tab_3)
        self.cmb_oh_ips.setObjectName("cmb_oh_ips")
        self.gridLayout_19.addWidget(self.cmb_oh_ips, 0, 0, 1, 1)
        self.cb_link_items = QtWidgets.QCheckBox(self.tab_3)
        self.cb_link_items.setChecked(True)
        self.cb_link_items.setObjectName("cb_link_items")
        self.gridLayout_19.addWidget(self.cb_link_items, 2, 0, 1, 1)
        self.cb_create_items = QtWidgets.QCheckBox(self.tab_3)
        self.cb_create_items.setChecked(True)
        self.cb_create_items.setObjectName("cb_create_items")
        self.gridLayout_19.addWidget(self.cb_create_items, 1, 0, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_19, 1, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_16, 2, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.lbl_output = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_output.setFont(font)
        self.lbl_output.setObjectName("lbl_output")
        self.verticalLayout_10.addWidget(self.lbl_output)
        self.txt_output_thing = QtWidgets.QTextBrowser(self.tab_3)
        self.txt_output_thing.setReadOnly(False)
        self.txt_output_thing.setObjectName("txt_output_thing")
        self.verticalLayout_10.addWidget(self.txt_output_thing)
        self.lbl_output_2 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_output_2.setFont(font)
        self.lbl_output_2.setObjectName("lbl_output_2")
        self.verticalLayout_10.addWidget(self.lbl_output_2)
        self.txt_output_item = QtWidgets.QTextBrowser(self.tab_3)
        self.txt_output_item.setReadOnly(False)
        self.txt_output_item.setObjectName("txt_output_item")
        self.verticalLayout_10.addWidget(self.txt_output_item)
        self.gridLayout_7.addLayout(self.verticalLayout_10, 0, 0, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.lbl_log_2 = QtWidgets.QLabel(self.tab_4)
        self.lbl_log_2.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_log_2.setFont(font)
        self.lbl_log_2.setObjectName("lbl_log_2")
        self.verticalLayout_11.addWidget(self.lbl_log_2)
        self.txt_log = QtWidgets.QTextBrowser(self.tab_4)
        self.txt_log.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_log.setObjectName("txt_log")
        self.verticalLayout_11.addWidget(self.txt_log)
        self.btn_clear_log = QtWidgets.QPushButton(self.tab_4)
        self.btn_clear_log.setObjectName("btn_clear_log")
        self.verticalLayout_11.addWidget(self.btn_clear_log)
        self.gridLayout_8.addLayout(self.verticalLayout_11, 0, 0, 1, 1)
        self.gridLayout_15.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setStyleSheet(" QProgressBar::chunk\n"
" {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 223, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
" }")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_last_log_txt = QtWidgets.QLabel(self.centralwidget)
        self.lbl_last_log_txt.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lbl_last_log_txt.setObjectName("lbl_last_log_txt")
        self.horizontalLayout_3.addWidget(self.lbl_last_log_txt)
        self.lbl_last_log = QtWidgets.QLabel(self.centralwidget)
        self.lbl_last_log.setText("")
        self.lbl_last_log.setWordWrap(True)
        self.lbl_last_log.setObjectName("lbl_last_log")
        self.horizontalLayout_3.addWidget(self.lbl_last_log)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1074, 26))
        self.menubar.setObjectName("menubar")
        self.menuTasmHAB = QtWidgets.QMenu(self.menubar)
        self.menuTasmHAB.setObjectName("menuTasmHAB")
        self.menuLoad_Config = QtWidgets.QMenu(self.menuTasmHAB)
        self.menuLoad_Config.setObjectName("menuLoad_Config")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_save_conf = QtGui.QAction(MainWindow)
        self.action_save_conf.setObjectName("action_save_conf")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionInfo = QtGui.QAction(MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.actionLoad_conf = QtGui.QAction(MainWindow)
        self.actionLoad_conf.setObjectName("actionLoad_conf")
        self.actionEdit_conf = QtGui.QAction(MainWindow)
        self.actionEdit_conf.setObjectName("actionEdit_conf")
        self.menuLoad_Config.addAction(self.actionEdit_conf)
        self.menuLoad_Config.addAction(self.actionLoad_conf)
        self.menuTasmHAB.addSeparator()
        self.menuTasmHAB.addAction(self.actionExit)
        self.menuTasmHAB.addAction(self.menuLoad_Config.menuAction())
        self.menuAbout.addAction(self.actionInfo)
        self.menubar.addAction(self.menuTasmHAB.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.cmb_baud.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.txt_ip, self.txt_user)
        MainWindow.setTabOrder(self.txt_user, self.txt_pass)
        MainWindow.setTabOrder(self.txt_pass, self.btn_get_http)
        MainWindow.setTabOrder(self.btn_get_http, self.cmb_ports)
        MainWindow.setTabOrder(self.cmb_ports, self.btn_serport_refr)
        MainWindow.setTabOrder(self.btn_serport_refr, self.cmb_baud)
        MainWindow.setTabOrder(self.cmb_baud, self.btn_get_serial)
        MainWindow.setTabOrder(self.btn_get_serial, self.btn_dev_details)
        MainWindow.setTabOrder(self.btn_dev_details, self.btn_load_object)
        MainWindow.setTabOrder(self.btn_load_object, self.txt_config_file_path)
        MainWindow.setTabOrder(self.txt_config_file_path, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.config_txtbrowser)
        MainWindow.setTabOrder(self.config_txtbrowser, self.btn_show_json_obj)
        MainWindow.setTabOrder(self.btn_show_json_obj, self.btn_save_config)
        MainWindow.setTabOrder(self.btn_save_config, self.btn_show_json_config)
        MainWindow.setTabOrder(self.btn_show_json_config, self.btn_gen_fin_objts)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TasmoHAB"))
        self.groupBox.setTitle(_translate("MainWindow", "Connection to Tasmota device"))
        self.label_2.setText(_translate("MainWindow", "Username"))
        self.btn_get_serial.setToolTip(_translate("MainWindow", "get data from tasmota device by serial"))
        self.btn_get_serial.setText(_translate("MainWindow", "Get from Serial"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.label_8.setText(_translate("MainWindow", "Baudrate"))
        self.cmb_baud.setItemText(0, _translate("MainWindow", "9600"))
        self.cmb_baud.setItemText(1, _translate("MainWindow", "115200"))
        self.label.setText(_translate("MainWindow", "Tasmota IP"))
        self.txt_ip.setText(_translate("MainWindow", "192.168.1.80"))
        self.label_4.setText(_translate("MainWindow", "COM"))
        self.btn_serport_refr.setText(_translate("MainWindow", "Refresh list"))
        self.btn_get_http.setToolTip(_translate("MainWindow", "get data from tasmota device by http"))
        self.btn_get_http.setText(_translate("MainWindow", "Get from HTTP"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Tasmota Device Status"))
        self.label_6.setText(_translate("MainWindow", "Module"))
        self.lbl_firmware.setText(_translate("MainWindow", "Firmware"))
        self.label_7.setText(_translate("MainWindow", "DeviceName"))
        self.btn_dev_details.setText(_translate("MainWindow", "Details"))
        self.lbl_dev_stat_2.setText(_translate("MainWindow", "Hostname"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Device config"))
        self.btn_load_object.setToolTip(_translate("MainWindow", "<html><head/><body><p>loads a predefined config file for the tasmota device.</p><p>You can use this to restore settings from another tasmota device to a new one.</p></body></html>"))
        self.btn_load_object.setText(_translate("MainWindow", "Load device config"))
        self.btn_set_dev_conf.setText(_translate("MainWindow", "Set Device Config"))
        self.btn_gen_rules.setText(_translate("MainWindow", "Edit Rules"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Items"))
        self.lbl_location.setText(_translate("MainWindow", "Model location"))
        self.txt_location.setText(_translate("MainWindow", "GroundFloor"))
        self.cb_sel_all.setText(_translate("MainWindow", "select/ deselect all Checkboxes"))
        self.label_11.setToolTip(_translate("MainWindow", "Select the right OpenHab config (definded in tasmohab.cfg)"))
        self.label_11.setText(_translate("MainWindow", "OpenHab Config"))
        self.cmb_outp_format.setToolTip(_translate("MainWindow", "select the right OH config (tasmohab.cfg)"))
        self.btn_edittmpl.setToolTip(_translate("MainWindow", "<html><head/><body><p>Opens an associated editor (i.e. notepad) for the *.tpl files (selected template).</p></body></html>"))
        self.btn_edittmpl.setText(_translate("MainWindow", "Edit Template"))
        self.cmb_template.setToolTip(_translate("MainWindow", "<html><head/><body><p>choose the right output format (txt or API) defined in template files (... ohgen/templates/MyTemplateFile.tpl)</p></body></html>"))
        self.btn_refr_obj_data.setToolTip(_translate("MainWindow", "<html><head/><body><p>The YAML config is translated to JSON. The selected template file is then performed.</p><p>Please be careful which output/ template you choose!</p></body></html>"))
        self.btn_refr_obj_data.setText(_translate("MainWindow", "Refresh object and show preview"))
        self.label_10.setToolTip(_translate("MainWindow", "choose the right output format defined in template files (... ohgen/templates/MyTemplateFile.tpl)"))
        self.label_10.setText(_translate("MainWindow", "Output template:"))
        self.btn_helpfullurls.setToolTip(_translate("MainWindow", "<html><head/><body><p>URL can be edited in tasmohab.cfg.</p></body></html>"))
        self.btn_helpfullurls.setText(_translate("MainWindow", "Helpfull config URLs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Get and Set"))
        self.label_9.setText(_translate("MainWindow", "YAML Format (editable)"))
        self.btn_show_json_obj.setToolTip(_translate("MainWindow", "Show all GPIO info from the tasmota device."))
        self.btn_show_json_obj.setText(_translate("MainWindow", "Show Tasmota GPIOs"))
        self.btn_save_config.setToolTip(_translate("MainWindow", "Save the above configuration to a file."))
        self.btn_save_config.setText(_translate("MainWindow", "Save YAML Device Config"))
        self.btn_show_json_config.setToolTip(_translate("MainWindow", "<html><head/><body><p>The YAML configuration is translated to JSON.</p><p>The JSON format is used to apply the selected template.</p></body></html>"))
        self.btn_show_json_config.setText(_translate("MainWindow", "Show current Json Object"))
        self.btn_gen_fin_objts.setToolTip(_translate("MainWindow", "<html><head/><body><p>The YAML config is translated to JSON. The selected template file is then performed.</p></body></html>"))
        self.btn_gen_fin_objts.setText(_translate("MainWindow", "Generate final objects"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Device Config Preview"))
        self.label_12.setText(_translate("MainWindow", "Config text File"))
        self.label_13.setText(_translate("MainWindow", "REST API"))
        self.txt_thing_file.setToolTip(_translate("MainWindow", "select where the things file should be stored"))
        self.lbl_thing_file.setText(_translate("MainWindow", "Things path"))
        self.txt_item_file.setToolTip(_translate("MainWindow", "select where the items file should be stored"))
        self.lbl_item_file.setText(_translate("MainWindow", "Items path"))
        self.btn_save_final_via_rest.setToolTip(_translate("MainWindow", "<html><head/><body><p>The above configuration is saved via REST API.</p><p>Please check the correct settings in tasmohab.cfg.</p><p>Also basic authentication under API Security-&gt; Show advanced must be enabled!</p></body></html>"))
        self.btn_save_final_via_rest.setText(_translate("MainWindow", "Save Thing and Item via REST API"))
        self.btn_save_final_to_file.setToolTip(_translate("MainWindow", "<html><head/><body><p>The above configuration is saved via txt files.</p></body></html>"))
        self.btn_save_final_to_file.setText(_translate("MainWindow", "Save Thing and Item to file"))
        self.cmb_oh_ips.setToolTip(_translate("MainWindow", "<html><head/><body><p>select the right OpenHab instance for REST API</p></body></html>"))
        self.cb_link_items.setText(_translate("MainWindow", "Link all items"))
        self.cb_create_items.setText(_translate("MainWindow", "Create items"))
        self.lbl_output.setText(_translate("MainWindow", "Thing"))
        self.lbl_output_2.setText(_translate("MainWindow", "Items"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "OH Object Output"))
        self.lbl_log_2.setText(_translate("MainWindow", "Log"))
        self.btn_clear_log.setText(_translate("MainWindow", "Clear Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Log"))
        self.lbl_last_log_txt.setText(_translate("MainWindow", "Last Log:"))
        self.menuTasmHAB.setTitle(_translate("MainWindow", "Menü"))
        self.menuLoad_Config.setTitle(_translate("MainWindow", "TasmoHab config"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.action_save_conf.setText(_translate("MainWindow", "Save Device Config"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
        self.actionLoad_conf.setText(_translate("MainWindow", "Load Config"))
        self.actionEdit_conf.setText(_translate("MainWindow", "Edit Config"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
