{#
  TODO:
  - metadata not included
  - add. items: reachable, RSSI, version
  - cmd and state topic for all types correct?
#}
{#
  First is the thing. Use Following url for explanations: https://www.openhab.org/addons/bindings/mqtt.generic/
#}

{
{%- set mqttUID ='local_mqtt' -%}
  "label": "{{label}} ({{ip}})",
  "bridgeUID": "mqtt:broker:{{mqttUID}}",
  "configuration": {
    "availabilityTopic": "tele/{{topic}}/LWT",
    "payloadNotAvailable": "Offline",
    "payloadAvailable": "Online"
  },
  "properties": {
  },
  "UID": "mqtt:topic:{{mqttUID}}:{{thingid}}",
  "thingTypeUID": "mqtt:topic",
  "location": "",
  "channels": [
    {% include "REST/oh_contact_channel" %}
    {% include "REST/oh_dimmer_channel" %}
    {% include "REST/oh_number_channel" %}
    {% include "REST/oh_rollershutter_channel" %}
    {% include "REST/oh_switch_channel" %}
    {% include "REST/oh_string_channel" %}
    {% include "REST/oh_group_channel" %}
    {% include "REST/oh_player_channel" %}
    {% include "REST/oh_location_channel" %}
    {% include "REST/oh_image_channel" %}
    {% include "REST/oh_color_channel" %}
    
    {
      "linkedItems": [
        "{{thingid}}_Version"          {# must match "linkeditems" definition from item #}
      ],
      "uid": "mqtt:topic:{{mqttUID}}:{{thingid}}:Version",
      "id": "{{label|replace(" ", "_")}}_Version",
      "channelTypeUID": "mqtt:string",
      "itemType": "string",
      "kind": "STATE",
      "label": "Firmware Version",
      "description": "Tasmota Firmware Version",
      "defaultTags": [
      ],
      "properties": {
      },
      "configuration": {
        "retained": false,
        "postCommand": false,
        "formatBeforePublish": "%s",
        "step": 1,
        "stateTopic": "tele/{{topic}}/INFO1",
        "transformationPattern": "REGEX:(.*Info1.*)∩JSONPATH:$.Info1.Version"
      }
    }
  ]
}

{#
#####
Here are the items:
#####
#}
[
  {
    "type": "Group",
    "name": "{{thingid}}",
    "label": "{{label}}",
    "category": "",
    "tags": [
      "Equipment"
    ],
    "groupNames": [
      "{{location}}"
    ],
  },
  {%- for item in contact %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_contact_item" %}
  {%- endfor %}
  {%- for item in dimmer %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_dimmer_item" %}
  {%- endfor %}
  {%- for item in number %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_number_item" %}
  {%- endfor %}
  {%- for item in rollershutter %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
      {% include "REST/oh_dimmer_item" %}
    {#
      {% include "REST/oh_rollershutter_item" %}
    #}
  {%- endfor %}
  {%- for item in switch %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_switch_item" %}
  {%- endfor %}
  {%- for item in string %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_string_item" %}
  {%- endfor %}
  {%- for item in group %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_group_item" %}
  {%- endfor %}
  {%- for item in player %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_player_item" %}
  {%- endfor %}
  {%- for item in location %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_location_item" %}
  {%- endfor %}
  {%- for item in image %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_image_item" %}
  {%- endfor %}
  {%- for item in color %}
    {% set for_loop = loop %}
    {% set item_obj = item %}
    {% include "REST/oh_color_item" %}
  {%- endfor %}
  
  {# This is the (constant) item for the FW-Version: #}
  {
    "type": "String",
    "name": "{{thingid}}_Version",          {# must match "linkedItems" in channel definition (from thing) #}
    "label": "{{thingid}}_Version",
    "category": "",
    "tags": [
      "Point"
    ],
    "groupNames": [
      "{{thingid}}"
    ],
  }
]
