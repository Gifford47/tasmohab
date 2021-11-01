{%- set groups = groups|default([]) -%}
{%- set tags = tags|default([]) -%}

{%- for item in number %}
Name:{{item.name}} Label:{{item.label}} Feature:{{item.features}} groups:{{item.groups}} tags:{{item.tags}} meta:{{item.metadata}} icon:{{item.icon}}
{%- endfor %}
