'''
    configure
    =========

    Configure icons, stylesheets, and resource files.
'''

import argparse
import glob
import json
import os
import re
import sys

home = os.path.dirname(os.path.realpath(__file__))

def parse_args(argv=None):
    '''Parse the command-line options.'''

    parser = argparse.ArgumentParser(description='Styles to configure for a Qt application.')
    parser.add_argument(
        '--styles',
        help='''comma-separate list of styles to configure. pass `all` to build all themes''',
        default='light,dark',
    )
    parser.add_argument(
        '--extensions',
        help='''comma-separate list of styles to configure. pass `all` to build all themes''',
        default='',
    )
    parser.add_argument(
        '--resource',
        help='''output resource file name''',
        default='custom.qrc',
    )
    parser.add_argument(
        '--pyqt6',
        help='''use PyQt6 rather than PyQt5.''',
        action='store_true'
    )
    args = parser.parse_args(argv)
    parse_styles(args)
    parse_extensions(args)

    return args

def load_json(path):
    '''Read a JSON file with limited comments support.'''

    # Note: we need comments for maintainability, so we
    # can annotate what works and the rationale, but
    # we don't want to prevent code from working without
    # a complex parser, so we do something very simple:
    # only remove lines starting with '//'.
    with open(path) as file:
        lines = file.read().splitlines()
    lines = [i for i in lines if not i.strip().startswith('//')]
    return json.loads('\n'.join(lines))

def read_template_dir(directory):
    '''Read the template data from a directory'''

    data = {
        'stylesheet': open(f'{directory}/stylesheet.qss.in').read(),
        'icons': [],
    }
    if os.path.exists(f'{directory}/icons.json'):
        icon_data = load_json(f'{directory}/icons.json')
    else:
        icon_data = {}
    for file in glob.glob(f'{directory}/*.svg.in'):
        svg = open(file).read()
        name = os.path.splitext(os.path.splitext(os.path.basename(file))[0])[0]
        if name in icon_data:
            replacements = icon_data[name]
        else:
            # Need to find all the values inside the image.
            keys = re.findall(r'\^[0-9a-zA-Z_-]+\^', svg)
            replacements = [i[1:-1] for i in keys]
        data['icons'].append({
            'name': name,
            'svg': svg,
            'replacements': replacements,
        })

    return data

def split_csv(string):
    '''Split a list of values provided as comma-separated values.'''

    values = string.split(',')
    return [i for i in values if i]

def parse_styles(args):
    '''Parse a list of valid styles.'''

    values = split_csv(args.styles)
    if 'all' in values:
        files = glob.glob(f'{home}/theme/*json')
        values = [os.path.splitext(os.path.basename(i))[0] for i in files]
    args.styles = values

def parse_extensions(args):
    '''Parse a list of valid extensions.'''

    values = split_csv(args.extensions)
    if 'all' in values:
        files = glob.glob(f'{home}/extension/*/*stylesheet.qss.in')
        values = [os.path.basename(os.path.dirname(i)) for i in files]
    args.extensions = values

