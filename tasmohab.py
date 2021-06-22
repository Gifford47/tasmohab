# -*- coding: utf-8 -*-
# !/usr/bin/env python

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QTextBrowser, QLabel, QVBoxLayout, QWidget, \
    QGridLayout, QCheckBox, QLineEdit, QComboBox

from datetime import datetime
from collections import defaultdict
import requests, json, time, queue, threading
from serial.tools.list_ports import comports
import os, sys, traceback, yaml, re
from serial import Serial
import tasmohabUI
import dev_config
import serial
import openhab
import tas_cmds

sys.path.append('./ohgen')  # import ohgen folder
import ohgen
import globals

ohgen_templates = []  # templates for ohgen

json_config_data = {}  # data from YAML config file
json_dev_status = {}  # data from device (http or serial)
json_gpio_status = {}  # data from device (http or serial)
json_tasmota_objects = {}  # this object is also used and filled when importing existing object config!


class tasmohabUI(QtWidgets.QMainWindow, tasmohabUI.Ui_MainWindow):

    def __init__(self, parent=None):
        super(tasmohabUI, self).__init__(parent)
        self.setupUi(self)
        self.http_url = ''

        self.UI_threads = []  # list of queued ui-threads
        self.yaml_config_data = ''
        self.json_config_data_new = {}
        for root, dirs, files in os.walk("./ohgen/templates"):                              # scan all template files (*.tpl) in dir
            for file in files:
                if file.endswith(".tpl"):
                    ohgen_templates.append(str(file.split('.')[0]))
        self.cmb_template.addItems(ohgen_templates)

        self.dev_config_wind = DevConfigWindow  # create an instance

        # menubar
        self.actionInfo.triggered.connect(self.about)
        self.actionExit.triggered.connect(self.exit)

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
        self.btn_gen_fin_objts.clicked.connect(self.gen_fin_objects)
        self.btn_save_final_obj.clicked.connect(self.save_final_files)
        self.btn_clear_log.clicked.connect(self.clear_log)

    def clear_log(self):
        self.txt_log.clear()

    def report_error(self, error=None):
        if error is not None:
            print(error)
        traceback.print_exc(limit=2, file=sys.stdout)

    def is_json(self, data):
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
            self.report_error(e)
        self.append_to_log("Config file saved:" + str(filepath))

    def list_com_ports(self):
        # adding list of items to combo box
        self.cmb_ports.clear()
        ports = [comport.device for comport in serial.tools.list_ports.comports()]
        self.append_to_log(ports)
        if not ports:  # if list is empty
            self.btn_get_serial.setEnabled(False)
        else:
            ports.sort()
            self.btn_get_serial.setEnabled(True)
            self.cmb_ports.addItems(ports)

    def append_to_log(self, text):
        self.txt_log.append(datetime.today().strftime('%d-%m-%Y %H:%M:%S') + '\t' + str(text))  # '\t' = tab space
        self.lbl_last_log.setText(str(text))

    def save_yaml_file_config(self):
        if bool(json_config_data):  # if json_config_data is not empty
            json_config_data['settings']['outputs']['default-output']['things-file'] = self.txt_thing_file.text()
            json_config_data['settings']['outputs']['default-output']['items-file'] = self.txt_item_file.text()

            self.update_yaml_to_json_config_data()                                              # update the internal yaml data
            if os.path.isfile(self.txt_config_file_path.text()):
                # noinspection PyTypeChecker
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

    def datathread_gpio_data(self, data):
        global json_gpio_status
        json_gpio_status = data
        try:
            self.create_tasmota_objects()
            self.add_ui_widgets()
        except Exception as e:
            traceback.print_exc(limit=2, file=sys.stdout)
            self.append_to_log('Failure when creating tasmota objects:'+str(e))

    def datathread_dev_data(self, data):
        global json_dev_status
        json_dev_status = data
        self.update_ui_device()

    def datathread_on_error(self, data):
        self.append_to_log(str(data))

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

        self.cmd = []  # for gpio
        for key, value in tas_cmds.gpio.items():
            self.cmd.append(value)

        self.get_ser_gpio_info = SerialDataThread(self.cmd, self.cmb_ports.currentText(), self.cmb_baud.currentText())
        self.get_ser_gpio_info.pyqt_signal_json_out.connect(self.datathread_gpio_data)  # 2nd argument is the returned data!!!
        self.get_ser_gpio_info.pyqt_signal_error.connect(self.datathread_on_error)      # 2nd argument is the returned data!!!
        self.get_ser_gpio_info.finished.connect(self.datathread_finish)
        self.get_ser_gpio_info.pyqt_signal_progress.connect(self.update_progressbar)

        self.UI_threads.append(self.get_ser_gpio_info)                                  # appent to list of queued ui-threads
        self.start_queued_threads()  # start queued threads

    def start_queued_threads(self):  # DON`T FORGET TO EXIT THE THREAD AFTER FINISH!!!
        print('Queued pyqt UI-Threads:' + str(len(self.UI_threads)))
        self.append_to_log('Queued pyqt UI-Threads:' + str(len(self.UI_threads)))
        if len(self.UI_threads) > 0:  # if found more than 0 elements
            self.UI_threads[0].start()  # get first element (thread) of list and start it. DON`T FORGET TO EXIT THE THREAD AFTER FINISH!!!

    def get_data_on_http(self):
        global json_dev_status
        global json_gpio_status
        if (self.txt_user.text() == "" and self.txt_pass.text() == ""):
            self.http_url = 'http://' + self.txt_ip.text() + '/cm?cmnd='
        else:
            self.http_url = 'http://' + self.txt_ip.text() + '/cm?user=' + self.txt_user.text() + '&password=' + self.txt_pass.text() + '&cmnd='
        self.cmd = []  # for status cmd
        for key, value in tas_cmds.status.items():
            self.cmd.append(value)
        self.get_http_dev_info = HttpDataThread(self.cmd, self.http_url, self.txt_ip.text())
        self.get_http_dev_info.pyqt_signal_json_out.connect(self.datathread_dev_data)       # 2nd argument is the returned data!!!
        self.get_http_dev_info.pyqt_signal_error.connect(self.datathread_on_error)          # 2nd argument is the returned data!!!
        self.get_http_dev_info.finished.connect(self.datathread_finish)
        self.get_http_dev_info.pyqt_signal_progress.connect(self.update_progressbar)
        self.UI_threads.append(self.get_http_dev_info)                                      # appent to list of queued ui-threads

        self.cmd = []                                                                       # for gpio cmds
        for key, value in tas_cmds.gpio.items():
            self.cmd.append(value)
        self.get_http_gpio_info = HttpDataThread(self.cmd, self.http_url, self.txt_ip.text())
        self.get_http_gpio_info.pyqt_signal_json_out.connect(self.datathread_gpio_data)     # 2nd argument is the returned data!!!
        self.get_http_gpio_info.pyqt_signal_error.connect(self.datathread_on_error)         # 2nd argument is the returned data!!!
        self.get_http_gpio_info.finished.connect(self.datathread_finish)
        self.get_http_gpio_info.pyqt_signal_progress.connect(self.update_progressbar)
        self.UI_threads.append(self.get_http_gpio_info)                                     # appent to list of queued ui-threads

        self.start_queued_threads()  # start queued threads

    def update_ui_device(self):
        global json_dev_status
        if not bool(json_dev_status):  # if json is empty
            self.lbl_dev_hostname.setText("")
            self.lbl_dev_firmware.setText("")
            self.lbl_dev_name.setText("")
            self.lbl_dev_module.setText("")
            for i in reversed(range(self.objects_grid.count()-1)):
                self.objects_grid.takeAt(i).widget().deleteLater()                          # delete all last widgets
        elif json_dev_status is not None and bool(json_dev_status):  # if json is not None
            self.lbl_dev_hostname.setText(str(json_dev_status['StatusNET']['Hostname']))
            self.lbl_dev_firmware.setText(str(json_dev_status['StatusFWR']['Version']))
            self.lbl_dev_name.setText(str(json_dev_status['Status']['DeviceName']))
            self.lbl_dev_module.setText(str(json_dev_status['Status']['Module']))

    def load_yaml_file_config(self):
        global json_config_data
        self.conf_file = QFileDialog.getOpenFileName(filter="YAML(*.yaml)")[0]
        if not self.conf_file == '':
            self.txt_config_file_path.setText(self.conf_file)
            json_config_data = self.read_yaml(self.conf_file)
            if 'settings' in json_config_data:
                self.txt_thing_file.setText(json_config_data['settings']['outputs']['default-output']['things-file'])
                self.txt_item_file.setText(json_config_data['settings']['outputs']['default-output']['items-file'])
            else:
                self.append_to_log('Corrupt YAML file loaded! Exiting here!')
            self.set_config_settings()
            self.update_json_to_yaml_config_data()
            self.gen_fin_objects()
            self.btn_gen_fin_objts.setEnabled(True)
            self.btn_save_final_obj.setEnabled(True)
            self.btn_set_dev_conf.setEnabled(True)

    def show_device_details(self):
        self.det_window = DetailWindow(json_dev_status)                 # initialize 2. windows for dev details
        self.det_window.show()

    def show_device_config(self):
        self.dev_config_wind = DevConfigWindow(self)                    # pass the current class object to modify its objects
        self.dev_config_wind.show()

    def create_tasmota_objects(self):
        global json_tasmota_objects

        # read every tasmota gpio and set object dict
        json_tasmota_objects['gpios'] = {}
        for gpio, value in json_gpio_status.items():
            first_key_gpio = str(list(json_gpio_status[gpio].keys())[0])                        # contains dict, f.e. '160': 'Switch1'
            first_key_gpio_val = json_gpio_status[gpio][first_key_gpio]                         # contains str, f.e. 'AM2301' or 'Switch1'
            json_tasmota_objects['gpios'][gpio] = {}  # placeholder (dict)
            json_tasmota_objects['thingid'] = json_dev_status['StatusNET']['Hostname']
            if first_key_gpio_val != 'None':
                json_tasmota_objects['gpios'][gpio]['active'] = True
            else:
                json_tasmota_objects['gpios'][gpio]['active'] = False
            json_tasmota_objects['gpios'][gpio]['gpio_val'] = value
            json_tasmota_objects['gpios'][gpio]['peripheral'] = first_key_gpio_val
            json_tasmota_objects['gpios'][gpio]['sensors'] = {}
            if first_key_gpio_val in json_dev_status['StatusSNS']:                              # list all possible sensor data
                # check if val is a dict. if not, create a dict with gpio name and gpio val
                if isinstance(json_dev_status['StatusSNS'][first_key_gpio_val], dict):          # check if val of sensor data is a dict
                    json_tasmota_objects['gpios'][gpio]['sensors'] = json_dev_status['StatusSNS'][first_key_gpio_val]  # fill in sensor data
                else:
                    json_tasmota_objects['gpios'][gpio]['sensors'][first_key_gpio_val] = json_dev_status['StatusSNS'][first_key_gpio_val]

    def add_ui_widgets(self):
        global json_tasmota_objects
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 207))
        self.objects_grid = QGridLayout(self.scrollAreaWidgetContents)
        # generate the headlines
        self.objects_grid.addWidget(QLabel('Active'), 0, 0)                  # Adds a widget at specified row and column
        self.objects_grid.addWidget(QLabel('GPIO'), 0, 1)
        self.objects_grid.addWidget(QLabel('GPIO Value'), 0, 2)
        self.objects_grid.addWidget(QLabel('Peripheral Name'), 0, 3)
        self.objects_grid.addWidget(QLabel('Item Type'), 0, 4)
        self.objects_grid.addWidget(QLabel('Groups'), 0, 5)
        self.objects_grid.addWidget(QLabel('Feature'), 0, 6)
        self.objects_grid.addWidget(QLabel('Metadata'), 0, 7)
        self.objects_grid.addWidget(QLabel('Tags'), 0, 8)

        # creating UI Widgets:
        # iter items for every single widget
        row = 1  # row
        for gpio, value in json_tasmota_objects['gpios'].items():
            peripheral_no = []
            peripheral_no = list(json_tasmota_objects['gpios'][gpio]['gpio_val'].keys())[0]  # get the tasmota peripheral no f.e. '1216' (for AM2301)
            # now the first four coloums will be filled:
            cb = QCheckBox()
            cb.setChecked(json_tasmota_objects['gpios'][gpio]['active'])
            self.objects_grid.addWidget(cb, row, 0)  # Adds a widget at specified row and column                                # add the checkbox
            self.objects_grid.addWidget(QLabel(gpio), row, 1)  # add the gpio label
            self.objects_grid.addWidget(QLabel(str(json_tasmota_objects['gpios'][gpio]['gpio_val'])), row, 2)  # add the gpio value(s)
            # for the following coloums:
            # check if it is a sensor or a actuator and display the appropriate widgets:
            if json_tasmota_objects['gpios'][gpio]['active']:  # only create following widgets when gpio has an peripheral
                # if the peripheral is a sensor, create an item for every measurement item
                if 'sensors' in json_tasmota_objects['gpios'][gpio]:                    # if key in dict exists ...
                    if bool(json_tasmota_objects['gpios'][gpio]['sensors']):            # if dict is not empty (peripheral is a sensor...)
                        # i am a sensor
                        self.add_ui_widget_peripheral(json_tasmota_objects['gpios'][gpio]['peripheral'], row)        # add the peripheral name/ sensor name
                        row += 1
                    else:                                                               # peripheral is not a sensor, but an actuator
                        # i am a actuator
                        # write in same line like 'gpiox'
                        self.add_ui_widget_peripheral(json_tasmota_objects['gpios'][gpio]['peripheral'], row)
                        self.add_ui_widgets_openhab(self.objects_grid, row, peripheral_no=peripheral_no)
                    row += 1                                                            # next line
            else:
                row += 1                                                                # next line
        # all gpios, corresponding sensors and actuators were added, but not sensors,
        # these sensors will be added in the following
        row += 1
        self.objects_grid.addWidget(QLabel('Sensors:'), row, 0)  # add Header for additional sensors
        row += 1
        for sensorname, value in json_dev_status['StatusSNS'].items():
            if isinstance(json_dev_status['StatusSNS'][sensorname], dict):                    # if sensor has a following dict:
                # create an item for every row:
                cb = QCheckBox()
                cb.setChecked(True)
                self.objects_grid.addWidget(cb, row, 0)  # add the checkbox for the sensor
                self.add_ui_widget_peripheral(sensorname, row)
                row += 1
                for sensor, value in json_dev_status['StatusSNS'][sensorname].items():        # iter over items
                    self.add_ui_widgets_sensor_single_line(self.objects_grid, row, sensor, value)             # add sensor to layout
                    row += 1
            else:
                self.add_ui_widget_peripheral(sensorname, row)
                self.add_ui_widgets_sensor_single_line(self.objects_grid, row, sensorname, value, col_cb=0)
                row += 1
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btn_refr_obj_data.setEnabled(True)

    def add_ui_widget_peripheral(self, name, row, col=3):
        lbl = QLabel(name)
        self.objects_grid.addWidget(lbl, row, col)  # add the peripheral name/ sensor name

    def add_ui_widgets_openhab(self, layout, row, peripheral_no='default'):
        cb = QComboBox()
        cb.addItems(openhab.item_types)
        try:
            cb.setCurrentIndex(openhab.std_items[peripheral_no]['std_type'])
        except:
            pass  # if index is not found
        layout.addWidget(cb, row, 4)  # add sensor value
        line = QLineEdit()
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, 5)
        cb = QComboBox()
        try:
            cb.addItems(openhab.std_items[peripheral_no]['feature'])                       # try to get index
        except:
            cb.addItems(openhab.std_items['default']['feature'])                           # else: return default value
        layout.addWidget(cb, row, 6)
        try:
            line = QLineEdit(openhab.std_items[peripheral_no]['meta'])
        except:
            line = QLineEdit(openhab.std_items['default']['meta'])
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, 7)
        try:
            line = QLineEdit(openhab.std_items[peripheral_no]['tags'])
        except:
            line = QLineEdit(openhab.std_items['default']['tags'])
        line.setMaximumWidth(200)
        line.setMaxLength(80)
        layout.addWidget(line, row, 8)

    def add_ui_widgets_sensor_single_line(self, layout, row, sensor, value, col_cb=1):
        cb = QCheckBox()
        cb.setChecked(True)
        layout.addWidget(cb, row, col_cb)  # add the checkbox for the sensor
        layout.addWidget(QLabel(sensor+':'+str(value)), row, 2)
        line = QLabel(sensor)
        #line.setMaximumWidth(200)
        #line.setMaxLength(80)
        layout.addWidget(line, row, 3)  # add sensor name
        self.add_ui_widgets_openhab(layout, row, peripheral_no=openhab.gpio_conversion.get(sensor,'default'))
        row += 1

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
        global json_config_data
        self.json_config_data_new.clear()                                                # clearing all entries
        if 'settings' in json_config_data:                                               # config file is loaded
            self.json_config_data_new['settings'] = json_config_data['settings'].copy()  # copy settings section
            try:  # add here things, that comes from device data...
                self.json_config_data_new['settings']['hostname'] = json_tasmota_objects['thingid']  # json_tasmota_objects could not be initiated
                self.json_config_data_new['settings']['friendlyname'] = json_dev_status['Status']['FriendlyName'][0]
                self.json_config_data_new['settings']['deviceName'] = json_dev_status['Status']['DeviceName']
                self.json_config_data_new['settings']['topic'] = json_dev_status['Status']['Topic']
            except Exception as e:
                pass
            self.json_config_data_new['settings']['outputs']['default-output'][
                'items-file'] = self.txt_item_file.text()  # item file
            self.json_config_data_new['settings']['outputs']['default-output'][
                'things-file'] = self.txt_thing_file.text()  # thing file
            json_config_data['settings'] = self.json_config_data_new[
                'settings'].copy()  # already copy new values to standard config data
            self.append_to_log('JSON settings config updated!')
            return True
        return False

    # update the json configuration here in relation to the user configurations for the tasmota objects
    # all entries from tasmota objects in the ui are read in here and stored in the 'json_config_data'
    # then the 'json_config_data' is taken to create the things and items
    def update_json_config_data_from_ui(self):
        global json_config_data
        if bool(json_config_data) == False:  # if dict is empty (no config file loaded
            # noinspection PyTypeChecker
            QMessageBox.information(self, 'No device config File!', 'Please load a template config file at minimum.',
                                    QMessageBox.Ok, QMessageBox.Ok)
            return
        if self.set_config_settings():
            thing_id = self.json_config_data_new['settings']['hostname']
            self.json_config_data_new[thing_id] = {}                              # create a new thing entry
            self.json_config_data_new[thing_id]['thingid'] = thing_id             # generate thingid
            self.json_config_data_new[thing_id]['label'] = self.json_config_data_new['settings']['deviceName']             # generate thing label
            self.json_config_data_new[thing_id]['template'] = str(self.cmb_template.currentText())      # qcombobox
            self.json_config_data_new[thing_id]['topic'] = self.json_config_data_new['settings']['topic']
            self.items_dict = defaultdict(list)                                        # create a dict with list for each item
            self.items_dict.clear()                                                 # clear old content
            row = 1
            col = 0
            tot_rows = self.objects_grid.rowCount()
            while row < tot_rows:  # loop through all rows
                try:
                    item = self.objects_grid.itemAtPosition(row, col)                                                       # get first item: the sensor, i.e. AM2301
                    if type(item.widget()) == QCheckBox and item.widget().isChecked():                              # if gpio checkbox is checked
                        item_name = str(self.objects_grid.itemAtPosition(row, col + 3).widget().text()).replace(' ','_')    # f.e.: the sensor name. replace space with underline
                        ###################### Check if sensor or actuator ######################
                        # if the next line is a QCheckbox: create a new item in last thing
                        # if the next line in next coloumn is a QCheckbox: create a new sensoritem
                        try:
                            next_item = self.objects_grid.itemAtPosition(row+1, col + 1).widget()                   # get item at next row and col
                        except:
                            next_item = None
                        if next_item is not None and type(next_item) == QCheckBox:
                            # i am a sensor: read the sensor and fill the dict
                            row += 1                                                                                # next line
                            while (type(next_item) == QCheckBox):
                                if next_item.isChecked():                                                           # get the sensor checkbox (not the gpio checkbox!)
                                    self.fill_items_dict(item_name, row, col)                                       # add item to dict
                                row += 1
                                try:
                                    next_item = self.objects_grid.itemAtPosition(row, col + 1).widget()             # try to get the next checkbox
                                except:
                                    next_item = None
                        else:                                                                                       # this line has no item and is a actuator
                            # i am a single sensor (one line in ui) or a actuator: read in and fill the dict
                            self.fill_items_dict(item_name, row, col)                                               # add item to dict
                            row += 1
                        ###################### END ######################
                        self.json_config_data_new[thing_id].update(self.items_dict)                                 # write new items to dict
                    else:
                        row += 1                                                                                # next line, last was unchecked
                except Exception as e:
                    # line is empty or has no widget at row, col
                    #self.report_error()                                                                        # optional
                    row += 1
            self.json_config_data_new = dict(self.json_config_data_new)
        else:                                                                                                   # no config file is loaded
            print('TODO: create a template for new config file ...')
        json_config_data.clear()  # clear to avoid duplicates
        json_config_data = self.json_config_data_new.copy()  # copy dict to dict
        self.update_json_to_yaml_config_data()
        cur_index = self.tabWidget.currentIndex()
        self.tabWidget.setCurrentIndex(cur_index + 1)

    def fill_items_dict(self, item_name, row, col):
        item_label = str(self.objects_grid.itemAtPosition(row, col + 3).widget().text())  # qlineedit
        item_type = str(self.objects_grid.itemAtPosition(row, col + 4).widget().currentText())  # qcombobox
        item_groups = str(self.objects_grid.itemAtPosition(row, col + 5).widget().text())  # qlineedit
        item_feature = str(self.objects_grid.itemAtPosition(row, col + 6).widget().currentText())  # qcombobox
        item_meta = str(self.objects_grid.itemAtPosition(row, col + 7).widget().text())  # qlineedit
        item_tags = str(self.objects_grid.itemAtPosition(row, col + 8).widget().text())  # qlineedit
        self.items_dict[item_type].append({'name': item_name,
                                      'label': item_label,
                                      'groups': [item_groups],
                                      'features': [item_feature],
                                      'metadata': [item_meta],
                                      'tags': [item_tags]}
                                     )

    def gen_fin_objects(self):
        self.txt_output_thing.clear()  # clear the textbrowser
        self.txt_output_item.clear()  # clear the textbrowser
        self.update_yaml_to_json_config_data()
        try:
            devices_file_name = self.conf_file
            globals.init_jinja_environment(self.conf_file)  # init global jinja_environment

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
            self.tabWidget.setCurrentIndex(2)  # jump ti final tab
        except Exception as e:
            print(e)

    def save_final_files(self):
        thing_file = json_config_data['settings']['outputs']['default-output']['things-file']
        item_file = json_config_data['settings']['outputs']['default-output']['items-file']
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
            print('Exception in files:' + str(e))

    def about(self):
        self.det_window = DetailWindow('A Tasmota object configurator for smarthome systems. <p>Created by Gifford47<\p>')                 # initialize 2. windows for dev details
        self.det_window.show()

    def exit(self):
        self.close()

