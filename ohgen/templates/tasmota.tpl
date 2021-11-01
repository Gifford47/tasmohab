{# 
  This is for a tasmota device with sensor and actuator.
  The device definition should look like this:
  Device_Name:
       template: tasmota-switch-multi
       switches:
               - name: Name_Of_Switch1_Item
                 label: Label for Switch 1
                 groups: (gSomethingForSwitch1)
               - name: Name_Of_Switch2_Item
                 label: Label for Switch 2
                 groups: (gSomethingForSwitch2)
#}
Thing mqtt:topic:{{thingid}} "{{label}}" (mqtt:broker:local_mqtt) {
    Channels:
{%- for item in color %}
  Type color : color{{loop.index}}	"{{item.label}}"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.{{item.name}}", commandTopic="cmnd/{{topic}}/{{item.name}}" ]
{%- endfor %}
{%- for item in contact %}
  Type contact : contact{{loop.index}}	"{{item.label}}"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.Switch{{loop.index}}" ]
{%- endfor %}
{%- for item in dimmer %}
  Type dimmer : dimmer{{loop.index}}	"{{item.label}}"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.Dimmer{{loop.index}}", commandTopic="cmnd/{{topic}}/Dimmer{{loop.index}}" ]
{%- if 'colortemp' in features %}
  Type dimmer : {{item.name}}_ct	"{{item.label}}_ColorTemp"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.CT", commandTopic="cmnd/{{topic}}/CT", min=135, max=500, step=1 ]
{%- endif -%}
{%- if 'color' in features %}
  Type string : {{item.name}}_color	"{{item.label}}_Color"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.Color", commandTopic="cmnd/{{topic}}/Color" ]
  Type colorHSB : {{item.name}}_colorhsb	"{{item.label}}_ColorHSB"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.HSBColor", commandTopic="cmnd/{{topic}}/HSBColor" ]
{%- endif %}
{%- endfor %}
{%- for item in group %}
{%- endfor %}
{%- for item in image %}
{%- endfor %}
{%- for item in location %}
{%- endfor %}
{%- for item in number %}
{%- if number | selectattr("name", "equalto", item.name) | list | count >= 1 %}
  Type number : {{item.name}}_{{item.label|replace(" ", "_")}}	"{{item.label}}"	[ stateTopic="tele/{{topic}}/SENSOR", transformationPattern="JSONPATH:$.{{item.name}}.{{item.label}}" ]
 {%- else %}
  Type number : {{item.name}}_{{item.label|replace(" ", "_")}}	"{{item.label}}"	[ stateTopic="tele/{{topic}}/SENSOR", transformationPattern="JSONPATH:$.{{item.name}}" ]
{%- endif %}
{%- endfor %}
{%- for item in player %}
{%- endfor %}
{%- for item in rollershutter %}
  Type rollershutter : rollershutter{{loop.index}}	"{{item.label}}"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.{{item.name}}", commandTopic="cmnd/{{topic}}/{{item.name}}" ]
{%- endfor %}
{%- for item in string %}
Type string : string{{loop.index}}	"{{item.label}}"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.{{item.name}}", commandTopic="cmnd/{{topic}}/{{item.name}}" ]
{%- endfor %}
{%- for item in switch %}
  Type switch : power{{loop.index}}	"{{item.label}}"	[ stateTopic="stat/{{topic}}/RESULT", transformationPattern="JSONPATH:$.Power{{loop.index}}", commandTopic="cmnd/{{topic}}/Power{{loop.index}}" ]
{%- endfor %}

  Type switch : reachable	"Reachable"	[ stateTopic="tele/{{topic}}/LWT", on="Online", off="Offline" ]
  Type string : Version	"Firmware"	[ stateTopic="tele/{{topic}}/INFO1", transformationPattern="JSONPATH:$.Version" ]
  Type number : RSSI	"RSSI"	[ stateTopic="tele/{{topic}}/STATE", transformationPattern="JSONPATH:$.Wifi.RSSI" ]
  //Type string : WifiDowntime	"WifiDowntime"	[ stateTopic="tele/{{topic}}/STATE", transformationPattern="JSONPATH:$.Wifi.Downtime" ]
  //Type number : LoadAvg	"LoadAVG"	[ stateTopic="tele/{{topic}}/STATE", transformationPattern="JSONPATH:$.LoadAvg" ]
  //Type number : Uptime	"Uptime"	[ stateTopic="tele/{{topic}}/STATE", transformationPattern="JSONPATH:$.UptimeSec" ]
}

{# 
#####
Here are the items:
#####
#}
{%- set groups = groups|default([]) -%}
{%- set tags = tags|default([]) -%}

Group {{thingid}}		"{{label}}"		({{location}})		[Equipment]

{%- for item in color %}
Color {{label}}_{{item.name}}_Color		"{{item.label}}"	{{item.icon}}	{{item.groups}}	{{item.tags}}	{ channel="mqtt:topic:{{thingid}}:color{{loop.index}}" {{ item.metadata }} }
{%- endfor %}
{%- for item in contact %}
Contact {{label}}_{{item.name}}{{loop.index}}		"{{item.label}}"	{{item.icon}}	{{item.groups}}	{{item.tags}}	{ channel="mqtt:topic:{{thingid}}:contact{{loop.index}}" {{ item.metadata }} }
{%- endfor %}
{%- for item in dimmer %}
Dimmer {{label}}_{{item.name}}_Dimmer		"{{item.label}}"	{{item.icon}}	{{item.groups}}	{{item.tags}}	{ channel="mqtt:topic:{{thingid}}:dimmer{{loop.index}}" {{ item.metadata }} }
{%- if 'ct' in features %}
Dimmer {{label}}_{{item.name}}_CT		"{{item.label}} CT"				{ channel="mqtt:topic:{{thingid}}:ct" }
{%- endif %}
{%- if 'color' in features %}
String {{label}}_{{item.name}}_Color		"{{item.label}} Color"			{ channel="mqtt:topic:{{thingid}}:color" }
{%- endif %}
{%- endfor %}
{%- for item in group %}
{%- endfor %}
{%- for item in image %}
{%- endfor %}
{%- for item in location %}
{%- endfor %}
{%- for item in number %}
Number {{label}}_{{item.name}}_{{item.label|replace(" ", "_")}}		"{{item.label}}"	{{item.icon}}	{{item.groups}}	{{item.tags}}	{channel="mqtt:topic:{{thingid}}:{{item.name}}_{{item.label|replace(" ", "_")}}" {{item.metadata}}}
{%- endfor %}
{%- for item in player %}
{%- endfor %}
{%- for item in rollershutter %}
Rollershutter {{label}}_{{item.name}}_{{item.label|replace(" ", "_")}}		"{{item.label}}"	{{item.icon}}	{{item.groups}}	{{item.tags}}	{channel="mqtt:topic:{{thingid}}:rollershutter{{loop.index}}" {{item.metadata}}}
{%- endfor %}
{%- for item in string %}
String {{label}}_{{item.name}}_{{item.label|replace(" ", "_")}}		"{{item.label}}"	{{item.icon}}	{{item.groups}}	{{item.tags}}	{channel="mqtt:topic:{{thingid}}:{{item.name}}_{{item.label|replace(" ", "_")}}" {{item.metadata}}}
{%- endfor %}
{%- for item in switch %}
{% set item_groups = item['groups']|default([]) -%}
{% set item_tags = item['tags']|default([]) -%}
{% set groups = groups|default([]) -%}
{% set tags = tags|default([]) -%}
Switch {{label}}_{{item.name}}_{{item.label|replace(" ", "_")}}		"{{item.label}}"	{{item.icon}}	{{item.groups}}	{{item.tags}}	{channel="mqtt:topic:{{thingid}}:power{{loop.index}}" {{item.metadata}}}
{%- endfor %}

Switch {{label}}_Reachable		"{{label}} Reachable"		({{thingid}})	[Status]		{channel="mqtt:topic:{{thingid}}:reachable"}
String {{label}}_Version		"{{label}} Version"		({{thingid}})		[Status]	{channel="mqtt:topic:{{thingid}}:Version"}
Number {{label}}_RSSI		"{{label}} RSSI [%d%%]"	<network>	({{thingid}})	[Status]	{channel="mqtt:topic:{{thingid}}:RSSI"}