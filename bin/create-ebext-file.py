#!/usr/bin/env python3
import os
import argparse

DEFAULT_DIR = '/home/ec2-user/'
EB_FILE_TEMPLATE = '''
files:
    "{dir}{fn}":
        mode: "000755"
        owner: root
        group: root
        content: |
{content}

commands:
    run-{fn_no_ext}:
        command: "{dir}{fn}"
'''.strip()


parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('config_file')
parser.add_argument('-d', '--dir', help="Directory to place the script")
args = vars(parser.parse_args())

def indent(lines, indent_by, using=' '):
    indentation = using * indent_by
    return [indentation + line for line in lines]

file = args['file']
with open(file, 'r') as fo:
    lines = fo.readlines()
content = ''.join(indent(lines, 12))

filename = os.path.basename(os.path.abspath(args['file']))
dir = args.get('dir') or DEFAULT_DIR
filename_without_ext, _ = os.path.splitext(filename)
config_file = args['config_file']


with open(config_file, 'w') as fo:
    fo.write(
        EB_FILE_TEMPLATE.format(
            fn=filename,
            fn_no_ext=filename_without_ext,
            dir=dir,
            content=content
        )
    )
