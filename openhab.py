item_types = ['Color', 'Contact', 'Dimmer', 'Group', 'Image', 'Location', 'Number', 'Player', 'Rollershutter', 'String', 'Switch']

feature_binary = ['', 'binary']
features_light = ['', 'colortemp', 'color']
features = feature_binary + features_light

tags_temp = ['sensor', 'Temperature']
tags_hum = ['sensor', 'Humidity']

# standard definitions (for items) for sensors and actuators:
std_items = {'1216':{'std_type':item_types.index('Number'), 'feature':features, 'meta':'sensor', 'tags':tags_temp+tags_hum , 'icon':''},          # AM230X
            '160':{'std_type':item_types.index('Switch'), 'feature':[], 'meta':'', 'tags':'switch' , 'icon':'switch'},                  # switch1
            '1376':{'std_type':item_types.index('Dimmer'), 'feature':features_light, 'meta':'', 'tags':'WS2812' , 'icon':''},                       # switch1
            '32':{'std_type':item_types.index('Switch'), 'feature':[], 'meta':'', 'tags':'button' , 'icon':''},                         # button1
            'default':{'std_type':item_types.index('Number'), 'feature':features, 'meta':'', 'tags':'' , 'icon':''}                     # default value
             }

# the 'gpio_conversion' is used to convert a sensorname like 'AM2301' to its gpio number used in tasmota to identify a sensor.
# with the gpio number is then used to get its standard values for the item
gpio_conversion = { 'AM2301':'1216'
}