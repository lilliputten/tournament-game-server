# -*- coding:utf-8 -*-
# @module yamlSupport
# @since 2020.02.23, 02:18
# @changed 2022.02.24, 00:43


import re
import yaml
from . import utils


# Yaml extending (TODO: Extract to separated module)...
# See:
# - https://www.programcreek.com/python/example/104725/yaml.add_representer


class CustomYamlDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        #  # Got warning here: R1725: Consider using Python 3 style super() without arguments (super-with-arguments)
        #  return super(CustomYamlDumper, self).increase_indent(flow, False)
        return super().increase_indent(flow, False)


def yamlReprStr(dumper, data):
    yamlTag = 'tag:yaml.org,2002:str'
    hasNewlines = '\n' in data or '\r' in data
    if hasNewlines:  # Block style for long multiline strings...
        # @see https://pyyaml.org/wiki/PyYAMLDocumentation
        # / There are 5 styles of scalars in YAML: plain, single-quoted, double-quoted, literal, and folded:
        useStyle = '|' if len(data) > 30 else '"'
        return dumper.represent_scalar(yamlTag, data, style=useStyle)
    if re.search(r'["\'\\ /]', data):
        #  style = '"' if "'" in data and '"' not in data else "'"
        return dumper.represent_scalar(yamlTag, data, style='\'')
    return dumper.represent_str(data)
    #  return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')


yaml.add_representer(str, yamlReprStr)


class BlockString:

    # default constructor
    def __init__(self, string, maxLength=0):
        self.string = string
        self.maxLength = maxLength

    def prepareString(self):
        return utils.prepareLongString(self.string, self.maxLength)


def yamlReprBlockString(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data.prepareString(), style='|')


yaml.add_representer(BlockString, yamlReprBlockString)
