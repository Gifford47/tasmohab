from PyQt6 import QtCore, QtGui, QtWidgets, QtGui
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QTextBrowser, QLabel, QVBoxLayout, QWidget, \
    QGridLayout, QCheckBox, QPushButton, QFrame
import tas_cmds
import scrape_docs
import json
import re
from tasmohab import DetailWindow

class Rule_Gen(QtWidgets.QMainWindow):
    def __init__(self, mainui):
        super(Rule_Gen, self).__init__()
        self.setupUi()
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.ui = mainui
        self.docs_url = self.ui.config['DEFAULT']['TasmotaDocs']
        self.cmds = []                              # a list with all cmds to send to the device to get rules
        self.cmds_in_docs = {}                      # a dict with all cmds in the tasmota docs
        self.cmds_in_docs_list = {}                 # a list (extract from dict) with all cmds int the tasmota docs
        self.rule_results = {}                      # inherits all rules
        self.cmds_in_rules = {}                     # inherits all cmds that were used and found in rules (after rule-check)
        self.syntax_words = {'if':'endif',          # if found the key, the value must also appear in the rule
                        'on':'endon',
                        'do':'on'}

        self.get_device_rules()

    def setupUi(self):
        self.setWindowTitle("Rule Editor")
        self.setMinimumSize(600, 500)
        self.frame = QFrame(self)
        self.layout = QVBoxLayout(self.frame)
        self.layout.setObjectName("layout")
        self.frame.setLayout(self.layout)

        self.movie = QtGui.QMovie(resource_path('loader.gif'))
        self.loader_img = QLabel(self.frame)
        self.loader_img.setObjectName("loader")
        self.loader_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loader_img.setMovie(self.movie)
        self.layout.addWidget(self.loader_img)

        self.movie.start()  # show loadging gif

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.frame)

    def rule_layout(self):
        # clear all previous widgets
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        # add widgets in an own GRID(!) for every rule
        for key, value in self.rule_results.items():
            try:
                first_key = list(value.keys())[0]
            except Exception as e:
                print(e)
                return
            self.grid_layout = QGridLayout()
            self.grid_layout.setObjectName(first_key)                # set the obj name

            lbl_rulename = QLabel(key.upper())
            myFont = QtGui.QFont()
            myFont.setBold(True)
            lbl_rulename.setFont(myFont)
            lbl_rulename.setObjectName(first_key+'_'+key)
            self.grid_layout.addWidget(lbl_rulename,0,0)

            i = 1
            for key,value in value[first_key].items():
                key = key.lower()
                if isinstance(value, str) and (value.lower() == 'on' or value.lower() == 'off'):
                    cb = QCheckBox(key)
                    cb.setObjectName(first_key+'_'+key)             # set the obj name
                    if (value.lower() == 'on'):
                        cb.setChecked(True)
                    self.grid_layout.addWidget(cb, i, 0)
                elif key.lower() == 'rules':
                    lbl = QLabel(key)
                    self.grid_layout.addWidget(lbl, i, 0)
                    tb = QTextBrowser()
                    tb.setObjectName(first_key+'_'+key)
                    value = self.color_syntax(value)
                    tb.append(value)
                    tb.setAcceptRichText(True)
                    tb.setReadOnly(False)
                    #tb.setMinimumHeight(80)
                    self.grid_layout.addWidget(tb, i, 1)
                else:
                    lbl = QLabel(key)
                    self.grid_layout.addWidget(lbl, i, 0)
                    lbl = QLabel(str(value))
                    lbl.setObjectName(first_key+'_'+key)
                    self.grid_layout.addWidget(lbl, i, 1)
                i += 1
                self.layout.addLayout(self.grid_layout)

        self.lay_btn = QVBoxLayout(self.frame)
        self.btn_send_rules = QPushButton('Transmit rules')
        self.btn_send_rules.setObjectName('send_rules')
        self.btn_send_rules.clicked.connect(self.transmit_rules)
        self.btn_check_syntax = QPushButton('Check rules')
        self.btn_check_syntax.clicked.connect(self.check_rules)
        self.btn_show_cmd_docs= QPushButton('Fetching docs from: '+self.docs_url+' ...')
        self.btn_show_cmd_docs.clicked.connect(self.show_cmnd_docs)
        self.btn_show_cmd_docs.setEnabled(False)

        self.lay_btn.addWidget(self.btn_check_syntax)
        self.lay_btn.addWidget(self.btn_show_cmd_docs)
        self.lay_btn.addWidget(self.btn_send_rules)
        self.layout.addLayout(self.lay_btn)

        self.loader_img = QLabel(self.frame)
        self.loader_img.setObjectName("loader")
        self.loader_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loader_img.setMovie(self.movie)
        self.layout.addWidget(self.loader_img)
        self.loader_img.hide()

    def transmit_rules(self):
        self.get_rules_from_ui()
        self.transmit_device_rules()

    def get_rules_from_ui(self):
        # get all user inputs and saves the data
        self.backlog = []
        for cmd, value in self.rule_results.items():
            rule_id = list(value.keys())[0]
            backlog_x = 'backlog '
            if self.frame.findChild(QCheckBox,rule_id+'_'+'state').isChecked():
                state = rule_id + ' 1'
            else:
                state = rule_id + ' 0'
            if self.frame.findChild(QCheckBox, rule_id+'_'+'once').isChecked():
                once = rule_id + ' 5'
            else:
                once = rule_id + ' 4'
            if self.frame.findChild(QCheckBox, rule_id + '_' + 'stoponerror').isChecked():
                stoponerr = rule_id + ' 9'
            else:
                stoponerr = rule_id + ' 8'

            text_browser = self.frame.findChild(QTextBrowser, rule_id+'_'+'rules').toPlainText()
            if not text_browser == '':
                text_browser = text_browser.replace('\n', ' ').replace('\r', ' ')
            else:
                text_browser = '"'
            rule = rule_id + ' ' + text_browser
            backlog_x += str(state) + ';' + str(once) + ';' + str(stoponerr)
            self.backlog.append(backlog_x)
            self.backlog.append(rule)

    def transmit_device_rules(self):
        self.ui.append_to_log('Sending new rules to device ...')
        self.loader_img.show()
        self.movie.start()                                      # show loadging gif
        self.ui.last_communication_class.timeout = .1           # set the timeout of class for response (serial or http)
        self.ui.last_communication_class.max_retries = 3
        self.ui.last_communication_class.response_waiting = .1  # internal adaptive waiting: wait for response for every cmd to send
        self.ui.last_communication_class.cmd_list = self.backlog
        self.ui.last_communication_class.pyqt_signal_json_out.disconnect()  # dont save the response into 'json_dev_status'
        self.ui.last_communication_class.pyqt_signal_json_out.connect(self.transm_device_rules_response)
        self.ui.last_communication_class.finished.disconnect()
        self.ui.last_communication_class.finished.connect(self.transm_device_rules_finished)
        self.ui.last_communication_class.start()

    def get_device_rules(self):
        self.get_cmd_list()
        self.ui.last_communication_class.timeout = .1           # set the timeout of class for response (serial or http)
        self.ui.last_communication_class.max_retries = 3
        self.ui.last_communication_class.response_waiting = .01  # internal adaptive waiting: wait for response for every cmd to send
        self.ui.last_communication_class.cmd_list = self.cmds
        # self.ui.last_communication_class.pyqt_signal_error.connect(self.ui.datathread_on_error)      # 2nd argument is the returned data!!!
        #self.ui.last_communication_class.pyqt_signal_error.disconnect()
        self.ui.last_communication_class.pyqt_signal_json_out.disconnect()  # dont save the response into 'json_dev_status'
        self.ui.last_communication_class.pyqt_signal_json_out.connect(self.get_device_rules_response)
        self.ui.last_communication_class.finished.connect(self.get_device_rules_finished)
        self.ui.last_communication_class.start()

    def init_scraper(self,url):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a scrape_worker object
        self.scrape_worker = scrape_page(url)
        # Step 4: Move scrape_worker to the thread
        self.scrape_worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.scrape_worker.run)
        self.scrape_worker.finished.connect(self.thread.quit)
        self.scrape_worker.finished.connect(self.scrape_worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.scrape_worker.result.connect(self.doc_thread_result)
        # Step 6: Start the thread
        self.thread.start()

    def get_device_rules_response(self,data):
        self.rule_results.update(data)
        #print(data)

    def get_device_rules_finished(self):
        try:
            self.init_scraper(self.docs_url)
        except Exception as e:
            print(e)
        self.rule_layout()

    def transm_device_rules_response(self,data):
        if not hasattr(self, 'label_response'):                     # when widgets not existing (first time)
            self.label_response = QLabel('Response:')
            self.browser_response = QTextBrowser(self.frame)
            self.browser_response.setObjectName("response_browser")
            self.layout.addWidget(self.label_response)
            self.layout.addWidget(self.browser_response)
            for key, value in data.items():
                self.browser_response.append(key + ':\n')
                self.browser_response.append(json.dumps(value) + '\n')
        else:                                                       # appent to browser
            for key, value in data.items():
                self.browser_response.append(key + ':\n')
                self.browser_response.append(json.dumps(value) + '\n')

    def transm_device_rules_finished(self):
        self.ui.append_to_log('Rules successfully send!')
        self.loader_img.hide()
        QMessageBox.information(self, 'Rules send', 'Rules successfully send!')

    def doc_thread_result(self,data):
        self.cmds_in_docs = data
        print('Docs fetched from:'+self.docs_url)
        self.btn_show_cmd_docs.setText('Show Docs to used commands')
        self.btn_show_cmd_docs.setEnabled(True)

    def get_cmd_list(self):
        for key, value in tas_cmds.rules.items():
            self.cmds.append(value)

    def color_syntax(self, string):
        highlight_words = []
        for a,b in self.syntax_words.items():
            highlight_words.append(a)
            highlight_words.append(b)
        font_start = "<span style=\"color:#f57842;\">"
        font_end = "</span>"
        string = string.replace(">","&gt;").replace("<","&lt;")             # convert html code (i.e. '>' and '<') so qtextbrowser interpret it as (user)text
        for word in highlight_words:
            if word in string:
                string = re.sub(r'\b' + word + r'\b', font_start+word+font_end, string)     # replace str with font-str
        string = re.sub(r'\b' + 'endon' + r'\b', r'endon<br/>', string)                         # add newline after every endon (trigger end)
        string = re.sub(r'\b' + 'do' + r'\b', r'do<br/>', string)  # add '\n' after every endon (trigger end)
        return string

    def check_rules(self):
        result = ''
        txtbrowser = self.frame.findChildren(QTextBrowser)          # get a list of all Qtextbrwoser
        for a in txtbrowser:                                        # if textbrowser is not a 'rule'
            if not 'rule' in a.objectName():
                break
            raw = a.toPlainText()
            raw = raw.replace('  ', ' ').lower()                            # remove double spacec with one space
            cmd_list = raw.split()                                    # get a list of words
            for key,value in self.syntax_words.items():
                count_key = cmd_list.count(key)                       # count the key in list
                count_val = cmd_list.count(value)
                if count_key != count_val:
                    result += 'Found '+str(count_key)+'x "'+key+'" and '+str(count_val)+'x "'+value+'" in '+a.objectName()+'\n'
            a.setText(self.color_syntax(raw))           # color the syntax
            # find valid cmds with docs:
            self.cmds_in_docs_list = {}
            for key,val in get_key_val_pair(self.cmds_in_docs):
                self.cmds_in_docs_list[key.lower()] = val
            self.find_cmds_in_string(raw)
        if result == '':
            result = 'No syntax errors found!'

        QMessageBox.information(self, 'Rules check', result)

    def find_cmds_in_string(self, string):
        cmd_list = re.split(r'[\s\W#=;%]+',string)       # re split on: '\s'(whitespace), '#', '='
        for word_in_rule in cmd_list:
            word_in_rule = word_in_rule.lower()
            if not word_in_rule.isnumeric():  # only words with/or without numbers are allowed
                if any(a in word_in_rule for a in self.cmds_in_docs_list):  # look if word is in any cmd of cmds_in_docs_list
                    for cat, cat_val in self.cmds_in_docs.items():
                        for cmd, descr in cat_val.items():
                            if re.search(word_in_rule, cmd, re.IGNORECASE):  # if key is found in commands from the docs
                                self.cmds_in_rules.setdefault(cat, {})
                                self.cmds_in_rules[cat][cmd] = descr

    def show_cmnd_docs(self):
        th = '<th style="border:1px solid black;">'
        td = '<td style="border:1px solid black;">'

        html = '<table style="width:100%;text-align:left;">'
        html += '<tr>'+th+'Category</th>'+th+'Command</th>'+th+'Description</th></tr>'

        for cat, val in self.cmds_in_rules.items():
            html += '<tr>'
            html += td + cat + '</td>'
            key = next(iter(val))
            html += td + key + '</td>'
            html += td + val[key] + '</td>'
            html += '</tr>'
            for cmd, desc in val.items():
                if cmd == key:
                    continue
                html += '<tr>'
                html += '<td></td>'
                html += td + cmd + '</td>'
                html += td + desc + '</td>'
                html += '</tr>'
        html += '</table>'
        html = html.replace('\\n', '<br/>').replace('\n', '<br/>')      # replace all newlines with html <br/> tag

        self.det_window = DetailWindow(html, format_to_json=False)                 # initialize detail window
        self.det_window.show()


class scrape_page(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(dict)

    def __init__(self, url):
        super(scrape_page, self).__init__()
        self.url = url

    def run(self):
        self.cmds_in_docs = {}
        self.cmds_in_docs = scrape_docs.get_all_commands(self.url)
        self.result.emit(self.cmds_in_docs)
        self.finished.emit()