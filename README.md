# TasmoHAB - OpenHAB Things and Items Generator via GUI

## Usage
I was inspired by the project https://github.com/jimtng/ohgen to easily link a Tasmota device with OpenHab through a GUI. The programme uses the almost identical code of 'ohgen' to generate the things and items files.
In the first step, all tasmota gpios of a device are queried and the peripherals are displayed in a table. Then the user can select or deselect individual actuators or sensors in the table. In the next step, a (.yaml) config for 'ohgen' is generated, which contains the objects selected by the user. This config can still be edited here.
In the last step, the things and items objects for openhab are displayed. These can either be copied or saved as files.
All read-in and processed data (sensors, device status, actuators, user settings, etc.) can be conveniently viewed in JSON format.

The programme still has potential for improvement, but it is already doing its job.

I would like to invite everyone to participate in the project to improve the tool!

![tasmohab](https://user-images.githubusercontent.com/49484063/122906746-c58c0900-d352-11eb-86c3-e09ea664d0fe.jpg)
![tasmohab3](https://user-images.githubusercontent.com/49484063/122906848-ddfc2380-d352-11eb-9325-dfcb451a60f7.jpg)


## How it works
[Show tasmota objects in scrollarea](https://github.com/Gifford47/tasmohab/blob/b7782cbbf6d76dd2fb72342bf9faae315ba54a94/tasmohab.py#L300)<br>
Show the gpio information in a table/grid
```
def add_ui_widgets(self):
```

[Add openhab widgets](https://github.com/Gifford47/tasmohab/blob/b7782cbbf6d76dd2fb72342bf9faae315ba54a94/tasmohab.py#L374)<br>
add the openhab specific widgets behind the corresponding object
```
def add_ui_openhab_widgets(self, layout, row, peripheral_no='default'):
```

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
pip install -r requirements.txt
