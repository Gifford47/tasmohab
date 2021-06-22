Thing mqtt:topic:mosquitto:{{thingid}} "{{label}}" (mqtt:broker:mosquitto) {
    Channels:
        Type switch: power       [ stateTopic="zigbee/{{thingid}}/state", commandTopic="zigbee/{{thingid}}/set/state", on="ON", off="OFF" ]
        Type dimmer: dimmer      [ stateTopic="zigbee/{{thingid}}/brightness", commandTopic="zigbee/{{thingid}}/set/brightness", min=0, max=255, step=1 ]
        Type dimmer: ct          [ stateTopic="zigbee/{{thingid}}/color_temp", commandTopic="zigbee/{{thingid}}/set/color_temp", min=153, max=500, step=1 ]
        Type number: linkquality [ stateTopic="zigbee/{{thingid}}/linkquality" ]
        Type switch: reachable   [ stateTopic="zigbee/{{thingid}}/availability", on="online", off="offline" ]
} 

Switch {{name}}_Power   "{{label}} Power" <light> {{groups}} { channel="mqtt:topic:mosquitto:{{thingid}}:power", autoupdate="false" }
Dimmer {{name}}_Dimmer  "{{label}} [%d%%]" { channel="mqtt:topic:mosquitto:{{thingid}}:dimmer"{% for m in metadata %}, {{m}}{%endfor%} }
Dimmer {{name}}_CT      "{{label}} Colour Temperature"     { channel="mqtt:topic:mosquitto:{{thingid}}:ct" }
Number {{name}}_Link    "{{label}} Link" <network> (gSignalStrength) { channel="mqtt:topic:mosquitto:{{thingid}}:linkquality" }