def parse_hexcolor(color):
    '''Parse a hexadecimal color.'''

    # Have a hex color: can be 6 or 8 (non-standard) items.
    color = color[1:]
    if len(color) not in (6, 8):
        raise NotImplementedError

    red = int(color[:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)
    alpha = 1.0
    if len(color) == 8:
        alpha = int(color[6:8], 16) / 100
    return (red, green, blue, alpha)

def parse_rgba(color):
    '''Parse an RGBA color.'''

    # Match our rgba character. Note that this is
    # First split the rgba components to get the inner stuff.
    # Both rgb() and rgba() can have or omit an alpha layer.
    rgba = re.match(r'^\s*rgba?\s*\((.*)\)\s*$', color).group(1)
    split = re.split(r'(?:\s*,\s*)|\s+', rgba)
    if len(split) not in (3, 4):
        raise NotImplementedError
    red = int(split[0])
    green = int(split[1])
    blue = int(split[2])
    alpha = 1.0
    if len(split) == 4:
        alpha = float(split[3])
    return (red, green, blue, alpha)

def parse_color(color):
    '''Parse a color into the RGBA components.'''

    if color.startswith('#'):
        return parse_hexcolor(color)
    elif color.startswith('rgb'):
        return parse_rgba(color)
    raise NotImplementedError

def icon_basename(icon, extension):
    '''Get the basename for an icon.'''

    if extension == 'default':
        return icon
    return f'{icon}_{extension}'

def replace_by_name(contents, theme, colors=None):
    '''Replace values by color name.'''

    # The placeholders have a syntax like `^foreground^`.
    # To simplify the replacement process, you can specify
    # a limited subset of colors, rather than use all of them.
    if colors is None:
        colors = theme.keys()
    for key in colors:
        color = theme[key]
        contents = contents.replace(f'^{key}^', color)
    return contents

def replace_by_index(contents, theme, colors):
    '''Replace values by color name.'''

    # The placeholders have a syntax like `^0^`, where
    # the is a list of valid colors and the index of
    # the color is the replacement key.
    # This is useful since we can want multiple colors
    # for the same icon (such as hovered arrows).
    for index, key in enumerate(colors):
        sub = f'^{index}^'
        # Need special handle values with opacities. Standard
        # SVG currently does not support `rgba` syntax, with an
        # opacity, but it does provide `fill-opacity` and `stroke-opacity`.
        # Therefore, if the replacement specifies `opacity` or `hex`,
        # parse the color, get the correct value, and use only that
        # for the replacement.
        if key.endswith(':hex'):
            color = theme[key[:-len(':hex')]]
            rgb = [f"{i:02x}" for i in parse_color(color)[:3]]
            value = f'#{"".join(rgb)}'
        elif key.endswith(':opacity'):
            color = theme[key[:-len(':opacity')]]
            value = str(parse_color(color)[3])
        else:
            value = theme[key]
        contents = contents.replace(sub, value)
    return contents

def configure_icons(config, style):
    '''Configure icons for a given style.'''

    theme = config['themes'][style]
    for template in config['templates']:
        for icon in template['icons']:
            replacements = icon['replacements']
            name = icon['name']
            if isinstance(replacements, dict):
                # Then we have the following format:
                #   The key is the substate of the icon, such
                #   as default, hover, pressed, etc, and the value
                #   is an ordered list of replacements.
                for ext, colors in replacements.items():
                    contents = replace_by_index(icon['svg'], theme, colors)
                    filename = f'{home}/dist/{style}/{icon_basename(name, ext)}.svg'
                    with open(filename, 'w') as file:
                        file.write(contents)
            else:
                # Then we just have a list of replacements for the
                # icon, using standard colors. For example,
                # replacement values might be `^foreground^`.
                assert isinstance(replacements, list)
                contents = replace_by_name(icon['svg'], theme, replacements)
                filename = f'{home}/dist/{style}/{name}.svg'
                with open(filename, 'w') as file:
                    file.write(contents)

def configure_stylesheet(config, style):
    '''Configure the stylesheet for a given style.'''

    contents = '\n'.join([i['stylesheet'] for i in config['templates']])
    contents = replace_by_name(contents, config['themes'][style])
    # Need to replace the URL paths for loading icons/
    # assets. In C++ Qt and PyQt5, this uses the resource
    # system, AKA, `url(:/dark/path/to/resource)`. In PyQt6, the
    # resource system has been replaced to use native
    # Python packaging, so we define a user-friendly name
    # based on the theme name, so `url(dark:path/to/resource)`.
    if config['pyqt6']:
        contents = contents.replace('^style^', f'{style}:')
    else:
        contents = contents.replace('^style^', f':/{style}/')

    with open(f'{home}/dist/{style}/stylesheet.qss', 'w') as file:
        file.write(contents)

def configure_style(config, style):
    '''Configure the icons and stylesheet for a given style.'''

    os.makedirs(f'{home}/dist/{style}', exist_ok=True)
    configure_icons(config, style)
    configure_stylesheet(config, style)

def write_xml(config):
    '''Simple QRC writer.'''

    # rcc doesn't exist for PyQt6
    assert not config['pyqt6']
    resources = []
    for style in config['themes'].keys():
        files = os.listdir(f'{home}/dist/{style}')
        resources += [f'{style}/{i}' for i in files]
    with open(f'{home}/dist/{config["resource"]}', 'w') as file:
        print('<RCC>', file=file)
        print('  <qresource>', file=file)
        for resource in sorted(resources):
            print(f'    <file>{resource}</file>', file=file)
        print('  </qresource>', file=file)
        print('</RCC>', file=file)

def configure(args):
    '''Configure all styles and write the files to a QRC file.'''

    # Need to convert our styles accordingly.
    config = {
        'themes': {},
        'templates': [],
        'pyqt6': args.pyqt6,
        'resource': args.resource
    }
    config['templates'].append(read_template_dir(f'{home}/template'))
    for style in args.styles:
        config['themes'][style] = load_json(f'{home}/theme/{style}.json')
    for extension in args.extensions:
        config['templates'].append(read_template_dir(f'{home}/extension/{extension}'))

    for style in config['themes'].keys():
        configure_style(config, style)

    if not args.pyqt6:
        # No point generating a resource file for PyQt6,
        # since we can't use rcc6 anyway.
        write_xml(config)

def main(argv=None):
    '''Configuration entry point'''
    configure(parse_args(argv))

if __name__ == '__main__':
    sys.exit(main())
