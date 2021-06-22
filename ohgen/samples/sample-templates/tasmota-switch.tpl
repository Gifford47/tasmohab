{# 
  This is for a multi-gang wall switch, e.g. Deta Smart Grid Connect
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
Thing mqtt:topic:mosquitto:{{thingid}} "{{label}}" (mqtt:broker:mosquitto) {
    Channels:
{%- for item in switches %}
        Type switch : power{{loop.index}}    [ stateTopic="stat/{{thingid}}/RESULT", transformationPattern="REGEX:(.*POWER{{loop.index}}.*)∩JSONPATH:$.POWER{{loop.index}}", commandTopic="cmnd/{{thingid}}/POWER{{loop.index}}" ]
{%- else %}
        Type switch : power     [ stateTopic="stat/{{thingid}}/RESULT", transformationPattern="REGEX:(.*POWER.*)∩JSONPATH:$.POWER", commandTopic="cmnd/{{thingid}}/POWER" ]
{%- endfor %}
{%- for item in buttons %}
        Type string : button{{loop.index}}   [ stateTopic="stat/{{thingid}}/BUTTON{{loop.index}}", transformationPattern="JSONPATH:$.ACTION" ]
{%- endfor %}
        Type switch : reachable [ stateTopic="tele/{{thingid}}/LWT", on="Online", off="Offline" ]
        Type number : rssi      [ stateTopic="tele/{{thingid}}/STATE", transformationPattern="JSONPATH:$.Wifi.RSSI" ]
        Type string : state     [ stateTopic="tele/{{thingid}}/dummy", commandTopic="cmnd/{{thingid}}/STATE" ]
}

{%- set groups = groups|default([]) -%}
{%- set tags = tags|default([]) -%}
{%- for item in switches -%}
        {% set item_groups = item['groups']|default([]) -%}
        {% set item_tags = item['tags']|default([]) -%}
        {% set groups = groups|default([]) -%}
        {% set tags = tags|default([]) -%}
        Switch {{item['name']}} {{item['label']|quote}} {{item['icon']|default('<switch>')}}{{ (groups+item_groups)|groups }}{{ (tags + item_tags)|tags }} { channel="mqtt:topic:mosquitto:{{thingid}}:power{{loop.index}}", autoupdate="false"{{ metadata|metadata }}{{ item['metadata']|metadata }} }
{% else -%}
        Switch {{name}}  {{label|quote}} {{icon|default('<switch>')}}{{groups|groups}}{{tags|tags}} { channel="mqtt:topic:mosquitto:{{thingid}}:power", autoupdate="false"{{metadata|metadata}} }
{% endfor %}
{%- for item in buttons -%}
        String {{item['name']}} {{item['label']|quote}} {{ item['groups']|groups }}{{ item['tags']|tags }} { channel="mqtt:topic:mosquitto:{{thingid}}:button{{loop.index}}", autoupdate="false"{{ metadata|metadata }}{{ item['metadata']|metadata }} }
{% endfor -%}
Number {{name}}_RSSI   "{{label}} RSSI [%d%%]"  <network> (gSignalStrength)  { channel="mqtt:topic:mosquitto:{{thingid}}:rssi" }
String {{name}}_State	(gTasmotaState)                            { channel="mqtt:topic:mosquitto:{{thingid}}:state" }
