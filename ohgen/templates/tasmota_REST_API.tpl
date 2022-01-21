{#
  First is the thing
#}

{
{%- set mqttUID ='local_mqtt' -%}
  "label": "{{label}}",
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
        "{{thingid}}_{{item.name}}"
      ],
      "uid": "mqtt:topic:{{mqttUID}}:{{thingid}}:{{item.name}}",
      "id": "{{item.label|replace(" ", "_")}}_{{item.name}}",
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
        "commandTopic": "cmnd/{{topic}}/POWER1",
        "step": 1,
        "stateTopic": "stat/{{topic}}/RESULT",
		"transformationPattern": "JSONPATH:$.POWER",
        "off": "0",
        "on": "1"
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
    "name": "{{thingid}}_{{item.name}}",
    "label": "{{item.label}}",
    "category": "{{item.icon}}",
    "tags": [
      "{{item.tags}}"
    ],
    "groupNames": {{item.groups.split(',')}},
  },
  {%- endfor %}
]
