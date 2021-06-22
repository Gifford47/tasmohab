# ohgen - OpenHAB Things and Items Generator

A template-based OpenHAB .things and .items file generator written in Python using [Jinja2](https://palletsprojects.com/p/jinja/) template engine.

The thing and items definitions are usually repetitive when you have multiple devices of the same type. The process of adding and maintaining .things and .items files involve tedious copy pasting and renaming. Changing how they are all defined is even more tedious.

`ohgen` enables you to create a template for each type of device and then generate the actual .things and .items files from a list of devices stored in `devices.yaml` file.

Example Device list:

```yaml
Light1:
  template: tasmota-light
  features:
    - color
    - ct
  groups:
    - Group1
    - Group2
  tags:
    - Tag1
    - Tag2
  metadata:
    - ga: Light

Switch1:
  template: tasmota-switch
  switches:
    - name: Light1_Switch
      label: Light1 Switch
      groups:
        - gInsideLights
    - name: Light2_Switch
      label: Light2 Switch
      groups:
        - gOutsideLights
  metadata:
    - ga: Light
```



## Usage

- Copy `quickexample.yaml` to `devices.yaml`
- Copy the directory `sample-templates` to `templates`

For convenience, `devices.yaml` will be used by default when no file is specified on the command line:
```
./ohgen.py
```

To use a different file, specify it on the command line:
```
./ohgen.py fullexample.yaml
```

By default, `ohgen` will prompt for confirmation if the output file already exists. To overwrite without prompting, specify `-o` or `--overwrite` in the command line, i.e.:
```
./ohgen.py -o
```

## Config and Device List File: `devices.yaml`

The `devices.yaml` file contains list of devices/things to be generated. For examples: see `quickexample.yaml` and `fullexample.yaml`


### The `settings` section

#### A Quick Example of the settings section:
```yaml
settings:
  output: mydefaultoutput
  template: tasmota-light-cct
  outputs:
    mydefaultoutput: 
      things-file: /openhab/conf/things/mythings.things
      items-file: /openhab/conf/items/myitems.items
      things-file-header: |+
        // This is going at the top of the things file
      items-file-header: |+
        // This goes into the top of the items file
        Group gMyGroup
```

The `settings:` section inside `devices.yaml` consists of three areas:
- Global variables - variables that appear directly under the `settings` section. These variables act as a fall back / default for the corresponding setting.
  - `output:` the default output when nothing is specified in the `templates` section. It refers to the entry in the `outputs` section.
  - `template:` the default template to use when not specified by the thing entry. It refers to the entry in the `templates` section, or directly to `./templates/` + templatename + `.tpl`. 
  - `header:` Global headers to insert into every output file both things and items. For specific headers to insert in a specific file, see the `outputs` section below.
- `templates:` # defines the list of template names
  This section is optional. By default, the templates will load from a subdirectory `./templates/template-name.tpl`. The extension `.tpl` will be added to the template name. This section can be added to override the default output file for specific template(s), or if you want to store your templates in a different place or name.
  - `template1-name:` # the name of the template
    - `template-file:` (optional) path to the template-file, including the file name. This path can be an absolute path, or relative to devices.yaml file. 
    
        When this setting is omitted, the default is set to "templates/template1-name.tpl" - where `template1-name` is the name of the template section above. 
    - `output`: (optional) outputname that applies for this template, overrides the global `output` variable
  - `template2-name:` # another template, for a different type of device or the same device but different configurations
    - `template-file:` path-to-the-template-file
    - `output:` `outputname` Multiple templates can be directed to the same outputname, which in turn will be saved in to the same files

- `outputs:` #The list of output file definitions. Multiple output files can be specified here, for example if you'd like to have a separate file for lights, switches, sensors, etc.
  - `output1-name:` 
    - `things-file:` path to the .things file, absolute or relative to this file (devices.yaml). Example: /openhab/conf/things/thingsfilename.things
    - `items-file:` path to the .items file. Example: /openhab/conf/items/itemsfilename.items
    - `things-file-header:` # extra headers to insert at the top of the generated .things file. Note that multiple lines can be entered in yaml using `|+` directly after the colon.
    - `items-file-header:` # extra headers to put at the top of the generated .items file

## Template

By default, template files are stored in `templates/` subdirectory, relative to the `devices.yaml` file, however this can be overridden in the devices.yaml file.

A template file contains the template of both Things and Items required for a particular type of device. The general format for the template file is as follows:

```php
# Hash comments are allowed and will be omitted from the generated file
// Thing / Item comments starting with double slashes will be included.
Thing thingid ..... {
    // put Thing comments inside the Thing declaration, otherwise they will go into the Items file.

}

Switch ItemName_XX ......
Number ItemName_YY ....
```

A template can contain only Thing, or only Items, or both. Multiple Things, Bridges, and Items can exist in a template. 

Rules for Thing and Bridge definition in the template:
- The opening brace must be at the end of the same line as `Thing` or `Bridge`
- The closing brace must be on its own separate line
- A `Thing` can be nested inside a `Bridge` observing the rules above

Variables from `devices.yaml` for the device will be substituted in the template file. Each thing entry in the yaml file will be loaded as a dictionary, which can be used inside the template. For detailed information about the template syntax, see [Jinja2 Template Designer](https://jinja.palletsprojects.com/templates/).

For more detailed examples, see the included templates in the sample-templates directory. Note that the included templates may change in the future. 

### Special Filters in the template

Filters are functions or variable modifiers in the template that takes the variable as an input and can produce a different output. To run a variable through a filter, add a pipe symbol between the variable and the filter like this: `{{variablename|filtername}}`

In addition to the [builtin filters from Jinja2](https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-builtin-filters), `ohgen` provides the following special filters:
- `groups`: applies to an array of group names. It will automatically create a comma separated list enclosed in parentheses. Example:
  ```yaml
  Item1:
    groups:
      - Group1
      - Group2
  ```

  Inside the template:
  ```
  Number {{name} {{groups|groups}} 
  ```

  Which will produce:
  ```
  Number Item1 (Group1, Group2)
  ```

- `tags` applies to an array of tag names. It will automatically create a comma separated list enclosed in square brackets, with each tag enclosed in double quotes. Example:
  ```yaml
  Item1:
    tags:
      - Tag1
      - Tag2
  ```

  Template:
  ```
  Number {{name} {{tags|tags}} 
  ```
  Which will produce:
  ```
  Number Item1 ["Tag1", "Tag2"]
  ```
- `metadata` applies to an array of metadata. It supports several different ways of specifying metadata in the yaml file. Example:
  ```yaml
  Item1:
    metadata:
      - style1a="value"
      - style1b="value" [ config1="value1", config2="value2" ]
      - style2: value
      - key: style3a
        value: value3
        configuration:
          - config1: value1
          - config2: value2
      - key: style3b
        value: value3
        configuration:
          - config1="value1"
          - config2="value2"
  ```
  Template:
  ```
  Number {{name} { {{metadata|metadata}} }
  ```
  Output:
  ```
  Number Item1 { style1a="value", style1b="value" [ config1="value1", config2="value2" ], style2="value", style3a="value3" [ config1="value1", config2="value2" ], style3b="value3" [ config1="value1", config2="value2" ] }
  ```

- `quote` will enclose a non-empty value with double quotes. This is handy for labels.



Note that the above constructs can also be created purely using Jinja2's loop and conditional statements. They are provided by `ohgen` for simplicity.

## Include and Macro

Jinja2 has a feature to [include another template](https://jinja.palletsprojects.com/en/2.11.x/templates/#include) and [import macros](https://jinja.palletsprojects.com/en/2.11.x/templates/#import). This is supported by `ohgen` also. The path reference inside the template is relative to the template folder.