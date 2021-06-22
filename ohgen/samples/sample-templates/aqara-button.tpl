
{# Template comment which will not be rendered #}
Thing mqtt:topic:mosquitto:{{thingid}} "{{label}}" (mqtt:broker:mosquitto) {
    Channels:
        Type string: click        [ stateTopic="zigbee/{{thingid}}/click" ]
        Type string: action       [ stateTopic="zigbee/{{thingid}}/action"  ]
        Type number: linkquality  [ stateTopic="zigbee/{{thingid}}/linkquality" ]
        Type switch: reachable    [ stateTopic="zigbee/{{thingid}}/availability", on="online", off="offline" ]
        Type number: battery      [ stateTopic="zigbee/{{thingid}}/battery" ]
}

String {{name}}_Click   {{groups|groups}}{{tags|tags}}   { channel="mqtt:topic:mosquitto:{{thingid}}:click"{{metadata|metadata}} }
String {{name}}_Action  {{groups|groups}}{{tags|tags}}   { channel="mqtt:topic:mosquitto:{{thingid}}:action"{{metadata|metadata}} }
Number {{name}}_Battery "{{label}} Battery [%d%%]" <battery> (gBatteries) { channel="mqtt:topic:mosquitto:{{thingid}}:battery", expire="3h" }
Number {{name}}_Link    "{{label}} Link"      <network> (gSignalStrength) { channel="mqtt:topic:mosquitto:{{thingid}}:linkquality" }
