
Thing mqtt:topic:mosquitto:{{thingid}} "{{label}}" (mqtt:broker:mosquitto) {
    Channels:
        Type rollershutter: position [ stateTopic="zigbee/{{thingid}}/position", commandTopic="zigbee/{{thingid}}/set/position" ]
        Type number: linkquality     [ stateTopic="zigbee/{{thingid}}/linkquality" ]
        Type switch: reachable       [ stateTopic="zigbee/{{thingid}}/availability", on="online", off="offline" ]
}

Rollershutter {{name}}_Shutter {{label|quote}} {{groups|groups}}{{tags|tags}}   { channel="mqtt:topic:mosquitto:{{thingid}}:position"{{metadata|metadata}} }
String {{name}}_Action  {{groups}}   { channel="mqtt:topic:mosquitto:{{thingid}}:action" }
Number {{name}}_Link    "{{label}} Link"      <network> (gSignalStrength) { channel="mqtt:topic:mosquitto:{{thingid}}:linkquality" }
