{# 
This template doesn't include a 'thing' - because it is for an item that is linked to multiple channels. 
The things / channels must be specified elsewhere
#}
// Multi channel light
Switch {{name}}_Power   "{{label}} Power" <light> {{groups|groups}}{{tags|tags}} { {% for c in channels: %}channel="mqtt:topic:mosquitto:{{c}}:power", {% endfor %}autoupdate="false"{{ metadata|metadata }} }
Dimmer {{name}}_Dimmer  {{label|quote}} { {% for c in channels: %}channel="mqtt:topic:mosquitto:{{c}}:dimmer"{% if not loop.last %}, {% endif %}{% endfor %}{{metadata|metadata}} }
String {{name}}_Color   "{{label}} Colour"              { {% for c in channels: %}channel="mqtt:topic:mosquitto:{{c}}:color"{% if not loop.last %}, {% endif %}{% endfor %} }

