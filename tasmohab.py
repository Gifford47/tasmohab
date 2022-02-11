# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import subprocess
import traceback
import yaml
from collections import defaultdict
from datetime import datetime

import json
import dirtyjson
import requests
import urllib
import serial
import threading
import time
import configparser
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QTextBrowser, QLabel, QVBoxLayout, QWidget, \
    QGridLayout, QCheckBox, QLineEdit, QComboBox
from serial import Serial
from serial.tools.list_ports import comports

import breeze_resources         # import breeze style
import dev_config
import openhab
import tas_cmds
import tasmohabUI
import rules
import api

sys.path.append('./ohgen')                  # import ohgen folder
try:
    from ohgen import ohgen                 # for pyinstaller one-file option
except:
    import ohgen
import globals

ohgen_templates = []                        # templates for ohgen
config_name = 'tasmohab.cfg'                # contains config data

templates_path = 'ohgen/templates'         # templates path
std_yaml_config_file = 'template.yaml'             # standard template file

json_config_data = {}                       # data from YAML config file. later it holds all relevant data to generate a thing an item
json_dev_status = {}                        # all device data from device (http or serial)
json_tasmota_objects = {}                   # this object contains only (formatted) gpio data (name, value and possible sensor) coming from tasmota device


class TasmohabUI(QtWidgets.QMainWindow, tasmohabUI.Ui_MainWindow):

    def __init__(self, parent=None):
        super(TasmohabUI, self).__init__(parent)
        self.setupUi(self)
        self.config = configparser.ConfigParser()
        self.config_file_path = ''
        if os.path.isfile(config_name):                                                     # load app config file (*.cfg)
            self.load_tasmohab_config(c_file=config_name)
        else:
            self.load_tasmohab_config()

        self.http_url = ''
        self.http_err_msg = 'Connection error. Cannot login with credentials. Please check username and password.'
        self.last_communication_class = None

        self.tbl_columns = {'Active' :              0,
                             'GPIO' :               1,
                             'GPIO Value' :         2,
                             'Peripheral Name' :    3,
                             'Feature' :            4,
                             'Item Label' :         5,
                             'Item Type' :          6,
                             'Groups' :             7,
                             'Metadata' :           8,
                             'Tags' :               9,
                             'Icon' :               10}

        self.UI_threads = []  # list of queued ui-threads
        self.yaml_config_data = ''
        self.yaml_conf_file = ''
        for root, dirs, files in os.walk('./'+templates_path):                              # scan all template files (*.tpl) in dir
            for file in files:
                if file.endswith(".tpl"):
                    ohgen_templates.append(str(file.split('.')[0]))
        self.cmb_template.addItems(ohgen_templates)
        self.cmb_template.setCurrentIndex(1)

        self.dev_config_wind = DevConfigWindow  # create an instance

        # set ui elements
        self.txt_thing_file.setText(self.config[self.cmb_outp_format.currentText()]['Thing_Path'] + 'new_thing.things')
        self.txt_item_file.setText(self.config[self.cmb_outp_format.currentText()]['Item_Path'] + 'new_items.items')
        self.cmb_oh_ips.addItems(self.config[self.cmb_outp_format.currentText()]['Openhab_Instances'].split(','))

        # menubar
        self.actionInfo.triggered.connect(self.about)
        self.actionExit.triggered.connect(self.exit)
        self.actionLoad_conf.triggered.connect(self.load_tasmohab_config)
        self.actionEdit_conf.triggered.connect(self.edit_tasmohab_config)

        self.btn_serport_refr.clicked.connect(self.list_com_ports)                          # Remember to pass the definition/method (without '()'), not the return value!
        self.btn_load_object.clicked.connect(self.load_yaml_file_config)
        self.btn_save_config.clicked.connect(self.save_yaml_file_config)
        self.btn_get_serial.clicked.connect(self.get_data_on_serial)
        self.btn_get_http.clicked.connect(self.get_data_on_http)
        self.btn_dev_details.clicked.connect(self.show_device_details)
        self.btn_set_dev_conf.clicked.connect(self.show_device_config)
        self.btn_show_json_obj.clicked.connect(self.show_tasmota_gpios)
        self.btn_refr_obj_data.clicked.connect(self.update_json_config_data_from_ui)
        self.btn_show_json_config.clicked.connect(self.show_json_config)
        self.btn_gen_fin_objts.clicked.connect(self.gen_objects_from_file)
        self.btn_save_final_to_file.clicked.connect(self.save_final_obj_to_file)
        self.btn_clear_log.clicked.connect(self.clear_log)
        self.btn_edittmpl.clicked.connect(self.edit_template)
        self.btn_helpfullurls.clicked.connect(self.show_config_urls)
        self.btn_gen_rules.clicked.connect(self.show_rule_generator)
        self.btn_save_final_via_rest.clicked.connect(self.save_final_obj_via_rest)
        self.cb_sel_all.stateChanged.connect(self.sel_all_checkboxes)
        
        self.txt_pass.returnPressed.connect(self.get_data_on_http)

    def load_tasmohab_config(self, c_file=None):
        """Reads tasmohab config file (*.cfg)"""
        if c_file is bool(c_file) or c_file is None:                     # if file is None, no existing file
            if bool(self.config.sections()) == False:                    # if config file is empty
                QMessageBox.warning(self,'No config file loaded!', 'Please make sure, that a "tasmohab.cfg" exists and is loaded!')
            c_file = QFileDialog.getOpenFileName(filter="Config(*.cfg)")[0]
            if not c_file == '':
                self.config_file_path = c_file
                self.config.read(c_file)
                self.cmb_outp_format.clear()
                self.cmb_outp_format.addItems(self.config.sections())
                self.cmb_oh_ips.clear()
                self.cmb_oh_ips.addItems(self.config[self.cmb_outp_format.currentText()]['Openhab_Instances'].split(','))

                self.append_to_log('Config file loaded:' + str(c_file))
            else:
                if bool(self.config.sections()) == False:
                    sys.exit()
        else:
            try:
                self.config_file_path = c_file
                self.config.read(c_file)
                self.cmb_outp_format.clear()
                self.cmb_outp_format.addItems(self.config.sections())
                self.append_to_log('Config file loaded:' + str(c_file))
            except Exception as e:
                self.append_to_log('Config file corrupted:' + str(c_file))
                self.report_error()

    def edit_tasmohab_config(self):
        #file_path = os.path.abspath(str(os.getcwd()) + '/' + config_name)
        if os.path.isfile(self.config_file_path):
            p = subprocess.Popen([self.config_file_path], shell=True)
            #p.wait()

    def clear_log(self):
        """Clears all log entries"""
        self.txt_log.clear()

    @staticmethod
    def report_error(error=None):
        if error is not None:
            print(error)
        traceback.print_exc(limit=2, file=sys.stdout)

    @staticmethod
    def is_json(data):
        try:
            json.loads(data)
        except ValueError as e:
            #self.report_error()                                                                # optional
            return False
        return True

    def read_yaml(self, filepath):
        with open(filepath, encoding='utf8') as file:
            # The FullLoader parameter handles the convert from YAML
            # scalar values to Python the dictionary format
            tmp = yaml.safe_load(file)
            return tmp

    def write_yaml(self, dict):
        filepath = QFileDialog.getSaveFileName(self, 'Save File', filter="YAML(*.yaml)")[0]
        try:
            with open(filepath, 'w') as file:
                yaml.dump(dict, file, sort_keys=False)
        except Exception as e:
            self.report_error()
        self.append_to_log("Config file saved:" + str(filepath))

    def list_com_ports(self):
        # adding list of items to combo box
        self.cmb_ports.clear()
        ports = [comport.device for comport in serial.tools.list_ports.comports()]
        self.append_to_log('Refreshing ports list:' + str(ports))
        if not ports:                                                                           # if list is empty
            self.btn_get_serial.setEnabled(False)
        else:
            ports.sort()
            self.btn_get_serial.setEnabled(True)
            self.cmb_ports.addItems(ports)

    def append_to_log(self, text):
        self.txt_log.append(datetime.today().strftime('%d-%m-%Y %H:%M:%S') + '\t' + str(text))  # '\t' = tab space
        self.lbl_last_log.setText(datetime.today().strftime('%d-%m-%Y %H:%M:%S') + '\t' + str(text))

    def save_yaml_file_config(self):
        """Save 'json_config_data' to a YAML file."""
        if bool(json_config_data):  # if json_config_data is not empty
            json_config_data['settings']['outputs']['default-output']['things-file'] = self.txt_thing_file.text()
            json_config_data['settings']['outputs']['default-output']['items-file'] = self.txt_item_file.text()

            self.update_yaml_to_json_config_data()                                              # update the internal yaml data
            if os.path.isfile(self.txt_config_file_path.text()):
                buttonReply = QMessageBox.question(self, 'Confirm overwrite',
                                                   "File '" + self.txt_config_file_path.text() + "' exists. Overwrite?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    with open(self.txt_config_file_path.text(), 'w') as file:
                        yaml.dump(yaml.safe_load(self.yaml_config_data), file, sort_keys=False)
                    self.append_to_log("Config file saved:" + self.txt_config_file_path.text())
                else:  # if no ...
                    self.write_yaml(yaml.safe_load(self.yaml_config_data))
            else:
                self.write_yaml(yaml.safe_load(self.yaml_config_data))
        else:
            # noinspection PyTypeChecker
            QMessageBox.information(self, 'Information', 'Please load a object config file first!', QMessageBox.Ok,
                                    QMessageBox.Ok)

    def datathread_dev_data(self, data):
        """Copy data from thread from the device into 'json_dev_status' and update the ui widgets."""
        global json_dev_status
        json_dev_status = data.copy()
        self.thing_id = json_dev_status[tas_cmds.status['network']]['StatusNET']['Hostname']           # set the global thingid
        self.thing_id = str(self.thing_id).replace('-', '_')
        self.update_ui_device_info()
        self.clear_ui_widgets()
        try:
            self.create_tasmota_objects()
            self.add_ui_widgets()
        except Exception as e:
            self.report_error()
            self.append_to_log('Failure when creating tasmota objects:'+str(e))

    def datathread_on_error(self, data, notification=False):
        self.append_to_log(str(data))
        if notification:
            QMessageBox.warning(self, 'Warning', str(data))

    def datathread_finish(self):
        self.btn_get_serial.setEnabled(True)
        self.btn_serport_refr.setEnabled(True)
        self.btn_get_http.setEnabled(True)
        if len(self.UI_threads) > 0:                                                        # if found more than 0 elements
            self.UI_threads[0].exit()                                                       # get first element (thread) of list und exit the thread
            del self.UI_threads[0]                                                          # delet first element (thread) of list (alternate; self.UI_threads.remove(self.get_ser_dev_info))
        self.start_queued_threads()

    def update_progressbar(self, data):
        self.progressBar.setValue(data)

    def get_data_on_serial(self):
        """Start a new thread and:\n
        - send every cmd in 'self.cmd' to the device and save the result in 'json_dev_status'
        - update the progressbar
        - update the self.last_communication_class for future connections"""
        self.btn_get_serial.setEnabled(False)
        self.btn_serport_refr.setEnabled(False)
        self.btn_get_http.setEnabled(False)                                                 # dont allow http commands
        global json_dev_status
        self.cmd = []  # for status
        for key, value in tas_cmds.status.items():
            self.cmd.append(value)

        self.get_ser_dev_info = SerialDataThread(self.cmd, self.cmb_ports.currentText(), self.cmb_baud.currentText())
        self.get_ser_dev_info.pyqt_signal_json_out.connect(self.datathread_dev_data)        # 2nd argument is the returned data!!!
        self.get_ser_dev_info.pyqt_signal_error.connect(self.datathread_on_error)           # 2nd argument is the returned data!!!
        self.get_ser_dev_info.finished.connect(self.datathread_finish)
        self.get_ser_dev_info.pyqt_signal_progress.connect(self.update_progressbar)
        self.UI_threads.append(self.get_ser_dev_info)  # appent to list of queued ui-threads

        self.last_communication_class = self.get_ser_dev_info                           # if we want to use the last class to communicate with the device
        self.start_queued_threads()  # start queued threads

    def start_queued_threads(self):  # DON`T FORGET TO EXIT THE THREAD AFTER FINISH!!!
        """Start new thread after last last thread is finished."""
        print('Queued pyqt UI-Threads:' + str(len(self.UI_threads)))
        self.append_to_log('Queued pyqt UI-Threads:' + str(len(self.UI_threads)))
        if len(self.UI_threads) > 0:  # if found more than 0 elements
            self.UI_threads[0].start()  # get first element (thread) of list and start it. DON`T FORGET TO EXIT THE THREAD AFTER FINISH!!!

    def get_data_on_http(self):
        """Start a new thread and:\n
        - look if the device is reachable
        - send every cmd in 'self.cmd' to the device and save the result in 'json_dev_status'
        - update the progressbar
        - update the self.last_communication_class for future connections"""
        global json_dev_status
        if (self.txt_user.text() == "" and self.txt_pass.text() == ""):
            self.http_url = 'http://' + self.txt_ip.text() + '/cm?cmnd='
        else:
            self.http_url = 'http://' + self.txt_ip.text() + '/cm?user=' + self.txt_user.text() + '&password=' + self.txt_pass.text() + '&cmnd='
        try:
            resp_code = requests.get(self.http_url, timeout=.5).status_code
        except Exception:
            self.report_error()
            self.append_to_log(self.http_err_msg)
            QMessageBox.warning(self, 'Connection Error', self.http_err_msg)
            return
        if resp_code != 200:
            self.append_to_log(self.http_err_msg)
            QMessageBox.warning(self, 'Connection Error', self.http_err_msg)
            return

        self.cmd = []  # for status cmd
        for key, value in tas_cmds.status.items():
            self.cmd.append(value)
        self.get_http_dev_info = HttpDataThread(self.cmd, self.http_url, self.txt_ip.text())
        self.get_http_dev_info.pyqt_signal_json_out.connect(self.datathread_dev_data)       # 2nd argument is the returned data!!!
        self.get_http_dev_info.pyqt_signal_error.connect(self.datathread_on_error)          # 2nd argument is the returned data!!!
        self.get_http_dev_info.finished.connect(self.datathread_finish)
        self.get_http_dev_info.pyqt_signal_progress.connect(self.update_progressbar)
        self.UI_threads.append(self.get_http_dev_info)                                      # appent to list of queued ui-threads

        self.last_communication_class = self.get_http_dev_info                               # if we want to use the last class to communicate with the device
        self.start_queued_threads()  # start queued threads

    def update_ui_device_info(self):
        """Update the device status section in the ui with current values."""
        global json_dev_status
        if not bool(json_dev_status):                                                       # if json is empty
            self.lbl_dev_hostname.setText("")
            self.lbl_dev_firmware.setText("")
            self.lbl_dev_name.setText("")
            self.lbl_dev_module.setText("")
            self.btn_refr_obj_data.setEnabled(False)
        elif json_dev_status is not None and bool(json_dev_status):                         # if json is not None and not empty
            try:
                self.lbl_dev_hostname.setText(str(json_dev_status[tas_cmds.status['network']]['StatusNET']['Hostname']))
                self.lbl_dev_firmware.setText(str(json_dev_status[tas_cmds.status['fw']]['StatusFWR']['Version']))
                self.lbl_dev_name.setText(str(json_dev_status[tas_cmds.status['state']]['Status']['DeviceName']))
                self.lbl_dev_module.setText(str(json_dev_status[tas_cmds.status['state']]['Status']['Module'])+' ('+str(json_dev_status[tas_cmds.status['template']]['NAME'])+')')
                if self.config['DEFAULT']['UpdateFileName'] != 'False':
                    # replace the old filename from things and items file with the new devicename:
                    conf_filename = self.config['DEFAULT']['UpdateFileName']
                    new_itemfilename = str(self.txt_item_file.text()).replace(os.path.basename(self.txt_item_file.text()), str(json_dev_status[tas_cmds.status['state']]['Status'][conf_filename])+'.items')
                    new_thingfilename = str(self.txt_thing_file.text()).replace(os.path.basename(self.txt_thing_file.text()), str(json_dev_status[tas_cmds.status['state']]['Status'][conf_filename])+'.things')
                    self.txt_item_file.setText(new_itemfilename)
                    self.txt_thing_file.setText(new_thingfilename)
            except Exception:
                self.report_error()
            #if json_config_data is not None and bool(json_config_data):
            self.btn_set_dev_conf.setEnabled(True)
            self.btn_gen_rules.setEnabled(True)

    def clear_ui_widgets(self):                                                          # removes all objects from scrollarea
        """Clears the scrollarea with all widget in it."""
        try:
            for i in reversed(range(self.objects_grid.count())):
                self.objects_grid.takeAt(i).widget().deleteLater()                          # delete all last widgets
        except Exception as e:
            pass

    def load_yaml_file_config(self, std_file=''):
        """Load a yaml file, that contains a configuration for a device or a template.
        The data of this file is stored in 'json_config_data'."""
        try:
            global json_config_data
            if os.path.isfile(std_file):
                self.yaml_conf_file = std_file
                self.txt_config_file_path.setText(std_file)
                json_config_data = self.read_yaml(std_file)
            else:
                self.yaml_conf_file = QFileDialog.getOpenFileName(filter="YAML(*.yaml)")[0]
                if not self.yaml_conf_file == '':
                    self.txt_config_file_path.setText(self.yaml_conf_file)
                    json_config_data = self.read_yaml(self.yaml_conf_file)
                else:
                    return
            if 'settings' in json_config_data:
                self.txt_thing_file.setText(json_config_data['settings']['outputs']['default-output']['things-file'])
                self.txt_item_file.setText(json_config_data['settings']['outputs']['default-output']['items-file'])
                self.tabWidget.setCurrentIndex(2)  # jump to final tab
            else:
                self.append_to_log('Corrupt YAML file loaded! Exiting here!')
                QMessageBox.warning(self, 'Corrupt template file', 'Corrupt YAML file loaded! Try another one.')
                self.tabWidget.setCurrentIndex(0)
                return
            self.update_json_to_yaml_config_data()
            self.update_ui_device_info()
            self.gen_fin_objects()
            self.btn_gen_fin_objts.setEnabled(True)
            self.btn_save_final_to_file.setEnabled(True)
            self.btn_save_final_via_rest.setEnabled(True)
        except Exception:
            self.report_error()

    def show_device_details(self):
        self.det_window = DetailWindow(json_dev_status)                 # initialize 2. windows for dev details
        self.det_window.show()

    def show_device_config(self):
        self.dev_config_wind = DevConfigWindow(self)                    # pass the current class object to modify its objects
        self.dev_config_wind.show()

    def show_rule_generator(self):
        self.dev_rules = rules.Rule_Gen(self)                    # pass the current class object to modify its objects
        self.dev_rules.show()

    def create_tasmota_objects(self):
        """Create a dict 'json_tasmota_objects' and copy the gpio configuration from device into it.
        The Template cmd is used to get all gpios from the device."""
        global json_tasmota_objects

        if bool(json_dev_status) == False:
            return
        # read every tasmota gpio and set object dict
        json_tasmota_objects = {}
        if '8266' in  str(json_dev_status[tas_cmds.status['fw']]['StatusFWR']['Hardware']).lower():     # for esp8266ex
            gpio_no_list = [0, 1, 2, 3, 4, 5, 9, 10, 12, 13, 14, 15, 16, 17]        # see https://tasmota.github.io/docs/Templates/#gpio
        else:                                                                       # for ESP32
            gpio_no_list = [0, 1, 2, 3, 4, 5, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]        # see https://tasmota.github.io/docs/Templates/#gpio
        for i, val in enumerate(gpio_no_list):
            gpio_no_list[i] = 'GPIO'+str(val)                                         # add 'GPIO' before every value/ reformat List
        gpios_template = json_dev_status[tas_cmds.status['template']]['GPIO']                # get all the gpios from the template cmd
        gpio_dict_template = dict(zip(gpio_no_list, gpios_template))                                  # create a dict with gpios as key and its values with gpio-no coming 'from json_dev_status[tas_cmds.status['template']]['GPIO']'
        gpio_dict_user = {}                                                         # create a new dict for user gpios
        for gpio, val in json_dev_status[tas_cmds.status['user_gpio']].items():
            #gpio = re.findall(r'\d+', gpio)                                         # get only numbers from string (GPIO5->5)
            try:
                gpio_dict_user[gpio] = int(list(val.keys())[0])
            except Exception:
                pass
            #gpio_dict_user.update({gpio:list(val.keys())[0]})                       # save every gpio with its first value (peripheral number) to dict. i.e.: {2:35} ...
        gpio_dict_merged = {}
        gpio_dict_merged.update(gpio_dict_template)                                 # update the existing dict with the template dict
        gpio_dict_merged.update(gpio_dict_user)                                     # update the existing dict with the user dict
        json_tasmota_objects = gpio_dict_merged.copy()                              # copy gpio_dict_merged into json_tasmota_objects

    def add_ui_headers(self):
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 207))
        self.objects_grid = QGridLayout(self.scrollAreaWidgetContents)
        # generate the headlines
        for name, col in self.tbl_columns.items():
            myFont = QtGui.QFont()
            myFont.setBold(True)
            label = QLabel(name)
            label.setFont(myFont)
            self.objects_grid.addWidget(label, 0, col)        # Adds a widget at specified row and column

    def add_ui_widgets(self):
        global json_tasmota_objects
        if bool(json_tasmota_objects) == False:                 # if empty, leave return
            return
        self.add_ui_headers()
        # creating UI Widgets:
        # iter items for every single widget
        row = 1  # row
        for gpio, peripheral_no in json_tasmota_objects.items():
            # now the first four coloums will be filled:
            peripheral = self.get_peripheral_name_by_no(peripheral_no)
            cb = QCheckBox()
            if peripheral_no not in [1,0]:              # peripheral 1='User', 0='Mone'
                cb.setChecked(True)
            else:
                cb.setChecked(False)
            self.objects_grid.addWidget(cb, row, self.tbl_columns['Active'])                    # Adds a widget (checkbox) at specified row and column
            self.objects_grid.addWidget(QLabel(gpio), row, self.tbl_columns['GPIO'])                                   # add the gpio label
            self.objects_grid.addWidget(QLabel(str(peripheral_no)), row, self.tbl_columns['GPIO Value'])  # add the gpio value(s)
            # print all gpios and their peripheral name and number
            self.add_ui_widget_peripheral(peripheral, row)  # add the peripheral name/ sensor name
            if peripheral_no not in [0,1]:              # peripheral number 1='User', 2='None'
                self.add_ui_widgets_user(self.objects_grid, row, peripheral,peripheral_no=peripheral_no)
            row += 1  # next line

        # all gpios and actuators were added, but not sensors (i.e I2C),
        # these sensors will be added in the following
        myFont = QtGui.QFont()
        myFont.setBold(True)
        label = QLabel('Sensors:')
        label.setFont(myFont)
        self.objects_grid.addWidget(label, row, 0)  # add Header for additional sensors
        row += 1
        col_subsensor = self.tbl_columns['GPIO']                                             # adds the checkbox for the sensor, but in the next coloumn
        for sensorname, value in json_dev_status[tas_cmds.status['sensor']]['StatusSNS'].items():
            if isinstance(json_dev_status[tas_cmds.status['sensor']]['StatusSNS'][sensorname], dict):                    # if sensor has a following dict
                # Sensor is a multisensor with multiple sensors
                # create an item for every row:
                cb = QCheckBox()
                cb.setChecked(True)
                self.objects_grid.addWidget(cb, row, self.tbl_columns['Active'])                             # add the checkbox for the sensor
                self.add_ui_widget_peripheral(sensorname, row)
                row += 1
                for sensor, value in json_dev_status[tas_cmds.status['sensor']]['StatusSNS'][sensorname].items():        # iter over items
                    # add the checkbox for the sensor, but in the next coloumn
                    self.add_ui_widgets_sensor_single_line(self.objects_grid, row, sensor, value, col_cb=self.tbl_columns['GPIO'], peripheral_name=sensorname)
                    row += 1
            # sensor is a single sensor with one value
            else:
                self.add_ui_widget_peripheral(sensorname, row)
                self.add_ui_widgets_sensor_single_line(self.objects_grid, row, sensorname, value, col_cb=0)
                row += 1
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btn_refr_obj_data.setEnabled(True)

    def add_ui_widget_peripheral(self, name, row):
        lbl = QLabel(name)
        self.objects_grid.addWidget(lbl, row, self.tbl_columns['Peripheral Name'])  # add the peripheral name/ sensor name

    def add_ui_widgets_user(self, layout, row, peripheral, peripheral_no='default'):
        try:
            line = QLineEdit(openhab.std_items[peripheral_no]['feature'])                    # feature
        except:
            line = QLineEdit(openhab.std_items['default']['feature'])                           # else: return default value
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, self.tbl_columns['Feature'])
        line = QLineEdit(peripheral)                                                         # item label
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, self.tbl_columns['Item Label'])
        cb = QComboBox()                                                                # item type
        cb.addItems(openhab.item_types)
        try:
            cb.setCurrentIndex(openhab.std_items[peripheral_no]['std_type'])
        except:
            cb.setCurrentIndex(openhab.item_types.index('number'))  # if index is not found
        layout.addWidget(cb, row, self.tbl_columns['Item Type'])
        line = QLineEdit(self.thing_id)                                              # item group
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, self.tbl_columns['Groups'])
        try:
            line = QLineEdit(openhab.std_items[peripheral_no]['meta'])                      # metadata
        except:
            line = QLineEdit(openhab.std_items['default']['meta'])
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, self.tbl_columns['Metadata'])
        try:
            line = QLineEdit(openhab.std_items[peripheral_no]['tags'])                      # tags
        except:
            line = QLineEdit(openhab.std_items['default']['tags'])
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, self.tbl_columns['Tags'])
        try:
            line = QLineEdit(openhab.std_items[peripheral_no]['icon'])                      # icon
        except:
            line = QLineEdit(openhab.std_items['default']['icon'])
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, self.tbl_columns['Icon'])

    # a single sensor will be shown in the ui in the following
    def add_ui_widgets_sensor_single_line(self, layout, row, sensor, value, col_cb=None, peripheral_name=None):
        col_checkb = self.tbl_columns['Active']
        if col_cb is not None:
            col_checkb = col_cb
        cb = QCheckBox()
        cb.setChecked(True)
        layout.addWidget(cb, row, col_checkb)                                                   # add the checkbox for the sensor
        layout.addWidget(QLabel(sensor+':'+str(value)), row, self.tbl_columns['GPIO Value'])
        line = QLabel(sensor)
        layout.addWidget(line, row, self.tbl_columns['Peripheral Name'])                                                      # add sensor name
        # if peripheral_name was submitted, get the peripheral_number, else use default values
        if peripheral_name != None:
            peripheral_no = self.get_peripheral_no_by_name(peripheral_name)
        self.add_ui_widgets_user(layout, row, sensor, peripheral_no=sensor)
        row += 1

    def get_peripheral_no_by_name(self, name):                                              # try to find the appropriate peripheral number from list
        peripheral_no = 'default'
        try:                                                                                # try to find the appropriate peripheral number from list
            for per_no, _dict in openhab.std_items.items():
                for key, val in _dict.items():
                    if key == 'name' and val.lower() == str(name).lower():
                        peripheral_no = per_no
                        break                                                               # Break the inner loop...
                else:
                    continue                                                                # Continue if the inner loop wasn't broken.
                break                                                                       # Inner loop was broken, break the outer.
        except Exception:
            pass
        return peripheral_no

    def get_peripheral_name_by_no(self, peripheral_no):
        peripheral_no = str(peripheral_no)
        if peripheral_no in openhab.std_items:
            return openhab.std_items[peripheral_no]['name']
        else:
            return None

    def update_json_to_yaml_config_data(self):
        global json_config_data
        self.yaml_config_data = yaml.dump(json_config_data, sort_keys=False)                      # yaml.load(f.read(), Loader=yaml.BaseLoader)
        self.config_txtbrowser.setText(self.yaml_config_data)
        self.append_to_log('YAML config object updated!')

    def update_yaml_to_json_config_data(self):  # if textbrowser is updated manually, json config needs to be updated!
        global json_config_data
        self.yaml_config_data = self.config_txtbrowser.toPlainText()
        json_config_data = yaml.safe_load(self.yaml_config_data)            # yaml_object will be a list or a dict
        self.append_to_log('JSON config object updated!')

    def show_tasmota_gpios(self):
        self.det_window = DetailWindow(json_tasmota_objects)                # initialize 2. windows for object details
        self.det_window.show()

    def show_json_config(self):
        global json_config_data
        self.update_yaml_to_json_config_data()
        self.det_window = DetailWindow(json_config_data)                    # initialize 2. windows for object details
        self.det_window.show()

    # configure the 'settings' header in json_config_data
    def set_config_settings(self):
        '''
        configure the 'settings' header in json_config_data
        '''
        global json_config_data
        # the following sets the default values of the dict
        json_config_data.setdefault('settings',{})
        json_config_data['settings'].setdefault('header', '')
        json_config_data['settings'].setdefault('output', 'default-output')
        json_config_data['settings'].setdefault('hostname', '')
        json_config_data['settings'].setdefault('ip', '')
        json_config_data['settings'].setdefault('friendlyname', '')
        json_config_data['settings'].setdefault('deviceName', '')
        json_config_data['settings'].setdefault('topic', '')
        json_config_data['settings'].update({'outputs':{'default-output':{'items-file':''}}})
        json_config_data['settings'].update({'outputs': {'default-output': {'things-file':''}}})
        try:  # add here things, that comes from device data...
            json_config_data['settings']['hostname'] = self.thing_id        # json_tasmota_objects could not be initiated
            json_config_data['settings']['friendlyname'] = json_dev_status[tas_cmds.status['state']]['Status']['FriendlyName'][0]
            json_config_data['settings']['deviceName'] = json_dev_status[tas_cmds.status['state']]['Status']['DeviceName']
            json_config_data['settings']['topic'] = json_dev_status[tas_cmds.status['state']]['Status']['Topic']
            json_config_data['settings']['ip'] = json_dev_status[tas_cmds.status['network']]['StatusNET']['IPAddress']
        except Exception as e:
            pass
        json_config_data['settings']['outputs']['default-output']['items-file'] = self.txt_item_file.text()  # item file
        json_config_data['settings']['outputs']['default-output']['things-file'] = self.txt_thing_file.text()  # thing file
        self.append_to_log('JSON config settings updated!')
        return True

    def update_json_config_data_from_ui(self):
        """Update the json configuration here in relation to the user configurations for the tasmota objects
        all entries from tasmota objects in the ui are read in and stored in the 'json_config_data'.
        Then the 'json_config_data' is taken to create the things and items."""
        global json_config_data
        json_config_data.clear()                                                                    # clear all existing data
        if self.set_config_settings():
            #self.thing_id = json_config_data['settings']['hostname']
            #self.thing_id = str(self.thing_id).replace('-', '_')
            json_config_data[self.thing_id] = {}                                                    # create a new thing entry
            json_config_data[self.thing_id]['thingid'] = self.thing_id                              # generate thingid
            json_config_data[self.thing_id]['label'] = json_config_data['settings']['deviceName']   # generate thing label
            json_config_data[self.thing_id]['template'] = str(self.cmb_template.currentText())      # qcombobox
            json_config_data[self.thing_id]['topic'] = json_config_data['settings']['topic']
            json_config_data[self.thing_id]['location'] = self.txt_location.text()
            json_config_data[self.thing_id]['ip'] = json_config_data['settings']['ip']

            self.read_items_from_ui()                                       # updates
            json_config_data[self.thing_id].update(self.items_dict)         # write new items to dict

            self.update_json_to_yaml_config_data()                          # update yaml from json
            self.tabWidget.setCurrentIndex(2)                               # jump to tabwidget Index=2
            self.gen_fin_objects()                                          # generate objects
            self.btn_gen_fin_objts.setEnabled(True)
            self.btn_save_final_to_file.setEnabled(True)
            self.btn_save_final_via_rest.setEnabled(True)

    def read_items_from_ui(self):
        """
        Reads in every item in table and saves them in 'self.items_dict'.
        """
        self.items_dict = defaultdict(list)                                        # create a dict with list for each item
        self.items_dict.clear()                                                 # clear old content
        row = 1
        col = 0
        tot_rows = self.objects_grid.rowCount()
        while row < tot_rows:  # loop through all rows
            try:
                item = self.objects_grid.itemAtPosition(row, col)                                                       # get first item: the sensor, i.e. AM2301
                if type(item.widget()) == QCheckBox and item.widget().isChecked():                              # if gpio checkbox is checked
                    item_name = str(self.objects_grid.itemAtPosition(row, self.tbl_columns['Peripheral Name']).widget().text()).replace(' ','_')    # f.e.: the sensor name. replace space with underline
                    ###################### Check if sensor or actuator ######################
                    # if the next line is a QCheckbox: create a new item in last thing
                    # if the next line in next coloumn is a QCheckbox: create a new sensoritem
                    try:
                        next_item = self.objects_grid.itemAtPosition(row+1, self.tbl_columns['GPIO']).widget()                   # get item at next row and col
                    except:
                        next_item = None
                    #print("item:"+item_name)
                    if next_item is not None and type(next_item) == QCheckBox:
                        # i am a sensor: read the sensor and fill the dict
                        row += 1                                                                                # next line
                        while (type(next_item) == QCheckBox):
                            if next_item.isChecked():                                                           # get the sensor checkbox (not the gpio checkbox!)
                                self.read_ui_widgets_user_by_row(row)                                             # read item in row and col
                                self.update_item_by_name(item_name)                                             # add/update item in dict
                                print("Added sub-sensor:" + item_name + "from line:" + str(row))
                            row += 1
                            try:
                                next_item = self.objects_grid.itemAtPosition(row, self.tbl_columns['GPIO']).widget()             # try to get the next checkbox
                            except:
                                next_item = None
                    else:                                                                                       # this line has no item and is a actuator
                        # i am a single sensor (one line in ui) or a actuator: read in and fill the dict
                        self.read_ui_widgets_user_by_row(row)                                                 # read item in row and col
                        self.update_item_by_name(item_name)                                                 # add/ update item in dict
                        print("Added sensor:"+item_name+" from line:"+str(row))
                        row += 1
                    ###################### END ######################
                else:
                    row += 1                                                                                # next line, last was unchecked
            except Exception as e:
                # line is empty or has no widget at row, col
                self.report_error()                                                                        # optional
                row += 1

    def read_ui_widgets_user_by_row(self, row):
        self.item_feature = self.objects_grid.itemAtPosition(row, self.tbl_columns['Feature']).widget().text()                      # qlineedit
        self.item_label = self.objects_grid.itemAtPosition(row, self.tbl_columns['Item Label']).widget().text()                        # qlineedit
        self.item_type = self.objects_grid.itemAtPosition(row, self.tbl_columns['Item Type']).widget().currentText()                  # qcombobox
        self.item_groups = self.objects_grid.itemAtPosition(row, self.tbl_columns['Groups']).widget().text()                       # qlineedit
        self.item_meta = self.objects_grid.itemAtPosition(row, self.tbl_columns['Metadata']).widget().text()                         # qlineedit
        self.item_tags = self.objects_grid.itemAtPosition(row, self.tbl_columns['Tags']).widget().text()                         # qlineedit
        self.item_icon = self.objects_grid.itemAtPosition(row, self.tbl_columns['Icon']).widget().text()                        # qlineedit

    def update_item_by_name(self, item_name):
        self.item_feature = self.item_feature.split(',') if (self.item_feature != '') else []                             # returns a list (for jinja2 template)

        # use the following syntax only, when 'RawOutput' is False in config
        if self.config.getboolean('DEFAULT','RawOutput') == False:
            system = self.config[self.cmb_outp_format.currentText()]                                            # choose smart home system

            self.item_label = str(system['PrefixLabel']+self.item_label+system['SuffixLabel']).replace("'", '') if (self.item_label!='') else ''
            self.item_groups = str(system['PrefixGroups']+self.item_groups+system['SuffixGroups']).replace("'", '') if (self.item_groups!='') else ''
            self.item_meta = str(system['PrefixMeta']+self.item_meta+system['SuffixMeta']).replace("'", '') if (self.item_meta!='') else ''
            self.item_tags = str(system['PrefixTags'] + self.item_tags + system['SuffixTags']).replace("'", '') if (self.item_tags != '') else ''
            if self.config.getboolean(self.cmb_outp_format.currentText(), 'TagsList') == True:
                self.item_tags = json.dumps(self.item_tags.split(',')) if (self.item_tags!='') else ''
            self.item_icon = str(system['PrefixIcons']+self.item_icon+system['SuffixIcons']).replace("'",'') if (self.item_icon!='') else ''

        self.items_dict[self.item_type].append({'name': item_name,
                                      'label': self.item_label,
                                      'groups': self.item_groups,
                                      'features': self.item_feature,                                         # returns a list (for jinja2 template)
                                      'metadata': self.item_meta,
                                      'tags': self.item_tags,
                                      'icon':self.item_icon}
                                     )

    def gen_objects_from_file(self):
        self.gen_fin_objects()
        self.tabWidget.setCurrentIndex(2)

    def gen_fin_objects(self):
        self.txt_output_thing.clear()  # clear the textbrowser
        self.txt_output_item.clear()  # clear the textbrowser
        self.update_yaml_to_json_config_data()
        try:
            devices_file_name = self.yaml_conf_file
            globals.init_jinja_environment(self.yaml_conf_file)  # init global jinja_environment

            data = json_config_data.copy()  # copy json_config_data to new data var (because 'settings' section was deleted before
            if not data:
                ohgen.warn("No data found in {}".format(devices_file_name))
                del data  # del data to avoid duplicates
                return
            ohgen.templates.clear()                                                 # clear templates, if template file has changed
            ohgen.settings = data.pop('settings', {})  # remove (pop) settings section from data

            # load jinja environment, set the loader path to dir(devices_file_name) + /templates
            globals.jinja_environment.filters.update(
                {'csv': ohgen.csv, 'groups': ohgen.openhab_groups, 'tags': ohgen.openhab_tags,
                 'metadata': ohgen.openhab_metadata, 'quote': ohgen.quote})

            # load all the yaml data first and generate each thing
            for name, thing in data.items():
                thing.setdefault('name', name)
                # fill in some useful variables
                thing.setdefault('label', ohgen.split_camel_case(name.replace("_", " ")))
                thing.setdefault('thingid', name.replace("_", "-").lower())
                thing.setdefault('name_parts', name.split("_"))
                thing.setdefault('room', ohgen.split_camel_case(name.split("_")[0]))

                output = ohgen.generate(name, thing)
                if output:
                    ohgen.add_thing_to_buffer(thing, output['things'], output['items'])
                elif output is None:
                    self.append_to_log('Error while generating things and items output. Please inspect template file and/or debug!')
            # print(ohgen.settings, ohgen.output_buffer)
            print("Devices: {}".format(len(data)))

            # write to textbrowser:
            for output_name in ohgen.output_buffer:
                for part in ohgen.output_buffer[output_name]:
                    headers = part + "-header"
                    footers = part + "-footer"
                    # write global headers
                    if part == 'things-file':
                        if 'header' in ohgen.settings:
                            self.txt_output_thing.append(ohgen.settings['header'])
                        # write output specific headers
                        if headers in ohgen.settings['outputs'][output_name]:
                            self.txt_output_thing.append(ohgen.settings['outputs'][output_name][headers])
                        # write the generated content
                        self.txt_output_thing.append("\n\n".join(ohgen.output_buffer[output_name][part]))
                        # write output specific footers
                        if footers in ohgen.settings['outputs'][output_name]:
                            self.txt_output_thing.append(ohgen.settings['outputs'][output_name][footers])
                        # write global footers
                        if 'footer' in ohgen.settings:
                            self.txt_output_thing.append(ohgen.settings['footer'])
                    if part == 'items-file':
                        if 'header' in ohgen.settings:
                            self.txt_output_item.append(ohgen.settings['header'])
                        # write output specific headers
                        if headers in ohgen.settings['outputs'][output_name]:
                            self.txt_output_item.append(ohgen.settings['outputs'][output_name][headers])
                        # write the generated content
                        self.txt_output_item.append("\n\n".join(ohgen.output_buffer[output_name][part]))
                        # write output specific footers
                        if footers in ohgen.settings['outputs'][output_name]:
                            self.txt_output_item.append(ohgen.settings['outputs'][output_name][footers])
                        # write global footers
                        if 'footer' in ohgen.settings:
                            self.txt_output_item.append(ohgen.settings['footer'])
            # print(json_config_data)
            # print(ohgen.output_buffer)
            ohgen.output_buffer.clear()  # clear data to avoid duplicates
            del data  # del data to avoid duplicates
            cur_index = self.tabWidget.currentIndex()
        except Exception as e:
            self.report_error()

    def save_final_obj_to_file(self):
        thing_file = self.txt_thing_file.text()
        item_file = self.txt_item_file.text()
        if os.path.isfile(thing_file) or os.path.isfile(item_file):
            # noinspection PyTypeChecker
            buttonReply = QMessageBox.question(self, 'Confirm overwrite',
                                               'Openhab Files exists.\nShould i overwrite?',
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.write_oh_files(thing_file)
                self.write_oh_files(item_file)
                self.append_to_log('Openhab Files updated!')
        else:
            self.write_oh_files(thing_file)
            self.write_oh_files(item_file)
            self.append_to_log('Openhab Files created!')

    def write_oh_files(self, file_path):
        try:
            file_path = os.path.abspath(file_path)  # get absolute filepath
            os.makedirs(os.path.dirname(file_path), exist_ok=True)  # make dirs, if not exists
            if '.things' in file_path:
                with open(file_path, 'w') as file:
                    file.write(self.txt_output_thing.toPlainText())
            if '.items' in file_path:
                with open(file_path, 'w') as file:
                    file.write(self.txt_output_item.toPlainText())
        except Exception as e:
            self.report_error()

    def about(self):
        self.det_window = DetailWindow('A Tasmota object configurator for OpenHab. <p>Created by Gifford47<\p>', format_to_json=False)                 # initialize 2. window for dev details
        self.det_window.show()

    def exit(self):
        self.close()

    def edit_template(self):
        file_path = os.path.abspath(os.getcwd() + '/' + templates_path + '/' + self.cmb_template.currentText() + '.tpl')
        if os.path.isfile(file_path):
            p = subprocess.Popen([file_path], shell=True)
            #p.wait()

    def show_config_urls(self):
        urls = {}
        try:
            urls = json.loads(self.config[self.cmb_outp_format.currentText()]['URLs'])
        except Exception as e:
            self.report_error()
        formatted_urls = ''
        for name, url in urls.items():
            formatted_urls += '<P>' + name + ': <a href='+url+'>'+str(url)+'</a>' + '</P>'
        self.det_window = DetailWindow(formatted_urls, format_to_json=False)                 # initialize 2. window
        self.det_window.show()

    def save_final_obj_via_rest(self):
        self.btn_save_final_via_rest.setEnabled(False)
        api_user = self.config[self.cmb_outp_format.currentText()]['OpenHab_User']
        api_pass = self.config[self.cmb_outp_format.currentText()]['OpenHab_Pass']

        # thing
        thing_data = self.read_and_fix_json(self.txt_output_thing.toPlainText())
        if (thing_data == False):
            self.append_to_log('Template error: Thing is no valid json format, could not fix it!')
            self.btn_save_final_via_rest.setEnabled(True)
            return False
        item_links_as_list = self.get_rest_links_from_channels(thing_data)

        # items
        item_data = self.read_and_fix_json(self.txt_output_item.toPlainText())
        if (item_data == False):
            self.append_to_log('Template error: Items do not have a valid json format, could not fix it!')
            self.btn_save_final_via_rest.setEnabled(True)
            return False

        if (item_links_as_list == False):
            self.append_to_log('Template error: Links are not generated. Please do it manually!')

        ip = self.cmb_oh_ips.currentText()
        action = 'create'
        # create thing
        self.txt_output_thing.setText(json.dumps(thing_data, indent=4, sort_keys=True))
        response = api.handle_thing(ip, action, body=thing_data, user=api_user, passw=api_pass)
        self.append_to_log('Thing:'+response)
        # create items
        self.txt_output_item.setText(json.dumps(item_data, indent=4, sort_keys=True))
        response = api.handle_item(ip, action, body=item_data, user=api_user, passw=api_pass)
        self.append_to_log('Item:'+response)
        # create links to items
        for link in item_links_as_list:
            response = api.handle_link(ip, action, body=link, user=api_user, passw=api_pass)
            self.append_to_log('Links:'+response)

        self.btn_save_final_via_rest.setEnabled(True)

    def read_and_fix_json(self, json_str):
        data = ''
        if self.is_json(json_str):
            data = json.loads(json_str)
            return data
        else:
            self.append_to_log('Template error: Trying to fix broken json ...')
            try:
                data = dirtyjson.loads(json_str)                       # if template return a broken json, try to repair
            except Exception:
                return False
            if not self.is_json(json.dumps(data)):                                            # if still broken ...
                return False
            else:
                return data

    def get_rest_links_from_channels(self, data):
        links_list = []
        link_dict = {}
        try:
            for channel in data['channels']:                                # create dict for link
                link_dict['itemName'] = channel['linkedItems'][0]           # get first item of array
                link_dict['channelUID'] = channel['uid']
                link_dict['configuration'] = {}
                links_list.append(link_dict)
        except Exception:
            return False
        return links_list

    def sel_all_checkboxes(self):
        cbs = self.frame.findChildren(QCheckBox)  # returns a list of all QLineEdit objects
        if self.cb_sel_all.isChecked():
            for cb in cbs:
                cb.setChecked(True)
        else:
            for cb in cbs:
                cb.setChecked(False)

class SerialDataThread(QThread):
    pyqt_signal_json_out = pyqtSignal(dict)
    pyqt_signal_error = pyqtSignal(str)
    pyqt_signal_progress = pyqtSignal(int)

    def __init__(self, cmd_list, port, baud, timeout=.3):
        QThread.__init__(self)
        self.cmd_list = cmd_list
        self.port = port
        self.baud = baud
        self.timeout = timeout                  # read timeout for serialport to get a byte
        self.max_retries = 5                    # max retries for one cmd to get a response
        self.response_waiting = .01                 # no of sec (time diff) that MUST be waited for next cmd (awaiting more responses)

    def run(self):
        response_waiting_max = self.response_waiting + 2
        try:
            ser = Serial(str(self.port), str(self.baud), timeout=self.timeout)
        except Exception as e:
            self.pyqt_signal_error.emit('Exception in reading serial:' + str(e))
            print(e)
            return
        result = {}
        ui = TasmohabUI()
        try:
            if ser.is_open:
                time.sleep(.1)  # skip tasmota startup

                for no, cmd in enumerate(self.cmd_list):
                    #print('CMD:'+cmd)
                    retry = 0
                    while retry <= self.max_retries:
                        json_tmp = []
                        buffer = None
                        ser.reset_output_buffer()
                        ser.reset_input_buffer()
                        ser.write(str.encode(cmd + '\n'))
                        print('send:'+cmd)
                        ser.flush()                                                 # it is buffering. required to get the data out *now*
                        t1 = datetime.now()
                        while bool(buffer) == False:                                # if buffer is still empty (in case of large response time (reboot))
                            if (datetime.now()-t1).total_seconds() > response_waiting_max:
                                break                                               # leave first while, if response comes anymore
                            wait_time = self.response_waiting
                            if cmd.count(';') > 1:                                  # for long cmds (i.e. backlog) increase waiting time till response
                                wait_time = self.response_waiting * cmd.count(';') * 0.1
                            while ser.inWaiting() > 0 or (datetime.now()-t1).total_seconds() < wait_time:       # get into loop if serial>1 char or time is not ended
                                #msg = ser.read_until('\r\n').decode(encoding='utf-8')  # get serial response and encode (old)
                                buffer = ser.readline().decode(encoding='utf-8')                    # get response line by line
                                #print('buffer:'+buffer)
                                x = buffer[buffer.find('{'):buffer.find('\r\n')]
                                if TasmohabUI.is_json(x):
                                    json_tmp.append(x)                               # find json between string and add it to list
                                    json_tmp = list(filter(None, json_tmp))              # filter/delete empty elements
                                #print('json_tmp:'+str(json_tmp))
                                if bool(json_tmp) == False:                          # if json_tmp is still empty (no json received)
                                    buffer = None
                        #print(json_tmp)
                        tmp = {}
                        if bool(json_tmp):                                          # if (list) json_tmp is not empty
                            for resp in json_tmp:
                                #print(resp, bool(json_tmp), (TasmohabUI.is_json(resp)))
                                tmp.update(json.loads(resp))                        # save data in a temp var
                                self.pyqt_signal_progress.emit(round(100 / len(self.cmd_list) * (no + 1)))  # update progress
                        else:
                            retry += 1                                              # retry if not valid json
                            if retry >= self.max_retries:
                                self.pyqt_signal_error.emit('Could not get valid JSON data.')
                                print('Could not get valid JSON data.')
                                return  # leave the whole function
                            print('Non valid JSON response received, retrying ...')
                            self.pyqt_signal_error.emit('Non valid JSON response received, retrying ...')
                        result[cmd] = tmp
                        if bool(result[cmd]):                                       # if a response to the cmd exists
                            break                                                   # get out of while loop of cmds

                time.sleep(.1)
                ser.close()
            else:
                print('Serial Port error')
        except serial.SerialTimeoutException as e:
            print(e)
        except Exception as e:
            self.pyqt_signal_error.emit('Exception in reading serial:' + str(e))
            print(e)
        ser.close()
        self.pyqt_signal_json_out.emit(result)

class HttpDataThread(QThread):
    pyqt_signal_json_out = pyqtSignal(dict)
    pyqt_signal_error = pyqtSignal(str)
    pyqt_signal_progress = pyqtSignal(int)

    def __init__(self, cmd_list, url, ip):
        QThread.__init__(self)
        self.cmd_list = cmd_list
        self.url = url
        self.ip = ip
        self.ui = TasmohabUI()
        self.timeout = .5
        self.max_retries = 2
        self.response_waiting = .1

    def run(self):
        self.send_http_cmd(self.cmd_list)
        return

    def send_http_cmd(self, cmds):                                                                  # send cmd as a list
        resp_code = 0
        result = {}
        try:
            #self.http_url = 'https://jsonplaceholder.typicode.com/todos/1'                         # for debug
            for cmd in cmds:
                retry = 0
                while retry <= self.max_retries:
                    resp_code = self.url_response_code(self.url + 'Time')  # check connection with some command
                    if resp_code == 200:  # if http ok (200) ...
                            json_tmp = ''
                            json_tmp = self.load_json_url(self.url, cmd)                                   # save return data
                            if (self.ui.is_json(json_tmp)):  # if the string is valid json
                                #result.update(json.loads(json_tmp))
                                result[cmd] = json.loads(json_tmp)
                            self.pyqt_signal_progress.emit(round(100 / len(cmds) * (cmds.index(cmd)+1)))     # update progressbar
                            break
                    else:
                        retry += 1
                        result[cmd] = {}
                        time.sleep(self.response_waiting)
                if retry >= self.max_retries:
                    self.pyqt_signal_error.emit(self.ui.http_err_msg)
                    break
        except Exception as e:
            #self.report_error()                                                                    # for debug
            self.pyqt_signal_error.emit('Err in http thread:' + str(e))
            pass
        self.pyqt_signal_json_out.emit(result)
        self.cmd_list.clear()

    def url_response_code(self, url):
        resp_code = None
        try:
            resp_code = requests.get(url, timeout=self.timeout).status_code  # response code
            self.ui.append_to_log("Response Code:" + str(resp_code))
            return resp_code
        except Exception as e:
            self.ui.report_error()                                        # for debug
            self.pyqt_signal_error.emit("Connection Error to " + self.ip + '. HTTP Response Code:' + str(resp_code))

    def load_json_url(self, url, params):
        para = urllib.parse.quote(params)
        data = json.dumps(requests.get(url+para).json())
        return data


class DetailWindow(QWidget):
    def __init__(self, string, format_to_json=True):
        super().__init__()
        # global json_dev_status
        layout = QVBoxLayout()
        self.textbrowser = QTextBrowser()
        self.textbrowser.setOpenExternalLinks(True)
        if format_to_json:
            self.textbrowser.append(json.dumps(string, indent=4, sort_keys=False))
        else:
            self.textbrowser.append(string)
        layout.addWidget(self.textbrowser)
        self.setLayout(layout)
        self.setWindowTitle('Details')
        self.setMinimumSize(600, 600)
        self.show()


class DevConfigWindow(QtWidgets.QDialog, dev_config.Ui_Dialog):
    def __init__(self, mainui):
        super(DevConfigWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.ui = mainui
        # uic.loadUi('dev_config.ui', self)  # Load the .ui file                 # alternativ with ui-file (class DevConfigWindow(QtWidgets.QDialog):)
        self.movie = QtGui.QMovie(resource_path('loader.gif'))
        self.btn_save_conf.clicked.connect(self.save_config)
        self.btn_send_conf.clicked.connect(self.send_config)
        self.set_text()

    def set_text(self):
        try:
            if 'settings' in json_config_data:  # if config file is loaded
                self.btn_save_conf.setEnabled(True)
            if 'backlog' in json_config_data['settings']:
                self.backlog.setText(json_config_data['settings']['backlog'])
        except Exception as e:
            print(e)
        qline_edits = self.frame.findChildren(QLineEdit)                    # returns a list of all QLineEdit objects
        for widget in qline_edits:                                          # loop through all found QLineEdit widgets
            for key, value in get_key_val_pair(json_dev_status):            # loop through all key value pairs in 'json_dev_status' ...
                if str(key).lower() == str(widget.objectName()).lower():                              # and look if the widget name is in 'json_dev_status' dict
                    obj = self.frame.findChild(QLineEdit, widget.objectName())      # get widget ...
                    obj.setText(str(value))                                      # and set the text


    def save_config(self):
        global json_config_data
        if str(self.backlog.text()) != '':
            try:
                json_config_data['settings']['backlog'] = str(self.backlog.text())
                self.ui.update_json_to_yaml_config_data()
                QMessageBox.information(self, 'Information', 'Backlog command saved in config!')
            except Exception as e:
                print('Exception:' + str(e))
        else:
            QMessageBox.warning(self, 'Warning', 'Backlog command is empty!')

    def send_config(self):
        """Adding more commands to send:\n
        - add a new widget 'QLineEdit' with the objectname = the tasmota commandname (f.e.: 'ssid1')
        - the function get this object (and its name) and put the name with its value to the backlog command"""
        cmds = {}
        qline_edits = self.frame.findChildren(QLineEdit)                # returns a list of all QLineEdit objects
        for widget in qline_edits:
            # get cmd name = 'widget.objectName()'
            # get cmd value = 'widget.text()'
            cmds[widget.objectName()] = widget.text()
        if len(cmds) > 30:
            print('Error:Backlog command only allows executing up to 30 consecutive commands!')
            return
        else:
            queue = []
            backlog_str1 = ''
            backlog_str2 = ''
            tmp = ''
            for cmd, value in cmds.items():
                if cmd == 'backlog':
                    if value != '':
                        backlog_str2 = 'backlog '
                        backlog_str2 += str(value)
                        continue
                    else:
                        continue
                if value != '':
                    tmp += str(cmd + ' ' + value)
                    tmp += '; '
            if tmp != '':
                backlog_str1 = 'backlog ' + tmp                                         # generate the backlog string
                backlog_str1 = backlog_str1[:-2]                                        # remove last two chars
                queue.append(backlog_str1)                                              # append the first backlog STRING (!) to list
            if backlog_str2 != '':
                queue.append(backlog_str2)
            if bool(queue):                                                               # if cmd is not empty
                #queue.append('restart 1')
                buttonreply = QMessageBox.question(self, 'Sending device config',
                                               "Are you sure to send the following commands to the device?:\n\n"+backlog_str1+'\n\n'+backlog_str2,
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            else:
                QMessageBox.warning(self, 'Warning', 'No commands to send!')
                return
            if buttonreply == QMessageBox.Yes:
                self.ui.last_communication_class.timeout = .7                                                 # set the timeout of class
                self.ui.last_communication_class.max_retries = 4
                self.ui.last_communication_class.response_waiting = len(cmds)*0.2                             # adaptive waiting: 0.1s times no of cmds
                self.ui.last_communication_class.cmd_list = queue
                #self.ui.last_communication_class.pyqt_signal_error.connect(self.ui.datathread_on_error)      # 2nd argument is the returned data!!!
                self.ui.last_communication_class.pyqt_signal_error.disconnect()
                self.ui.last_communication_class.pyqt_signal_json_out.disconnect()                          # dont save the response into 'json_dev_status'
                self.ui.last_communication_class.pyqt_signal_json_out.connect(self.datathread_response)
                self.ui.last_communication_class.finished.connect(self.datathread_finished)
                self.loader_img = QLabel(self.frame)
                self.loader_img.setObjectName("loader")
                self.loader_img.setAlignment(QtCore.Qt.AlignCenter)
                self.loader_img.setMovie(self.movie)
                self.lay_button.addWidget(self.loader_img)
                try:
                    self.movie.start()                                                                     # show loadging gif
                    self.btn_send_conf.setEnabled(False)
                    self.ui.btn_set_dev_conf.setEnabled(False)
                    self.ui.append_to_log('Sending new configuration to device ...')
                    print('Sending to device:' + str(queue))
                    self.ui.last_communication_class.start()
                except Exception as e:
                    self.ui.report_error()

    def datathread_response(self, data):
        #a = json.dumps(data)
        self.label = QLabel('Response:')
        self.browser = QTextBrowser(self.frame)
        self.browser.setObjectName("response_browser")
        self.lay_button.addWidget(self.label)
        self.lay_button.addWidget(self.browser)
        for key, value in data.items():
            self.browser.append(key+':\n')
            self.browser.append(json.dumps(value)+'\n')

    def datathread_finished(self):
        global json_dev_status
        QMessageBox.information(self, 'Config send', 'Config was send! Please reboot device and get new device info!')
        self.ui.append_to_log('Configuration send, rebooting device!')
        json_dev_status.clear()                                                             # clear device data, because it maybe contains old data
        json_tasmota_objects.clear()                                                        # clear tasmota objects
        self.ui.update_ui_device_info()                                                   # clear device info data on ui
        self.ui.clear_ui_widgets()                                                          # clear widgets in scrollarea
        self.movie.stop()                                                                   # stop and delete spinner
        self.loader_img.deleteLater()                                                       # delete loader


### MAIN ###
def main_ui():
    app = QApplication(sys.argv)

    ## set stylesheet
    ## https://github.com/Alexhuszagh/BreezeStyleSheets
    ## python stylesheet/configure.py --styles=all --extensions=all --resource breeze.qrc
    ## pyrcc5 stylesheet/dist/breeze.qrc -o breeze_resources.py
    #file = QFile(":/light/stylesheet.qss")
    #file.open(QFile.ReadOnly | QFile.Text)
    #stream = QTextStream(file)
    #app.setStyleSheet(stream.readAll())

    app.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))
    UI = TasmohabUI()
    UI.show()
    UI.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))
    UI.list_com_ports()  # at startup list ports
    sys.exit(app.exec())  # return code of ui app

# this is only for pyinstaller (path for data in --onefile mode)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def keys_exists(element, *keys):
    '''
    Check if keys exists in in dict.
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

def get_key_val_pair(dictionary):
    '''
    Get key, value pair in (nested) in nested dict.
    '''
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from get_key_val_pair(value)
        else:
            yield (key, value)


if __name__ == '__main__':
    t_ui = threading.Thread(target=main_ui, name='UI_Thread')
    t_ui.start()
    print('Running threads:')
    for thread in threading.enumerate():
        print(thread.name)
    print('\n')

    while not t_ui.is_alive():
        pass
        #time.sleep(.5)
        #if not t_ui.is_alive():
    sys.exit()
