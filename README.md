# TasmoHAB - OpenHAB Things and Items Generator via GUI

## Usage
**Please read 'Requirements' before you use the program!**<br><br>
I was inspired by the project https://github.com/jimtng/ohgen to easily link a Tasmota device with OpenHab through a GUI. The programme uses the almost identical code of 'ohgen' to generate the things and items files.
In the first step, all tasmota gpios of a device are queried and the peripherals are displayed in a table. Then the user can select or deselect individual actuators or sensors in the table. In the next step, a (.yaml) config for 'ohgen' is generated, which contains the objects selected by the user. This config can still be edited here.
In the last step, the things and items objects for openhab are displayed. These can either be copied or saved as files.
All read-in and processed data (sensors, device status, actuators, user settings, etc.) can be conveniently viewed in JSON format.

The programme still has potential for improvement, but it is already doing its job.

I would like to invite everyone to participate in the project to improve the tool!

![tasmohab](https://user-images.githubusercontent.com/49484063/122906746-c58c0900-d352-11eb-86c3-e09ea664d0fe.jpg)
![tasmohab3](https://user-images.githubusercontent.com/49484063/122906848-ddfc2380-d352-11eb-9325-dfcb451a60f7.jpg)


## How it works
### Json data 
The program uses 
```
json_config_data = {}                       # data from YAML config file. later it holds all relevant data to generate a thing an item
json_dev_status = {}                        # all device data from device (http or serial)
json_gpio_status = {}                       # all gpio data from device (http or serial)
json_tasmota_objects = {}                   # this object contains only gpio data (name, value and possible sensor) coming from tasmota device
```
```json_tasmota_objects``` will be used later to fill the gui with content (gpios, sensors and actuators).

For example, here is the program flow when you click "Get from serial":

```python
** *tasmohab.py ** *
--> C:\Python36\lib\threading.py
tasmohab. < module > -> threading.Thread.__init__
tasmohab. < module > -> threading.Thread.is_alive
tasmohab. < module > -> threading.Thread.start
tasmohab. < module > -> threading.enumerate
tasmohab. < module > -> threading.name
tasmohab. < module > -> tasmohab.DetailWindow
tasmohab. < module > -> tasmohab.DevConfigWindow
tasmohab. < module > -> tasmohab.HttpDataThread
tasmohab. < module > -> tasmohab.SerialDataThread
tasmohab. < module > -> tasmohab.TasmohabUI
tasmohab.main_ui -> tasmohab.resource_path
tasmohab.main_ui -> tasmohab.TasmohabUI.__init__
tasmohab.main_ui -> tasmohab.TasmohabUI.datathread_dev_data
tasmohab.main_ui -> tasmohab.TasmohabUI.datathread_finish
tasmohab.main_ui -> tasmohab.TasmohabUI.datathread_gpio_data
tasmohab.main_ui -> tasmohab.TasmohabUI.get_data_on_serial
tasmohab.main_ui -> tasmohab.TasmohabUI.list_com_ports
tasmohab.main_ui -> tasmohab.TasmohabUI.update_progressbar

tasmohab.TasmohabUI.__init__ -> tasmohabUI.Ui_MainWindow.setupUi
tasmohab.TasmohabUI.add_ui_widgets -> tasmohab.TasmohabUI.add_ui_headers
tasmohab.TasmohabUI.add_ui_widgets -> tasmohab.TasmohabUI.add_ui_widget_peripheral
tasmohab.TasmohabUI.add_ui_widgets -> tasmohab.TasmohabUI.add_ui_widgets_openhab
tasmohab.TasmohabUI.add_ui_widgets -> tasmohab.TasmohabUI.add_ui_widgets_sensor_single_line
tasmohab.TasmohabUI.add_ui_widgets_sensor_single_line -> tasmohab.TasmohabUI.add_ui_widgets_openhab
tasmohab.TasmohabUI.datathread_dev_data -> tasmohab.TasmohabUI.update_ui_device
tasmohab.TasmohabUI.datathread_finish -> tasmohab.TasmohabUI.start_queued_threads
tasmohab.TasmohabUI.datathread_gpio_data -> tasmohab.TasmohabUI.add_ui_widgets
tasmohab.TasmohabUI.datathread_gpio_data -> tasmohab.TasmohabUI.create_tasmota_objects
tasmohab.TasmohabUI.get_data_on_serial -> tasmohab.SerialDataThread.__init__
tasmohab.TasmohabUI.get_data_on_serial -> tasmohab.TasmohabUI.start_queued_threads

tasmohab.TasmohabUI.list_com_ports -> list_ports_windows.comports
tasmohab.TasmohabUI.list_com_ports -> tasmohab. < listcomp >
tasmohab.TasmohabUI.list_com_ports -> tasmohab.TasmohabUI.append_to_log
tasmohab.TasmohabUI.start_queued_threads -> tasmohab.TasmohabUI.append_to_log

```

![TasmoHab UI Functions](https://github.com/Gifford47/tasmohab/blob/master/docs/tasmohab_widget_functions.png?raw=true)

#### [Show tasmota objects in scrollarea](https://github.com/Gifford47/tasmohab/blob/b7782cbbf6d76dd2fb72342bf9faae315ba54a94/tasmohab.py#L300)<br>
Show whole data (gpio information, openhab items, peripheral name, sensors, etc.) in a table/grid. The program differences between sensors
and actuators. Sensors are objects, which are appear under 'StatusSNS' from the json response of the tasmota device.
All other objects that do not appear there are actuators.
```
def add_ui_widgets(self):
```

#### [Add openhab widgets](https://github.com/Gifford47/tasmohab/blob/b7782cbbf6d76dd2fb72342bf9faae315ba54a94/tasmohab.py#L374)<br>
Add the openhab specific widgets behind the corresponding object:
```
def add_ui_openhab_widgets(self, layout, row, peripheral_no='default'):
```
The values for every widget about an item comes from: [openhab.py](The values for every widget about an item comes from:) 

#### [Generate openhab items and things](https://github.com/Gifford47/tasmohab/blob/57ad5b3bfca9c0363c19613d0d58ef5800bae667/tasmohab.py#L550)
All relevant data is stored in ```json_config_data```[dict]. The function takes these data to generate things 
and items. It appends some additional data and then use [ohgen.py](https://github.com/Gifford47/tasmohab/blob/master/ohgen/ohgen.py) 
to format the output data in a way that openhab can use it. Therefore ohgen needs a 'template of format'.
You have to choose these template before you can generate any thing or output. These templates muste be 
named '*.tpl' and can be edited while runtime. The template have to be stored under ```ohgen/templates/test.tpl```.
The data is then shown in the last tab and can be saved to a thing and an item file.

## In the future ...
Theoretically, it is relatively easy to adapt the output format to other smarthome systems (e.g. homeassistant, etc.).
Among other things, the file ```openhab.py```, the function ```add_ui_openhab_widgets``` and of course the function ```gen_fin_objects``` 
must be adapted or replaced to adapt the output format. The third tab "Object output" can be filled with content e.g. at 
runtime to generate a different layout for other smarthome systems.

## Work in progress
- Device configuration:
    - only 'backlog cmd' is implemented, other configurations are not transmitted or saved

## Debugging
### Convert to .exe
- python -m PyQt5.uic.pyuic tasmohabUI.ui -o tasmohabUI.py       # for UI components
- pyrcc5 resource.qrc -o ressource_rc.py      # for ressource items f.e. images (ressource.qrc)

- pyinstaller --onefile --windowed --icon=icon.ico --noconsole --clean --paths=...\TasmoHAB --pat
hs=...\TasmoHAB\ohgen tasmohab.py

with virtualenv path:
- pyinstaller --onefile --windowed --icon=icon.ico --noconsole --clean --paths=...\PyCharm\venv\Lib\site-packages --paths=...\PyCharm\TasmoHAB --pat
hs=...\PyCharm\TasmoHAB\ohgen tasmohab.py

For Debug (not windowed):
- pyinstaller --onefile --debug all --icon=icon.ico --clean --paths=...\PyCharm\venv\Lib\site-packages --paths=...\PyCharm\TasmoHAB --pat
hs=...\PyCharm\TasmoHAB\ohgen tasmohab.py
- And then: ".\dist\tasmohab.exe"

after successfull build (uses last build config in spec file):
- pyinstaller tasmohab.spec

alternatives:
- pip install auto-py-to-exe
- auto-py-to-exe

## Requirements:
- tasmota device tested with firmware >8.3.1 
- pip install -r requirements.txt

## Credits
- Thanks to https://github.com/jimtng for this initial release of his work!
