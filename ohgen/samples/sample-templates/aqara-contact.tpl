Thing mqtt:topic:mosquitto:{{thingid}} "{{label}}" (mqtt:broker:mosquitto) {
    Channels:
        Type contact: contact      [ stateTopic="zigbee/{{thingid}}/contact", on="false", off="true"  ]
        Type number : linkquality  [ stateTopic="zigbee/{{thingid}}/linkquality" ]
        Type switch : reachable    [ stateTopic="zigbee/{{thingid}}/availability", on="online", off="offline" ]
        Type number : battery      [ stateTopic="zigbee/{{thingid}}/battery" ]
}

Contact {{name}}_State   "{{label}} State"       {{groups|groups}}{{tags|tags}} { channel="mqtt:topic:mosquitto:{{thingid}}:contact"{{metadata|metadata}} }
Number  {{name}}_Link    "{{label}} Link"      <network> (gSignalStrength) { channel="mqtt:topic:mosquitto:{{thingid}}:linkquality" }
Number  {{name}}_Battery "{{label}} Battery [%d%%]" <battery> (gBatteries) { channel="mqtt:topic:mosquitto:{{thingid}}:battery", expire="1h" }