class SerialDataThread(QThread):
    pyqt_signal_json_out = pyqtSignal(dict)
    pyqt_signal_error = pyqtSignal(str)
    pyqt_signal_progress = pyqtSignal(int)

    def __init__(self, cmd_list, port, baud):
        QThread.__init__(self)
        self.cmd_list = cmd_list
        self.port = port
        self.baud = baud

    def run(self):
        ser = Serial(str(self.port), str(self.baud), timeout=.1)
        json_str = {}
        ui = tasmohabUI()
        try:
            if ser.is_open:
                time.sleep(.1)  # skip tasmota startup
                max_retries = 5
                for no, cmd in enumerate(self.cmd_list):
                    retry = 0
                    while retry < max_retries:
                        msg = ''
                        ser.reset_output_buffer()
                        ser.reset_input_buffer()
                        ser.write(str.encode(cmd + '\n'))
                        ser.flush()  # it is buffering. required to get the data out *now*
                        time.sleep(.1)
                        while ser.inWaiting() > 0:
                            msg = ser.read_until('\r\n').decode(encoding='utf-8')  # get serial response and encode
                        json_tmp = msg[msg.find('{'):msg.find('\0')]  # find json between string
                        if (tasmohabUI.is_json(ui, json_tmp)):  # if the string is valid json
                            json_str.update(json.loads(json_tmp))
                            retry = 0
                            self.pyqt_signal_progress.emit(round(100 / len(self.cmd_list) * (no + 1)))  # update progress
                            break  # leave the while
                        else:
                            if retry >= max_retries:
                                self.pyqt_signal_error.emit('Could not get valid JSON data.')
                            else:
                                retry += 1  # retry if not valid json
                                print('Non valid JSON response received, retrying ...')
                                self.pyqt_signal_error.emit('Non valid JSON response received, retrying ...')
                                time.sleep(.5)  # wait for new data
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
        self.pyqt_signal_json_out.emit(json_str)

