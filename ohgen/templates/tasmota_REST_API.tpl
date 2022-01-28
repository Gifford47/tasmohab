{#
  First is the thing
#}

{
{%- set mqttUID ='local_mqtt' -%}
  "label": "{{label}} on {{ip}}",
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
    {%- for item in switch %}
    {
      "linkedItems": [
        "{{thingid}}_{{item.name}}{{loop.index}}"
      ],
      "uid": "mqtt:topic:{{mqttUID}}:{{thingid}}:{{item.name}}{{loop.index}}",
      "id": "{{item.label|replace(" ", "_")}}_{{item.name}}{{loop.index}}",
      "channelTypeUID": "mqtt:switch",
      "itemType": "switch",
      "kind": "STATE",
      "label": "{{item.label}}",
      "description": "{{item.label}}",
      "defaultTags": [
        "{{item.tags}}"
      ],
      "properties": {
      },
      "configuration": {
        "retained": false,
        "postCommand": false,
        "formatBeforePublish": "%s",
        "commandTopic": "cmnd/{{topic}}/POWER{{loop.index}}",
        "step": 1,
        "stateTopic": "stat/{{topic}}/RESULT",
        "transformationPattern": "JSONPATH:$.POWER{{loop.index}}",
        "off": "0",
        "on": "1"
      }
    },
    {%- endfor %}
    {%- for item in number %}
    {
      "linkedItems": [
        "{{thingid}}_{{item.name}}_{{item.label}}"
      ],
      "uid": "mqtt:topic:{{mqttUID}}:{{thingid}}:{{item.name}}",
      "id": "{{item.label|replace(" ", "_")}}_{{item.name}}",
      "channelTypeUID": "mqtt:number",
      "itemType": "number",
      "kind": "STATE",
      "label": "{{item.label}}",
      "description": "{{item.label}}",
      "defaultTags": [
        "{{item.tags}}"
      ],
      "properties": {
      },
      "configuration": {
        "retained": false,
        "postCommand": false,
        "formatBeforePublish": "%s",
        "step": 1,
        "stateTopic": "tele/{{topic}}/SENSOR",
        "transformationPattern": "JSONPATH:$.{{item.name}}.{{item.label}}"
      }
    },
    {%- endfor %}
    {%- for item in dimmer %}
    {
      "linkedItems": [
        "{{thingid}}_{{item.name}}{{loop.index}}"
      ],
      "uid": "mqtt:topic:{{mqttUID}}:{{thingid}}:{{item.name}}{{loop.index}}",
      "id": "{{item.label|replace(" ", "_")}}_{{item.name}}{{loop.index}}",
      "channelTypeUID": "mqtt:number",
      "itemType": "dimmer",
      "kind": "STATE",
      "label": "{{item.label}}",
      "description": "{{item.label}}",
      "defaultTags": [
        "{{item.tags}}"
      ],
      "properties": {
      },
      "configuration": {
        "retained": false,
        "postCommand": false,
        "formatBeforePublish": "%s",
        "commandTopic": "cmnd/{{topic}}/Dimmer{{loop.index}}",
        "step": 1,
        "stateTopic": "tele/{{topic}}/SENSOR",
        "transformationPattern": "JSONPATH:$.Dimmer{{loop.index}}"
      }
    },
    {%- endfor %}
    {%- for item in string %}
    {
      "linkedItems": [
        "{{thingid}}_{{item.name}}_{{item.label}}"
      ],
      "uid": "mqtt:topic:{{mqttUID}}:{{thingid}}:{{item.name}}{{loop.index}}",
      "id": "{{item.label|replace(" ", "_")}}_{{item.name}}{{loop.index}}",
      "channelTypeUID": "mqtt:string",
      "itemType": "string",
      "kind": "STATE",
      "label": "{{item.label}}",
      "description": "{{item.label}}",
      "defaultTags": [
        "{{item.tags}}"
      ],
      "properties": {
      },
      "configuration": {
        "retained": false,
        "postCommand": false,
        "formatBeforePublish": "%s",
        "step": 1,
        "stateTopic": "tele/{{topic}}/SENSOR",
        "transformationPattern": "JSONPATH:$.{{item.name}}.{{item.label}}"
      }
    },
    {%- endfor %}
    {%- for item in contact %}
    {
      "linkedItems": [
        "{{thingid}}_{{item.name}}"
      ],
      "uid": "mqtt:topic:{{mqttUID}}:{{thingid}}:{{item.name}}{{loop.index}}",
      "id": "{{item.label|replace(" ", "_")}}_{{item.name}}{{loop.index}}",
      "channelTypeUID": "mqtt:string",
      "itemType": "string",
      "kind": "STATE",
      "label": "{{item.label}}",
      "description": "{{item.label}}",
      "defaultTags": [
        "{{item.tags}}"
      ],
      "properties": {
      },
      "configuration": {
        "retained": false,
        "postCommand": false,
        "formatBeforePublish": "%s",
        "step": 1,
        "stateTopic": "tele/{{topic}}/SENSOR",
        "transformationPattern": "JSONPATH:$.Switch{{loop.index}}.{{item.label}}"
      }
    },
    {%- endfor %}
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
  {%- for item in switch %}
  {
    "type": "Switch",
    "name": "{{thingid}}_{{item.name}}{{loop.index}}",
    "label": "{{item.label}}",
    "category": "{{item.icon}}",
    "tags": [
      "{{item.tags}}"
    ],
    "groupNames": {{item.groups.split(',')}},
  },
  {%- endfor %}
    {%- for item in number %}
  {
    "type": "Number",
    "name": "{{thingid}}_{{item.name}}_{{item.label}}",
    "label": "{{item.label}}",
    "category": "{{item.icon}}",
    "tags": [
      "{{item.tags}}"
    ],
    "groupNames": {{item.groups.split(',')}},
  },
  {%- endfor %}
  {%- for item in dimmer %}
  {
    "type": "Dimmer",
    "name": "{{thingid}}_{{item.name}}{{loop.index}}",
    "label": "{{item.label}}",
    "category": "{{item.icon}}",
    "tags": [
      "{{item.tags}}"
    ],
    "groupNames": {{item.groups.split(',')}},
  },
  {%- endfor %}
  {%- for item in string %}
  {
    "type": "String",
    "name": "{{thingid}}_{{item.name}}_{{item.label}}",
    "label": "{{item.label}}",
    "category": "{{item.icon}}",
    "tags": [
      "{{item.tags}}"
    ],
    "groupNames": {{item.groups.split(',')}},
  },
  {%- endfor %}
]
