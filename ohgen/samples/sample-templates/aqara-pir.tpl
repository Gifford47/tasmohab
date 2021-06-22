Thing mqtt:topic:mosquitto:{{thingid}} "{{label}}" (mqtt:broker:mosquitto) {
    Channels:
        Type contact : occupancy    [ stateTopic="zigbee/{{thingid}}/occupancy", on="true", off="false"  ]
        Type number  : lux          [ stateTopic="zigbee/{{thingid}}/illuminance_lux" ]
        Type number  : linkquality  [ stateTopic="zigbee/{{thingid}}/linkquality" ]
        Type switch  : reachable    [ stateTopic="zigbee/{{thingid}}/availability", on="online", off="offline" ]
        Type number  : battery      [ stateTopic="zigbee/{{thingid}}/battery" ]
}

Contact {{name_parts[0]}}_Motion       "{{room}} Motion" <motion> {{groups|groups}}{{tags|tags}}  { channel="mqtt:topic:mosquitto:{{thingid}}:occupancy"{{metadata|metadata}} }
Number  {{name_parts[0]}}_Lux          "{{room}} Lux"                             (gLux) { channel="mqtt:topic:mosquitto:{{thingid}}:lux" }
Number  {{name}}_Link     "{{label}} Link"      <network> (gSignalStrength) { channel="mqtt:topic:mosquitto:{{thingid}}:linkquality" }
Number  {{name}}_Battery  "{{label}} Battery [%d%%]" <battery> (gBatteries) { channel="mqtt:topic:mosquitto:{{thingid}}:battery", expire="1h" }