class HttpDataThread(QThread):
    pyqt_signal_json_out = pyqtSignal(dict)
    pyqt_signal_error = pyqtSignal(str)
    pyqt_signal_progress = pyqtSignal(int)

    def __init__(self, cmd_list, url, ip):
        QThread.__init__(self)
        self.cmd_list = cmd_list
        self.url = url
        self.ip = ip
        self.ui = tasmohabUI()

    def run(self):
        self.send_http_cmd(self.cmd_list)

    def send_http_cmd(self, cmds):                                                                  # send cmd as a list
        resp_code = 0
        result = {}
        try:
            #self.http_url = 'https://jsonplaceholder.typicode.com/todos/1'                         # for debug
            resp_code = self.url_response_code(self.url + cmds[0])                                  # check connection with first command
            if resp_code == 200:  # if http ok (200) ...
                for cmd in cmds:
                    json_tmp = self.load_json_url(self.url + cmd)                                   # save return data
                    if (self.ui.is_json(json_tmp)):  # if the string is valid json
                        result.update(json.loads(json_tmp))
                    self.pyqt_signal_progress.emit(round(100 / len(cmds) * (cmds.index(cmd)+1)))     # update progressbar
        except Exception as e:
            #self.report_error()                                                                    # for debug
            self.pyqt_signal_error.emit('Err in http thread:' + str(e))
            pass
        self.pyqt_signal_json_out.emit(result)

    def url_response_code(self, url):
        resp_code = None
        try:
            resp_code = requests.get(url, timeout=.5).status_code  # response code
            self.ui.append_to_log("Response Code:" + str(resp_code))
            return resp_code
        except Exception as e:
            self.ui.report_error()                                        # for debug
            self.pyqt_signal_error.emit("Connection Error to " + self.ip + '. HTTP Response Code:' + str(resp_code))

    def load_json_url(self, x):
        data = json.dumps(requests.get(x).json())
        return data


