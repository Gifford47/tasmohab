Thing mqtt:topic:mosquitto:{{thingid}} "{{label}}" (mqtt:broker:mosquitto)  @ "Environment" {
    Channels:
        Type number : temperature  [ stateTopic="zigbee/{{thingid}}/temperature", unit="°C" ]
        Type number : humidity     [ stateTopic="zigbee/{{thingid}}/humidity", unit="%" ]
        Type number : pressure     [ stateTopic="zigbee/{{thingid}}/pressure", unit="mbar" ]
        Type number : linkquality  [ stateTopic="zigbee/{{thingid}}/linkquality" ]
        Type switch : reachable    [ stateTopic="zigbee/{{thingid}}/availability", on="online", off="offline" ]
        Type number : battery      [ stateTopic="zigbee/{{thingid}}/battery", unit="%" ]
}

{%- set ga_group = 'g{}_Temperature'.format(name_parts[0]) -%}
Group {{ga_group}} "{{room}} Temperature" { ga="Thermostat" }
{%- set groups = ['gTemperature', ga_group] + groups|default([]) %}
Number:Temperature {{name_parts[0]}}_Temperature         "{{room}} Temperature" <temperature> {{groups|groups}}{{tags|tags}} { channel="mqtt:topic:mosquitto:{{thingid}}:temperature", expire="65m", ga="thermostatTemperatureAmbient"{{metadata|metadata}} }
Number             {{name_parts[0]}}_Humidity            "{{room}} Humidity [%.1f%%]" <humidity> {{ humidity_groups|groups }} { channel="mqtt:topic:mosquitto:{{thingid}}:humidity" }
Number             {{name_parts[0]}}_Pressure            "{{room}} Pressure"                   { channel="mqtt:topic:mosquitto:{{thingid}}:pressure" }
Number             {{name}}_Link    "{{label}} Link"             <network>  (gSignalStrength) { channel="mqtt:topic:mosquitto:{{thingid}}:linkquality" }
Number             {{name}}_Battery "{{label}} Battery [%d%%]"   <battery>  (gBatteries)      { channel="mqtt:topic:mosquitto:{{thingid}}:battery" }