class DetailWindow(QWidget):
    def __init__(self, json_str):
        super().__init__()
        # global json_dev_status
        layout = QVBoxLayout()
        self.textbrowser = QTextBrowser()
        self.textbrowser.append(json.dumps(json_str, indent=4, sort_keys=False))
        layout.addWidget(self.textbrowser)
        self.setLayout(layout)
        self.setWindowTitle('Details')
        self.setMinimumSize(600, 600)
        self.show()


class DevConfigWindow(QtWidgets.QDialog, dev_config.Ui_Dialog):
    def __init__(self, mainui):
        super(DevConfigWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.ui = mainui
        # uic.loadUi('dev_config.ui', self)  # Load the .ui file                 # alternativ with ui-file (class DevConfigWindow(QtWidgets.QDialog):)
        self.btn_save_conf.clicked.connect(self.save_config)
        self.set_text()

    def set_text(self):
        try:
            if 'settings' in json_config_data:  # if config file is loaded
                self.btn_save_conf.setEnabled(True)
            if 'backlog' in json_config_data['settings']:
                self.txt_backlog.setText(json_config_data['settings']['backlog'])
        except Exception as e:
            print(e)

    def save_config(self):
        global json_config_data
        try:
            json_config_data['settings']['backlog'] = str(self.txt_backlog.text())
            self.ui.update_json_to_yaml_config_data()
            QMessageBox.information(self, 'Information', 'Config was saved!')
        except Exception as e:
            print('Exception:' + str(e))


### MAIN ###
def main_ui():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))
    UI = tasmohabUI()
    UI.show()
    UI.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))
    UI.list_com_ports()  # at startup list ports
    sys.exit(app.exec_())  # return code of ui app

# this is only for pyinstaller (path for data in --onefile mode)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    t_ui = threading.Thread(target=main_ui, name='UI_Thread')
    t_ui.start()
    print('Running threads:')
    for thread in threading.enumerate():
        print(thread.name)
    print('\n')

    while 1:
        time.sleep(1)
        if not t_ui.is_alive():
            sys.exit()
